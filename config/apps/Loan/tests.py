from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from config.apps.authantification.models import User

from .models import Loan, Wallet, WalletActivity


class LoanModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.wallet = Wallet.objects.create(user=self.user)
        self.loan = Loan.objects.create(
            client=self.user,
            amount=Decimal("1000.00"),
            interest_rate=10.5,
            duration_months=12,
            approval_date=timezone.now(),
        )

    def test_loan_total_amount_to_pay(self):
        """Test total amount to pay calculation."""
        expected_total = Decimal("1105.00")  # 1000 + 5.25 * 12
        self.assertEqual(self.loan.total_amount_to_pay(), expected_total)

    def test_loan_remaining_amount(self):
        """Test remaining amount calculation."""
        self.loan.amount_paid = Decimal("500.00")
        self.loan.save()
        self.assertEqual(self.loan.remaining_amount(), Decimal("605.00"))

    #     def test_loan_status_update(self):
    #         """Test status update for fully repaid and overdue loans."""
    #         # Fully repaid loan
    #         self.loan.amount_paid = self.loan.total_amount_to_pay()
    #         self.loan.save()
    #         self.assertEqual(self.loan.status, Loan.Status.REPAID)

    # #         # Overdue loan
    #         self.loan.status = Loan.Status.IN_PROGRESS
    #         self.loan.end_date = timezone.now().date() - timezone.timedelta(days=1)
    #         self.loan.save()
    #         self.assertEqual(self.loan.status, Loan.Status.OVERDUE)

    # def test_wallet_creation_on_loan(self):
    #     """Test wallet creation when a loan is created."""
    #     new_user = User.objects.create_user(username="new1user", password="password123")
    #     Loan.objects.create(
    #         client=new_user,
    #         amount=Decimal("500.00"),
    #         interest_rate=10.0,
    #         duration_months=6,
    #         approval_date=timezone.now(),
    #     )
    #     self.assertTrue(Wallet.objects.filter(user=new_user).exists())

    def test_loan_end_date_calculation(self):
        """Test end date calculation based on approval date and duration."""
        expected_end_date = self.loan.approval_date + timezone.timedelta(days=365)
        self.assertEqual(self.loan.end_date, expected_end_date)


class WalletModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="walletuser", password="password123"
        )
        self.wallet = Wallet.objects.create(user=self.user, balance=Decimal("1000.00"))

    def test_wallet_add_balance(self):
        """Test adding balance to the wallet."""
        self.wallet.add_balance(Decimal("500.00"))
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("1500.00"))

    def test_wallet_subtract_balance(self):
        """Test subtracting balance from the wallet."""
        self.wallet.subtract_balance(Decimal("300.00"))
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("700.00"))

    # def test_wallet_insufficient_balance(self):
    #     """Test subtracting more than the available balance."""
    #     with self.assertRaises(ValueError):
    #         self.wallet.subtract_balance(Decimal("2000.00"))

    def test_wallet_activity_logging(self):
        """Test that wallet activities are logged correctly."""
        self.wallet.add_balance(Decimal("100.00"))
        self.wallet.subtract_balance(Decimal("50.00"))
        activities = WalletActivity.objects.filter(wallet=self.wallet)
        self.assertEqual(activities.count(), 2)
        self.assertEqual(activities.first().activity_type, "add")
        self.assertEqual(activities.last().activity_type, "subtract")


class WalletActivityModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="activityuser", password="password123"
        )
        self.wallet = Wallet.objects.create(user=self.user, balance=Decimal("500.00"))

    def test_log_activity(self):
        """Test logging a wallet activity."""
        WalletActivity.log_activity(self.wallet, "add", Decimal("200.00"))
        activity = WalletActivity.objects.last()
        self.assertEqual(activity.wallet, self.wallet)
        self.assertEqual(activity.activity_type, "add")
        self.assertEqual(activity.amount, Decimal("200.00"))
        self.assertIn("Activity: add", activity.description)
