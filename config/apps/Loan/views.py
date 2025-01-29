from datetime import datetime
from decimal import Decimal

import django_filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from elasticsearch_dsl.query import MultiMatch
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .documents import LoanDocument
from .models import Loan, Wallet
from .serializers import LoanSerializer, LoansforelasticSerializer, WalletSerializer


class LoanViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Loan instances.
    """

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["client__username", "client__email", "status"]
    ordering_fields = ["start_date", "end_date"]
    filterset_fields = ["status", "amount", "interest_rate", "duration_months"]
    lookup_field = "id"
    ordering = ["-start_date"]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    @method_decorator(
        cache_page(60 * 15, key_prefix="loans_list")
    )  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Restrict loans to the authenticated user.
        Admin users can see all loans.
        """
        user = self.request.user
        if user.is_staff:
            return Loan.objects.all()
        return Loan.objects.filter(client=user)

    def perform_create(self, serializer):
        """
        Automatically set the client to the authenticated user when creating a loan.
        """
        serializer.save(client=self.request.user)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        try:
            loan = self.get_object()
            current_date = datetime.now().date()
            if loan.status == loan.Status.PENDING:
                loan.approval_date = current_date
                loan.status = loan.Status.IN_PROGRESS
                loan._update_wallet_balance()
                loan.save()
                return Response(
                    {"message": "Loan approved successfully"}, status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Loan is not in a pending state"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        try:
            loan = self.get_object()
            if loan.status == loan.Status.PENDING:
                loan.status = loan.Status.CANCELLED
                loan.save()
                return Response(
                    {"message": "Loan rejected successfully"}, status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Loan is not in a pending state"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class WalletViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Wallet instances.
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["user__username", "user__email"]
    ordering_fields = ["user__date_joined"]
    filterset_fields = ["user__email", "balance", "notifications_enabled"]
    lookup_field = "id"
    ordering = ["-user__date_joined"]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    @method_decorator(
        cache_page(60 * 15, key_prefix="wallet_list")
    )  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Restrict wallets to the authenticated user.
        Admin users can see all wallets.
        """
        user = self.request.user
        if not Wallet.objects.filter(user=user).exists():
            Wallet.objects.create(user=user)
        if user.is_staff:
            return Wallet.objects.all()
        return Wallet.objects.filter(user=user)

    @action(detail=True, methods=["post"])
    def add_balance(self, request, pk=None):
        try:
            wallet = self.get_object()
            amount = Decimal(request.data.get("amount", 0))
            if amount <= 0:
                return Response(
                    {"error": "Amount must be greater than zero."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            wallet_serializer = self.get_serializer(wallet)
            wallet_serializer.add_balance(amount)
            wallet.save()
            return Response(
                {"message": f"Added {amount} to wallet.", "balance": wallet.balance},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=["post"])
    def subtract_balance(self, request, pk=None):
        try:
            wallet = self.get_object()
            amount = Decimal(request.data.get("amount", 0))
            if amount <= 0:
                return Response(
                    {"error": "Amount must be greater than zero."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if wallet.balance < amount:
                return Response(
                    {"error": "Insufficient balance."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            wallet_serializer = self.get_serializer(wallet)
            wallet_serializer.subtract_balance(amount)
            wallet.save()
            return Response(
                {
                    "message": f"Subtracted {amount} from wallet.",
                    "balance": wallet.balance,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoanSearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get("q", "")  # Get the search query from the URL parameter

        if query:
            # Perform a multi-match search on the Elasticsearch index
            search_results = LoanDocument.search().query(
                MultiMatch(
                    query=query,
                    fields=["amount", "interest_rate", "status", "description"],
                )
            )
        else:
            search_results = (
                LoanDocument.search()
            )  # Return all results if no query is provided

        # Serialize the results
        loans = [LoansforelasticSerializer(hit).data for hit in search_results]
        return Response(loans, status=status.HTTP_200_OK)
