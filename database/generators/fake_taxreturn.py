import csv
import random
from datetime import date, timedelta

random.seed(727)

number_of_returns = 25

filing_statuses = [
    "Single",
    "MFJ",
    "MFS",
    "HOH",
    "QSS"
]

with open("TaxReturn.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "ReturnID",
        "TaxpayerID",
        "TaxYear",
        "FilingStatus",
        "FilingDate",
        "TotalIncome",
        "AdjustedGrossIncome",
        "TotalDeductions",
        "TaxableIncome",
        "TotalNonrefundableCredits",
        "TotalTax"
    ])

    for i in range(number_of_returns):

        return_id = 1001 + i

        # Connect this return to an existing taxpayer
        taxpayer_id = i + 1

        tax_year = 2025

        filing_status = random.choice(filing_statuses)

        # Generate a filing date between Jan 20 and Apr 15, 2026
        start_date = date(2026, 1, 20)
        end_date = date(2026, 4, 15)

        days_between = (end_date - start_date).days
        filing_date = start_date + timedelta(
            days=random.randint(0, days_between)
        )

        # Generate fake financial values
        total_income = random.randint(30000, 200000)

        adjustments = random.randint(0, 5000)

        adjusted_gross_income = max(
            0,
            total_income - adjustments
        )

        total_deductions = random.randint(1000, 30000)

        taxable_income = max(
            0,
            adjusted_gross_income - total_deductions
        )

        total_nonrefundable_credits = random.randint(0, 3000)

        # Simplified fake tax amount for database testing
        estimated_tax = taxable_income * random.uniform(0.08, 0.20)

        total_tax = max(
            0,
            estimated_tax - total_nonrefundable_credits
        )

        writer.writerow([
            return_id,
            taxpayer_id,
            tax_year,
            filing_status,
            filing_date,
            round(total_income, 2),
            round(adjusted_gross_income, 2),
            round(total_deductions, 2),
            round(taxable_income, 2),
            round(total_nonrefundable_credits, 2),
            round(total_tax, 2)
        ])

print(f"Created TaxReturn.csv with {number_of_returns} tax returns.")