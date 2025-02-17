from dj_rest_auth.registration.views import ResendEmailVerificationView, VerifyEmailView
from .serializers import UserSerializer,RoleSerializer
from rest_framework import viewsets
from.models import User,Role
from rest_framework.decorators import action
from rest_framework.response import Response
from config.apps.Loan.models import Loan,Wallet,WalletActivity
from config.apps.Loan.serializers import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
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
