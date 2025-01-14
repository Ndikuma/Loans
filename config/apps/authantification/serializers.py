from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from .models import Role


class RegisterSerializer(RegisterSerializer):
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        required=False,  # Optional: Set to True if you want this field to be mandatory
    )
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    def save(self, request):
        user = super().save(request)

        # Set additional user fields
        user.first_name = self.validated_data.get("first_name", "")
        user.last_name = self.validated_data.get("last_name", "")
        user.role = self.validated_data.get("role")
        user.save()

        return user
