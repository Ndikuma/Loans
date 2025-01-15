from decimal import Decimal

from django.db import models
from django.utils import timezone
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
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    payment_schedule = models.CharField(
        max_length=20, choices=PaymentSchedule.choices, default=PaymentSchedule.MONTHLY
    )
    description = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(
        max_digits=20, default=Decimal("0.00"), decimal_places=2, null=True, blank=True
    )
    amount_paid = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True
    )
    late_payment_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    penalty_rate = models.FloatField(default=1.5)
    approval_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_amount = self.total_amount_to_pay()
        if not self.end_date:
            from dateutil.relativedelta import relativedelta

            self.end_date = self.approval_date + relativedelta(
                months=self.duration_months
            )

        if self.status == self.Status.OVERDUE:
            overdue_days = (timezone.now().date() - self.end_date).days
            self.late_payment_fee = max(
                Decimal("0.00"), Decimal(overdue_days * self.penalty_rate)
            )

        if self.status == self.Status.IN_PROGRESS and self.approval_date:
            self._update_wallet_balance()
            # self.calculate_payment_plan().get_payment_status()

        super().save(*args, **kwargs)

    def _update_wallet_balance(self):
        """Add loan amount to the client's wallet when loan is approved."""
        try:
            wallet = self.client.wallet
            wallet.add_balance(self.amount)
        except Wallet.DoesNotExist:
            print(f"No wallet found for client {self.client.username}")

    def calculate_payment_plan(self):
        """Calculate and return the payment plan."""
        calculator = PaymentPlanCalculator(
            amount=self.amount,
            interest_rate=self.interest_rate,
            duration_months=self.duration_months,
            start_date=self.start_date,
            payment_schedule=self.payment_schedule,
            client=self.client,
            amount_paid=self.amount_paid,
        )
        return calculator

    def update_status(self):
        """Update loan status based on progress and overdue conditions."""
        if self.is_fully_repaid():
            self.status = self.Status.REPAID
        elif self.is_overdue():
            self.status = self.Status.OVERDUE
        elif self.status == self.Status.PENDING and self.amount_paid > 0:
            self.status = self.Status.IN_PROGRESS

        self.save()

    def total_amount_to_pay(self):
        """Calculate total amount to repay, including interest."""
        monthly_interest_rate = self.interest_rate / 12 / 100
        total_interest = (
            self.amount * Decimal(monthly_interest_rate) * self.duration_months
        )
        return (self.amount + total_interest).quantize(Decimal("0.00"))

    def remaining_amount(self):
        """Calculate remaining amount to be paid."""
        total = self.total_amount_to_pay()  # Assuming this returns a number
        paid = self.amount_paid  # Assuming this is a number as well
        if total is not None and paid is not None:
            return Decimal(total - paid)
        return Decimal(0)

    def is_fully_repaid(self):
        """Check if the loan is fully repaid."""
        return self.remaining_amount() == Decimal("0.00")

    def is_overdue(self):
        """Check if the loan is overdue."""
        if not self.start_date or self.duration_months <= 0:
            return False  # Or raise an exception if it's invalid data

        # elapsed_months = (timezone.now().date() - self.start_date).days // 30
        # expected_amount_paid = (self.total_amount_to_pay() / self.duration_months) * elapsed_months

        # return self.amount_paid < expected_amount_paid

    class Meta:
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
    max_withdrawal_limit = models.DecimalField(
        max_digits=20, decimal_places=2, default=1000.00
    )
    notifications_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

    def add_balance(self, amount: Decimal):
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
