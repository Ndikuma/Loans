from dj_rest_auth.registration.views import ResendEmailVerificationView, VerifyEmailView


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
