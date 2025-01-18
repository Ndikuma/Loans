from datetime import datetime, timedelta
from decimal import Decimal


class PaymentPlanCalculator:
    def __init__(self, loan):
        """
        Initialize the PaymentPlanCalculator with a Loan instance.
        """
        self.loan = loan
        self.amount = loan.amount
        self.interest_rate = loan.interest_rate
        self.duration_months = loan.duration_months
        self.start_date = loan.start_date
        self.payment_schedule = loan.payment_schedule
        self.client = loan.client
        self.amount_paid = loan.amount_paid
        self.late_payment_fee_per_day = Decimal(loan.penalty_rate)

    def calculate_payment_plan(self):
        """
        Calculate the payment plan based on the loan's details.
        Only proceed if the loan status is IN_PROGRESS.
        """
        if self.loan.status != self.loan.Status.IN_PROGRESS:
            raise ValueError(
                "Payment plan can only be calculated for loans in IN_PROGRESS status."
            )

        total_amount = self.loan.total_amount_to_pay()
        if self.payment_schedule == self.loan.PaymentSchedule.MONTHLY:
            return self._generate_plan(total_amount, 30, "Month", self.duration_months)
        elif self.payment_schedule == self.loan.PaymentSchedule.QUARTERLY:
            return self._generate_plan(
                total_amount, 90, "Quarter", self.duration_months // 3
            )
        elif self.payment_schedule == self.loan.PaymentSchedule.ANNUALLY:
            return self._generate_plan(
                total_amount, 365, "Year", self.duration_months // 12
            )

    def _generate_plan(self, total_amount, days_in_period, period_name, periods):
        """
        Generate a detailed payment plan.
        """
        payment_amount = total_amount / periods
        plan = []
        for i in range(1, periods + 1):
            due_date = self.start_date + timedelta(days=days_in_period * i)
            plan.append(
                {
                    "period": f"{period_name} {i}",
                    "due_date": due_date,
                    "payment_amount": round(payment_amount, 2),
                    "amount_paid": Decimal(0),
                    "status": "unpaid",
                    "overdue_days": 0,
                    "late_payment_fee": Decimal(0),
                }
            )
        return plan

    def deduct_payment(self):
        """
        Deduct payments and apply late fees if applicable.
        Only proceed if the loan status is IN_PROGRESS.
        """
        current_date = datetime.now().date()  # Get the current date
        payment_plan = self.calculate_payment_plan()  # Get the payment plan
        for payment in payment_plan:
            if self.loan.is_fully_repaid():
                payment["status"] == "paid"
            if self.loan.is_overdue():
                payment["status"] = "overdue"

            # Check if the payment is overdue and not already paid
            if (
                current_date > payment["due_date"]
                and payment["status"] == "unpaid"
                and self.loan.total_amount <= self.loan.amount_paid
            ):
                overdue_days = max(0, (current_date - payment["due_date"]).days)
                payment["overdue_days"] = overdue_days
                payment["late_payment_fee"] = (
                    self.late_payment_fee_per_day * overdue_days
                )
                self.loan.late_payment_fee = (
                    self.loan.late_payment_fee or Decimal(0)
                ) + payment["late_payment_fee"]
                self.loan.save()
                payment["status"] = "overdue"  # Update the status to "overdue"

            if payment["status"] == "unpaid" or payment["status"] == "paid":
                # If the payment is marked as paid or unpaid, remove overdue_days and late_payment_fee if not applicable
                payment.pop("overdue_days", None)
                payment.pop("late_payment_fee", None)

            if payment["status"] == "unpaid" and current_date > payment["due_date"]:
                if self.client.wallet.balance >= payment["payment_amount"]:
                    # Deduct the payment amount from the client's wallet
                    self.client.wallet.subtract_balance(payment["payment_amount"])
                    self.client.wallet.save()

                    # Update the loan's amount_paid
                    self.loan.amount_paid = (
                        self.loan.amount_paid or Decimal(0)
                    ) + payment["payment_amount"]
                    self.loan.save()
                    # Update the payment record
                    payment["amount_paid"] = payment["payment_amount"]
                    payment["status"] = "paid"
                else:
                    # If the client can't pay, mark as overdue
                    payment["status"] = "overdue"

        return payment_plan

    def get_payment_status(self):
        """
        Retrieve the payment status for all scheduled payments.
        Display a message if the loan status is not IN_PROGRESS.
        """
        if self.loan.status != self.loan.Status.IN_PROGRESS:
            # Display the message and return an empty status list
            print(
                "Payment status can only be retrieved for loans in IN_PROGRESS status."
            )
            return []

        payment_status = []
        for payment in self.deduct_payment():
            if payment["status"] == "paid" or payment["status"] == "unpaid":
                # Remove keys for overdue days and late payment fee if payment is already paid
                payment.pop("overdue_days", None)
                payment.pop("late_payment_fee", None)

            payment_status.append(
                {
                    "period": payment["period"],
                    "due_date": payment["due_date"].strftime("%Y-%m-%d"),
                    "payment_amount": payment["payment_amount"],
                    "amount_paid": payment["amount_paid"],
                    "status": payment["status"],
                    # Only include overdue_days and late_payment_fee if they exist
                    **(
                        {"overdue_days": payment["overdue_days"]}
                        if "overdue_days" in payment
                        else {}
                    ),
                    **(
                        {"late_payment_fee": payment["late_payment_fee"]}
                        if "late_payment_fee" in payment
                        else {}
                    ),
                }
            )

        return payment_status
