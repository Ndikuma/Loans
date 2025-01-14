import locale  # noqa: F401
from datetime import date  # noqa: F401
from datetime import datetime, timedelta  # noqa: F401
from decimal import Decimal

from django.db import models
from django.utils import timezone  # noqa: F401
from django.utils.timezone import now  # noqa: F401
from django.utils.translation import gettext_lazy as _

from config.apps.authantification.models import User

from .utils import PaymentPlanCalculator


class Loan(models.Model):
    # Status Choices
    class Status(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        REPAID = "REPAID", _("Repaid")
        OVERDUE = "OVERDUE", _("Overdue")
        CANCELLED = "CANCELLED", _("Cancelled")

    # Payment Schedule Choices
    class PaymentSchedule(models.TextChoices):
        MONTHLY = "MONTHLY", _("Monthly")
        QUARTERLY = "QUARTERLY", _("Quarterly")
        ANNUALLY = "ANNUALLY", _("Annually")

    # Fields
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loan_set")
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    interest_rate = models.FloatField(default=10.5)
    duration_months = models.PositiveIntegerField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)  # Made required
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    payment_schedule = models.CharField(
        max_length=20,
        choices=PaymentSchedule.choices,
        default=PaymentSchedule.MONTHLY,
    )
    description = models.TextField(blank=True, null=True)  # Made required
    total_amount = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True
    )
    amount_paid = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True
    )
    late_payment_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    penalty_rate = models.FloatField(default=1.5)
    approval_date = models.DateField(blank=True, null=True)  # Made required
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.total_amount_to_pay()
        # Calculate end_date if not provided
        if not self.end_date:
            self.end_date = self.approval_date + timedelta(
                days=self.duration_months * 30
            )  # Approximate calculation for months

        # Calculate late payment fee based on penalty_rate and overdue duration (e.g., days overdue)
        if self.status == self.Status.OVERDUE:
            overdue_days = (timezone.now().date() - self.end_date).days
            self.late_payment_fee = max(
                Decimal("0.00"), Decimal(overdue_days * self.penalty_rate)
            )
        # Transfer amount to client wallet when loan approved
        if self.status == self.Status.IN_PROGRESS and self.approval_date:
            self._update_wallet_balance()

        # Call the parent save method
        super().save(*args, **kwargs)

    def _update_wallet_balance(self):
        """Add loan amount to the client's wallet when loan is approved."""
        try:
            wallet = self.client.wallet
            wallet.add_balance(self.amount)
        except Wallet.DoesNotExist:
            print(f"No wallet found for client {self.client.username}")

    def calculate_payment_plan(self):
        # Get the current wallet balance from the client object

        # Create an instance of the PaymentPlanCalculator
        calculator = PaymentPlanCalculator(
            amount=self.amount,
            interest_rate=self.interest_rate,
            duration_months=self.duration_months,
            start_date=self.start_date,
            payment_schedule=self.payment_schedule,
            client=self.client,
            amount_paid=self.amount_paid,
        )

        # Calculate the payment plan and update payment statuses
        calculator

        # Return the updated payment plan
        return calculator
        # Update the wallet balance after a payment is deducted
        self.client.wallet.balance = calculator.get_wallet_balance()

    def update_status(self):
        """
        Update the loan status based on payment progress and overdue conditions.
        """
        # Check if the loan is fully repaid
        if self.is_fully_repaid():
            self.status = self.Status.REPAID
        # Check if the loan is overdue
        elif self.is_overdue():
            self.status = self.Status.OVERDUE
        # If the loan is pending and some payment has been made, update the status to 'In Progress'
        elif self.status == self.Status.PENDING and self.amount_paid > 0:
            self.status = self.Status.IN_PROGRESS

        # Save the updated status to the database
        self.save()

    def total_amount_to_pay(self):
        """
        Calculate the total amount to be repaid, including interest.
        """
        # Calculate the monthly interest rate
        monthly_interest_rate = self.interest_rate / 12 / 100

        # Calculate the total interest over the loan duration
        total_interest = (
            self.amount * Decimal(monthly_interest_rate) * self.duration_months
        )

        # Calculate the total amount to be repaid (principal + interest)
        total_to_pay = self.amount + total_interest

        # Round the result to two decimal places
        return total_to_pay.quantize(Decimal("0.00"))

    def remaining_amount(self):
        """
        Calculate the remaining amount to be paid.
        """
        # Subtract the total amount paid from the total amount to be repaid
        remaining = self.total_amount_to_pay() - self.amount_paid

        # Ensure the remaining amount is not negative
        return max(remaining, Decimal("0.00"))

    def is_fully_repaid(self):
        """
        Check if the loan is fully repaid.
        """
        # The loan is fully repaid if the remaining amount is zero
        return self.remaining_amount() == Decimal("0.00")

    def is_overdue(self):
        """
        Check if the loan is overdue based on the current date and payment schedule.
        """
        # Calculate the expected number of payments based on the duration and start date
        elapsed_months = (timezone.now().date() - self.start_date).days // 30

        # Calculate the expected amount paid by now
        expected_amount_paid = (
            self.total_amount_to_pay() / self.duration_months
        ) * elapsed_months

        # Check if the actual amount paid is less than the expected amount
        return self.amount_paid < expected_amount_paid

    class Meta:
        # Order the records by the 'start_date' in descending order
        ordering = ["-start_date"]
        verbose_name = _("Loan")
        verbose_name_plural = _("Loans")
        indexes = [
            models.Index(fields=["client", "status"]),
        ]

    def __str__(self):
        return f"Loan for {self.client.username} - {self.amount} ({self.status})"


class Wallet(models.Model):
    class WalletType(models.TextChoices):
        STANDARD = "STANDARD", _("Standard")
        PREMIUM = "PREMIUM", _("Premium")
        BUSINESS = "BUSINESS", _("Business")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    wallet_type = models.CharField(
        max_length=20, choices=WalletType.choices, default=WalletType.STANDARD
    )
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    # Wallet settings are included here
    max_withdrawal_limit = models.DecimalField(
        max_digits=20, decimal_places=2, default=1000.00
    )
    notifications_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

    def add_balance(self, amount):
        """Add funds to the wallet."""
        if amount > 0:
            self.balance += amount
            self.save()

    def subtract_balance(self, amount):
        """Subtract funds from the wallet."""
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.save()

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")
