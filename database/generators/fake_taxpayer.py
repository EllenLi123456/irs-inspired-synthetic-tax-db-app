from faker import Faker
import csv
import random

fake = Faker()

# Makes the generated data repeatable
Faker.seed(727)
random.seed(727)

number_of_taxpayers = 25

with open("Taxpayer.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Header row
    writer.writerow([
        "TaxpayerID",
        "FirstName",
        "MiddleInitial",
        "LastName",
        "StreetAddress",
        "ApartmentNumber",
        "City",
        "State",
        "ZIPCode"
    ])

    for i in range(number_of_taxpayers):
        taxpayer_id = i + 1
        first_name = fake.first_name()
        middle_initial = random.choice([
            "",
            fake.random_uppercase_letter()
        ])
        last_name = fake.last_name()
        street_address = fake.street_address().replace("\n", " ")

        # Some taxpayers have apartments, some do not
        apartment_number = random.choice([
            "",
            "",
            "",
            f"Apt {random.randint(1, 999)}"
        ])

        city = fake.city()
        state = fake.state_abbr()
        zip_code = fake.zipcode()

        writer.writerow([
            taxpayer_id,
            first_name,
            middle_initial,
            last_name,
            street_address,
            apartment_number,
            city,
            state,
            zip_code
        ])

print(f"Created Taxpayer.csv with {number_of_taxpayers} taxpayers.")