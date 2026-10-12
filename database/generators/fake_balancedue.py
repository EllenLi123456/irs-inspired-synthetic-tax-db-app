import csv
import random
from datetime import date, timedelta

random.seed(727)

balance_statuses = [
    "Unpaid",
    "Payment Plan",
    "Paid"
]

# Read ReturnIDs that already have refunds
refund_return_ids = set()

with open("Refund.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        refund_return_ids.add(
            int(row["ReturnID"])
        )


balance_due_records = []

balance_due_id = 6001

with open("TaxReturn.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        return_id = int(row["ReturnID"])
        total_tax = float(row["TotalTax"])

        # Skip returns that already have a refund
        if return_id in refund_return_ids:
            continue

        # Some remaining returns will have a balance due,
        # and some will have neither
        has_balance_due = random.choice([True, False])

        if not has_balance_due:
            continue

        amount_due = round(
            random.uniform(
                100,
                max(100, total_tax * 0.50)
            ),
            2
        )

        # Due date for 2025 individual tax returns
        due_date = date(2026, 4, 15)

        balance_status = random.choice(
            balance_statuses
        )

        balance_due_records.append([
            balance_due_id,
            return_id,
            amount_due,
            due_date,
            balance_status
        ])

        balance_due_id += 1


with open("BalanceDue.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "BalanceDueID",
        "ReturnID",
        "AmountDue",
        "DueDate",
        "BalanceStatus"
    ])

    writer.writerows(balance_due_records)


print(
    f"Created BalanceDue.csv with "
    f"{len(balance_due_records)} balance due records."
)