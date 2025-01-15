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
        amount_paid=None,
        late_payment_fee_per_day=Decimal(5),  # Late payment fee per day
    ):
        self.amount = Decimal(amount)
        self.amount_paid = Decimal(amount_paid or 0)
        self.interest_rate = Decimal(interest_rate)
        self.duration_months = duration_months
        self.start_date = start_date
        self.payment_schedule = payment_schedule
        self.client = client  # Client object with wallet
        self.payments_made = []  # Track payments
        self.late_payment_fee_per_day = late_payment_fee_per_day  # Fee per day of delay

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
        plan = []
        for i in range(1, periods + 1):
            plan.append(
                {
                    "period": f"{period_name} {i}",
                    "due_date": self.start_date + timedelta(days=days_in_period * i),
                    "payment_amount": round(payment_amount, 2),
                    "amount_paid": Decimal(0),  # Track partial payments
                    "status": "unpaid",
                    "overdue_days": 0,  # Track overdue days
                    "late_payment_fee": Decimal(0),  # Track late payment fee
                }
            )
        return plan

    def deduct_payment(self):
        """Deduct payments from the client's wallet and check payment for each period."""
        current_date = datetime.now().date()
        payment_plan = self.calculate_payment_plan()

        for i, scheduled_payment in enumerate(payment_plan):
            payment_amount = scheduled_payment["payment_amount"]
            if i == 0:
                if payment_amount <= self.amount_paid:
                    scheduled_payment["status"] = "paid"
                if current_date <= scheduled_payment["due_date"]:
                    scheduled_payment["status"] = "overdue"

            if scheduled_payment["status"] == "unpaid":
                if current_date >= scheduled_payment["due_date"]:
                    # Check wallet balance for the current payment
                    payment_amount = scheduled_payment["payment_amount"] * i
                    if payment_amount <= self.amount_paid:
                        scheduled_payment["status"] = "paid"

                    if self.client.wallet.balance >= payment_amount:
                        # Deduct partial or full payment
                        self.client.wallet.subtract_balance(payment_amount)
                        scheduled_payment["amount_paid"] += payment_amount
                        self.amount_paid += payment_amount

                        self.payments_made.append(
                            {
                                "payment_date": scheduled_payment["due_date"],
                                "amount": payment_amount,
                            }
                        )

                    # After deducting, check if the full amount is paid
                    if (
                        scheduled_payment["amount_paid"]
                        >= scheduled_payment["payment_amount"]
                    ):
                        scheduled_payment["status"] = "paid"
                    else:
                        scheduled_payment["status"] = (
                            "unpaid"  # If not fully paid, mark as unpaid
                        )
                    if current_date >= scheduled_payment["due_date"]:
                        scheduled_payment["status"] = "overdue"

                # If overdue, calculate overdue days and apply late fee
                if current_date > scheduled_payment["due_date"]:
                    scheduled_payment["overdue_days"] = (
                        current_date - scheduled_payment["due_date"]
                    ).days
                    if scheduled_payment["overdue_days"] > 0:
                        # Apply late payment fee for each overdue day
                        scheduled_payment["late_payment_fee"] = (
                            scheduled_payment["overdue_days"]
                            * self.late_payment_fee_per_day
                        )
                        self.client.wallet.subtract_balance(
                            scheduled_payment["late_payment_fee"]
                        )

            # After checking each payment, mark status as paid if fully paid
            if scheduled_payment["amount_paid"] >= scheduled_payment["payment_amount"]:
                scheduled_payment["status"] = "paid"
            elif scheduled_payment["amount_paid"] > 0:
                scheduled_payment["status"] = "partial"

        return payment_plan

    def get_payment_status(self):
        """Return the status of all scheduled payments."""
        payment_status = []
        for payment in self.deduct_payment():
            payment_status.append(
                {
                    "period": payment["period"],
                    "due_date": payment["due_date"].strftime("%Y-%m-%d"),
                    "payment_amount": payment["payment_amount"],
                    "amount_paid": payment["amount_paid"],
                    "status": payment["status"],
                    "overdue_days": payment["overdue_days"],
                    "late_payment_fee": payment["late_payment_fee"],
                }
            )
        return payment_status

    def get_wallet_balance(self):
        """Return the client's wallet balance."""
        return round(self.client.wallet.balance, 2)

    def get_total_paid(self):
        """Return the total amount paid."""
        return round(self.amount_paid, 2)

    def get_payments_made(self):
        """Return a list of all payments made by the client."""
        return self.payments_made
