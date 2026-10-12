import csv
import random

random.seed(727)

deduction_types = [
    "Standard Deduction",
    "Medical Expenses",
    "State and Local Taxes",
    "Mortgage Interest",
    "Charitable Contributions"
]

deduction_records = []

deduction_id = 3001

with open("TaxReturn.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        return_id = int(row["ReturnID"])
        total_deductions = float(row["TotalDeductions"])

        # Each return will have between 1 and 3 deduction records
        number_of_deductions = random.randint(1, 3)

        selected_deduction_types = random.sample(
            deduction_types,
            number_of_deductions
        )

        remaining_deductions = total_deductions

        for i in range(number_of_deductions):

            deduction_type = selected_deduction_types[i]

            # Give the last deduction record the remaining amount
            if i == number_of_deductions - 1:
                amount = remaining_deductions

            else:
                amount = round(
                    random.uniform(
                        remaining_deductions * 0.20,
                        remaining_deductions * 0.70
                    ),
                    2
                )

                remaining_deductions = round(
                    remaining_deductions - amount,
                    2
                )

            deduction_records.append([
                deduction_id,
                return_id,
                deduction_type,
                round(amount, 2)
            ])

            deduction_id += 1


with open("Deduction.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "DeductionID",
        "ReturnID",
        "DeductionType",
        "Amount"
    ])

    writer.writerows(deduction_records)


print(
    f"Created Deduction.csv with "
    f"{len(deduction_records)} deduction records."
)