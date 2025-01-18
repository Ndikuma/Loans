from decimal import Decimal

from rest_framework import serializers

from .models import Loan, Wallet, WalletActivity
from .utils import PaymentPlanCalculator


class WalletActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletActivity
        fields = [
            "id",
            "activity_type",
            "amount",
            "timestamp",
            "description",
        ]
        read_only_fields = fields


class PaymentPlanSerializer(serializers.Serializer):
    """
    Serializer for generating and displaying the payment plan of a loan.
    """

    period = serializers.CharField()
    due_date = serializers.DateField()
    payment_amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    amount_paid = serializers.DecimalField(max_digits=20, decimal_places=2)
    status = serializers.CharField()
    overdue_days = serializers.IntegerField(required=False)
    late_payment_fee = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False
    )


class WalletSerializer(serializers.ModelSerializer):
    activities = WalletActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = [
            "id",
            "user",
            "wallet_type",
            "balance",
            "notifications_enabled",
            "activities",
        ]
        read_only_fields = ["id", "balance", "activities"]

    def add_balance(self, amount: Decimal):
        wallet = self.instance
        wallet.add_balance(amount)
        return wallet

    def subtract_balance(self, amount: Decimal):
        wallet = self.instance
        wallet.subtract_balance(amount)
        return wallet


class LoanSerializer(serializers.ModelSerializer):
    remaining_amount = serializers.DecimalField(
        max_digits=20, decimal_places=2, read_only=True
    )
    is_fully_repaid = serializers.BooleanField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    payment_progress = serializers.DecimalField(
        max_digits=20, decimal_places=2, read_only=True
    )
    payment_plan = serializers.SerializerMethodField()

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
            "remaining_amount",
            "is_fully_repaid",
            "is_overdue",
            "payment_progress",
            "payment_plan",
        ]
        read_only_fields = [
            "id",
            "status",
            "total_amount",
            "amount_paid",
            "late_payment_fee",
            "total_amount_to_pay",
            "remaining_amount",
            "is_fully_repaid",
            "is_overdue",
            "start_date",
            "end_date",
            "approval_date",
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
        """
        Generate the payment plan for the loan instance.
        """
        calculator = PaymentPlanCalculator(obj)
        payment_plan = calculator.get_payment_status()
        return PaymentPlanSerializer(payment_plan, many=True).data
