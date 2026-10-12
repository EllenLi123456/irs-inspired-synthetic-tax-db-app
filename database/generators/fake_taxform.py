import csv
import random

random.seed(727)

additional_forms = [
    "Schedule 1",
    "Schedule A",
    "Schedule B",
    "Schedule C",
    "Schedule D",
    "Schedule E"
]

tax_form_records = []

tax_form_id = 7001

with open("TaxReturn.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:

        return_id = int(row["ReturnID"])

        # Every return must include Form 1040
        tax_form_records.append([
            tax_form_id,
            return_id,
            "Form 1040"
        ])

        tax_form_id += 1

        # Randomly add 0 to 2 additional forms
        number_of_additional_forms = random.randint(0, 2)

        selected_forms = random.sample(
            additional_forms,
            number_of_additional_forms
        )

        for form_type in selected_forms:

            tax_form_records.append([
                tax_form_id,
                return_id,
                form_type
            ])

            tax_form_id += 1


with open("TaxForm.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
        "TaxFormID",
        "ReturnID",
        "FormType"
    ])

    writer.writerows(tax_form_records)


print(
    f"Created TaxForm.csv with "
    f"{len(tax_form_records)} tax form records."
)