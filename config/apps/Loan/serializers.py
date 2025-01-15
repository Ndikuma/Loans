from decimal import Decimal

from rest_framework import serializers

from .models import Loan, Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            "id",
            "user",
            "wallet_type",
            "balance",
            "max_withdrawal_limit",
            "notifications_enabled",
        ]
        read_only_fields = ["id", "balance"]

    def add_balance(self, amount: Decimal):
        wallet = self.instance
        wallet.add_balance(amount)
        return wallet

    def subtract_balance(self, amount: Decimal):
        wallet = self.instance
        wallet.subtract_balance(amount)
        return wallet


class LoanSerializer(serializers.ModelSerializer):
    total_amount_to_pay = serializers.DecimalField(
        max_digits=20, decimal_places=2, read_only=True
    )

    remaining_amount = serializers.DecimalField(
        max_digits=20, decimal_places=2, read_only=True
    )
    is_fully_repaid = serializers.BooleanField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    payment_plan = serializers.SerializerMethodField()
    payment_made = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = [
            "id",
            "client",
            "amount",
            "interest_rate",
            "duration_months",
            "start_date",
            "end_date",
            "status",
            "payment_schedule",
            "description",
            "total_amount",
            "amount_paid",
            "late_payment_fee",
            "penalty_rate",
            "approval_date",
            "created_at",
            "updated_at",
            "total_amount_to_pay",
            "remaining_amount",
            "is_fully_repaid",
            "is_overdue",
            "payment_plan",
            "payment_made",
        ]
        read_only_fields = [
            "id",
            "status",
            "total_amount",
            "amount_paid",
            "late_payment_fee",
            "created_at",
            "updated_at",
            "total_amount_to_pay",
            "remaining_amount",
            "is_fully_repaid",
            "is_overdue",
        ]

    def create(self, validated_data):
        """Override create to calculate total amount and end date."""
        loan = Loan.objects.create(**validated_data)
        loan.total_amount = loan.total_amount_to_pay()
        loan.save()
        return loan

    def update(self, instance, validated_data):
        """Override update to handle status changes."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def get_payment_plan(self, obj):
        return obj.calculate_payment_plan().get_payment_status()

    def get_payment_made(self, obj):
        return obj.calculate_payment_plan().get_payments_made()
