import csv
import random

random.seed(727)

credit_types = [
    "Child Tax Credit",
    "Credit for Other Dependents",
    "Education Credit",
    "Foreign Tax Credit",
    "Retirement Savings Credit"
]

credit_records = []

credit_id = 4001

with open("TaxReturn.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        return_id = int(row["ReturnID"])
        total_credits = float(row["TotalNonrefundableCredits"])

        # If the return has no credits, create no TaxCredit rows
        if total_credits == 0:
            continue

        # Each return with credits will have between 1 and 2 credit records
        number_of_credits = random.randint(1, 2)

        selected_credit_types = random.sample(
            credit_types,
            number_of_credits
        )

        remaining_credits = total_credits

        for i in range(number_of_credits):

            credit_type = selected_credit_types[i]

            # Give the last credit record the remaining amount
            if i == number_of_credits - 1:
                amount = remaining_credits

            else:
                amount = round(
                    random.uniform(
                        remaining_credits * 0.30,
                        remaining_credits * 0.70
                    ),
                    2
                )

                remaining_credits = round(
                    remaining_credits - amount,
                    2
                )

            credit_records.append([
                credit_id,
                return_id,
                credit_type,
                round(amount, 2)
            ])

            credit_id += 1


with open("TaxCredit.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "CreditID",
        "ReturnID",
        "CreditType",
        "Amount"
    ])

    writer.writerows(credit_records)


print(
    f"Created TaxCredit.csv with "
    f"{len(credit_records)} tax credit records."
)