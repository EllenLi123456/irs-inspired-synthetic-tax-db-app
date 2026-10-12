import csv
import random

random.seed(727)

income_types = [
    "Wages",
    "Interest",
    "Dividends",
    "Business Income",
    "Rental Income"
]

income_records = []

income_id = 2001

with open("TaxReturn.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        return_id = int(row["ReturnID"])
        total_income = float(row["TotalIncome"])

        # Each return will have between 1 and 3 income sources
        number_of_income_sources = random.randint(1, 3)

        selected_income_types = random.sample(
            income_types,
            number_of_income_sources
        )

        remaining_income = total_income

        for i in range(number_of_income_sources):

            income_type = selected_income_types[i]

            # Give the last income record all remaining income
            if i == number_of_income_sources - 1:
                amount = remaining_income

            else:
                amount = round(
                    random.uniform(
                        remaining_income * 0.20,
                        remaining_income * 0.70
                    ),
                    2
                )

                remaining_income = round(
                    remaining_income - amount,
                    2
                )

            income_records.append([
                income_id,
                return_id,
                income_type,
                round(amount, 2)
            ])

            income_id += 1


with open("IncomeRecord.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "IncomeID",
        "ReturnID",
        "IncomeType",
        "Amount"
    ])

    writer.writerows(income_records)


print(
    f"Created IncomeRecord.csv with "
    f"{len(income_records)} income records."
)