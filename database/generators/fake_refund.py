import csv
import random
from datetime import date, timedelta

random.seed(727)

refund_statuses = [
    "Pending",
    "Approved",
    "Issued"
]

refund_records = []

refund_id = 5001

with open("TaxReturn.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        return_id = int(row["ReturnID"])
        total_tax = float(row["TotalTax"])

        # Randomly decide whether this return receives a refund
        has_refund = random.choice([True, False])

        if not has_refund:
            continue

        # Generate a reasonable fake refund amount
        refund_amount = round(
            random.uniform(100, max(100, total_tax * 0.50)),
            2
        )

        refund_status = random.choice(refund_statuses)

        # Generate refund date after filing date
        filing_date = date.fromisoformat(row["FilingDate"])

        refund_date = filing_date + timedelta(
            days=random.randint(7, 45)
        )

        refund_records.append([
            refund_id,
            return_id,
            refund_amount,
            refund_date,
            refund_status
        ])

        refund_id += 1


with open("Refund.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "RefundID",
        "ReturnID",
        "RefundAmount",
        "RefundDate",
        "RefundStatus"
    ])

    writer.writerows(refund_records)


print(
    f"Created Refund.csv with "
    f"{len(refund_records)} refund records."
)