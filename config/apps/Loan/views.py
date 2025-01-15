from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Loan, Wallet
from .serializers import LoanSerializer, WalletSerializer


class LoanViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Loan instances.
    """

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     """
    #     Restrict loans to the authenticated user.
    #     Admin users can see all loans.
    #     """
    #     user = self.request.user
    #     if user.is_staff:
    #         return Loan.objects.all()
    #     return Loan.objects.filter(client=user)

    # def perform_create(self, serializer):
    #     """
    #     Automatically set the client to the authenticated user when creating a loan.
    #     """
    #     serializer.save(client=self.request.user)


class WalletViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Wallet instances.
    """

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     """
    #     Restrict wallets to the authenticated user.
    #     Admin users can see all wallets.
    #     """
    #     user = self.request.user
    #     if user.is_staff:
    #         return Wallet.objects.all()
    #     return Wallet.objects.filter(user=user)

    # def perform_create(self, serializer):
    #     """
    #     Prevent wallet creation if a user already has one.
    #     """
    #     user = self.request.user
    #     if Wallet.objects.filter(user=user).exists():
    #         raise serializers.ValidationError("You already have a wallet.")
    #     serializer.save(user=user)
