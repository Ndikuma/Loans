from datetime import datetime, timedelta
from decimal import Decimal


class PaymentPlanCalculator:
    def __init__(
        self,
        amount,
        interest_rate,
        duration_months,
        start_date,
        payment_schedule,
        client,
        amount_paid,
    ):
        self.amount = Decimal(amount)
        self.amount_paid = Decimal(amount_paid)
        self.interest_rate = Decimal(interest_rate)
        self.duration_months = duration_months
        self.start_date = start_date
        self.payment_schedule = payment_schedule
        self.client = client  # Client object with wallet
        self.payments_made = []  # Track payments

    def calculate_payment_plan(self):
        total_amount = self.amount + (self.amount * self.interest_rate / 100)

        if self.payment_schedule == "MONTHLY":
            return self._generate_plan(total_amount, 30, "Month", self.duration_months)
        elif self.payment_schedule == "QUARTERLY":
            return self._generate_plan(
                total_amount, 90, "Quarter", self.duration_months // 3
            )
        elif self.payment_schedule == "ANNUALLY":
            return self._generate_plan(
                total_amount, 365, "Year", self.duration_months // 12
            )

    def _generate_plan(self, total_amount, days_in_period, period_name, periods):
        payment_amount = total_amount / periods
        return [
            {
                "period": f"{period_name} {i + 1}",
                "due_date": self.start_date + timedelta(days=days_in_period * i),
                "payment_amount": round(payment_amount, 2),
                "status": "unpaid",
            }
            for i in range(1, periods + 1)
        ]

    def deduct_payment(self, current_date=None):
        """Deduct payments from the client's wallet and check payment for each period."""
        current_date = current_date or datetime.now().date()
        payment_plan = self.calculate_payment_plan()

        for scheduled_payment in payment_plan:
            if scheduled_payment["status"] == "unpaid":
                if current_date >= scheduled_payment["due_date"]:
                    # Check wallet balance for the current payment
                    if (
                        self.client.wallet.balance
                        >= scheduled_payment["payment_amount"]
                    ):
                        self.client.wallet.subtract_balance(
                            scheduled_payment["payment_amount"]
                        )
                        self.amount_paid += scheduled_payment["payment_amount"]
                        scheduled_payment["status"] = "paid"
                        self.payments_made.append(
                            {
                                "payment_date": current_date,
                                "amount": scheduled_payment["payment_amount"],
                            }
                        )
                    else:
                        # Mark as overdue if insufficient funds
                        scheduled_payment["status"] = "overdue"

        # Update the status of payments based on the total paid
        for scheduled_payment in payment_plan:
            if self.amount_paid >= scheduled_payment["payment_amount"]:
                scheduled_payment["status"] = "paid"

        return payment_plan

    def get_payment_status(self):
        """Return the status of all scheduled payments."""
        return [
            {
                "period": payment["period"],
                "due_date": payment["due_date"].strftime("%Y-%m-%d"),
                "payment_amount": payment["payment_amount"],
                "status": payment["status"],
            }
            for payment in self.deduct_payment()
        ]

    def get_wallet_balance(self):
        """Return the client's wallet balance."""
        return round(self.client.wallet.balance, 2)

    def get_total_paid(self):
        """Return the total amount paid."""
        return round(self.amount_paid, 2)
