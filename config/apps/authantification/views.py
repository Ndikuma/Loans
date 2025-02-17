from dj_rest_auth.registration.views import ResendEmailVerificationView, VerifyEmailView
from .serializers import UserSerializer,RoleSerializer
from rest_framework import viewsets
from.models import User,Role
from rest_framework.decorators import action
from rest_framework.response import Response
from config.apps.Loan.models import Loan,Wallet,WalletActivity
from config.apps.Loan.serializers import *
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import django_filters.rest_framework

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['username', 'email']
    ordering_fields = ['date_joined']
    filterset_fields = ['email', 'role']
    lookup_field = 'id'
    ordering = ['-date_joined']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    
    @method_decorator(
        cache_page(60 * 15, key_prefix="user_list")
    )  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    
    @action(detail=True, methods=["POST"])
    def banuser(self,request,pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"message": "User has been banned."}, status=200)
    
    @action(detail=True,methods=["post"])
    def unbanuser(self,request,pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"message": "User has been unbanned."}, status=200)
    @action(detail=True,methods=["get"])
    def user_loans(self, request, pk=None):
        user = self.get_object()

        # Use Subquery to get loans related to the user
        loans = Loan.objects.filter(client=user).values('id', 'amount', "amount_paid",'status', 'created_at')
        # Use Prefetch to fetch related wallet activities
        

        return Response({
            "username": user.username,
            "email": user.email,
            "role": user.role.name,
            "loans": list(loans)  # Convert QuerySet to a list of dictionaries
        })


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes=[IsAdminUser]
    lookup_field = 'id'
    ordering = ['id']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    
    @method_decorator(
        cache_page(60 * 15, key_prefix="role_list")
    )  # Cache for 15 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    


# Custom View for verifying email
class CustomVerifyEmailView(VerifyEmailView):
    def post(self, request, *args, **kwargs):
        # You can customize the behavior here
        response = super().post(request, *args, **kwargs)
        # Add additional logic or modify the response
        response.data["custom_message"] = "Email verification processed successfully."
        return response


# Custom View for resending email verification
class CustomResendEmailVerificationView(ResendEmailVerificationView):
    def post(self, request, *args, **kwargs):
        # You can customize the behavior here
        response = super().post(request, *args, **kwargs)
        # Add additional logic or modify the response
        response.data["custom_message"] = "Verification email has been resent."
        return response
