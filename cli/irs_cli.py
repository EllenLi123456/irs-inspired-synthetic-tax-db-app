import os

import mysql.connector
from tabulate import tabulate


# Display taxpayer records as a table
def display_taxpayers(taxpayers):

    headers = [
        "Taxpayer ID",
        "First Name",
        "MI",
        "Last Name",
        "Street Address",
        "Apartment",
        "City",
        "State",
        "ZIP Code"
    ]

    print(
        tabulate(
            taxpayers,
            headers=headers,
            tablefmt="grid"
        )
    )


# READ 1: View all taxpayers
def view_all_taxpayers(cursor):

    print("\n👥  View All Taxpayers")

    cursor.execute(
        """
        SELECT *
        FROM Taxpayer
        ORDER BY TaxpayerID
        """
    )

    taxpayers = cursor.fetchall()

    if taxpayers:
        display_taxpayers(taxpayers)
    else:
        print("❌  No taxpayers found.")


# READ 2: Find taxpayer by ID
def find_taxpayer(cursor):

    print("\n🔍  Find a Taxpayer")

    taxpayer_id = input(
        "Enter Taxpayer ID (0 to return to menu): "
    )

    if taxpayer_id == "0":
        print("↩️  Search canceled.")
        return

    cursor.execute(
        """
        SELECT *
        FROM Taxpayer
        WHERE TaxpayerID = %s
        """,
        (taxpayer_id,)
    )

    taxpayer = cursor.fetchone()

    if taxpayer:
        print("\n✅  Taxpayer found:")
        display_taxpayers([taxpayer])
    else:
        print("❌  Taxpayer not found.")


# CREATE: Add a new taxpayer
def add_taxpayer(cursor, connection):

    print("\n➕  Add a New Taxpayer")
    print("Press Enter to skip an optional field.")
    print("Enter 0 at any time to cancel.")

    taxpayer_id = input("Taxpayer ID: ")
    if taxpayer_id == "0":
        print("↩️  Add taxpayer canceled.")
        return

    first_name = input("First Name: ")
    if first_name == "0":
        print("↩️  Add taxpayer canceled.")
        return

    middle_initial = input("Middle Initial: ")
    if middle_initial == "0":
        print("↩️  Add taxpayer canceled.")
        return

    last_name = input("Last Name: ")
    if last_name == "0":
        print("↩️  Add taxpayer canceled.")
        return

    street_address = input("Street Address: ")
    if street_address == "0":
        print("↩️  Add taxpayer canceled.")
        return

    apartment_number = input("Apartment Number: ")
    if apartment_number == "0":
        print("↩️  Add taxpayer canceled.")
        return

    city = input("City: ")
    if city == "0":
        print("↩️  Add taxpayer canceled.")
        return

    state = input("State: ")
    if state == "0":
        print("↩️  Add taxpayer canceled.")
        return

    zip_code = input("ZIP Code: ")
    if zip_code == "0":
        print("↩️  Add taxpayer canceled.")
        return

    # Convert skipped optional fields to NULL
    if middle_initial == "":
        middle_initial = None
    else:
        middle_initial = middle_initial.upper()

    if apartment_number == "":
        apartment_number = None

    state = state.upper()

    # Review, validate, and correct taxpayer information
    while True:

        validation_errors = []

        if taxpayer_id == "":
            validation_errors.append(
                "Taxpayer ID is required."
            )

        if first_name == "":
            validation_errors.append(
                "First Name is required."
            )

        if last_name == "":
            validation_errors.append(
                "Last Name is required."
            )

        if street_address == "":
            validation_errors.append(
                "Street Address is required."
            )

        if city == "":
            validation_errors.append(
                "City is required."
            )

        if state == "":
            validation_errors.append(
                "State is required."
            )

        if zip_code == "":
            validation_errors.append(
                "ZIP Code is required."
            )

        # Check Taxpayer ID
        if taxpayer_id != "":

            if not taxpayer_id.isdigit():
                validation_errors.append(
                    "Taxpayer ID must contain numbers only."
                )

            else:
                cursor.execute(
                    """
                    SELECT TaxpayerID
                    FROM Taxpayer
                    WHERE TaxpayerID = %s
                    """,
                    (taxpayer_id,)
                )

                existing_taxpayer = cursor.fetchone()

                if existing_taxpayer:
                    validation_errors.append(
                        "Taxpayer ID already exists."
                    )

        # Check Middle Initial
        if middle_initial is not None:

            if len(middle_initial) != 1:
                validation_errors.append(
                    "Middle Initial must be one letter."
                )

        # Check State
        if state != "":

            if (
                len(state) != 2
                or not state.isalpha()
            ):
                validation_errors.append(
                    "State must be two letters, such as CA."
                )

        # Check ZIP Code
        if zip_code != "":

            valid_zip = (
                len(zip_code) == 5
                and zip_code.isdigit()
            )

            valid_zip_plus_four = (
                len(zip_code) == 10
                and zip_code[:5].isdigit()
                and zip_code[5] == "-"
                and zip_code[6:].isdigit()
            )

            if (
                not valid_zip
                and not valid_zip_plus_four
            ):
                validation_errors.append(
                    "ZIP Code must be 5 digits or ZIP+4."
                )

        # Display review information as a table
        taxpayer_review = [
            (
                taxpayer_id,
                first_name,
                middle_initial,
                last_name,
                street_address,
                apartment_number,
                city,
                state,
                zip_code
            )
        ]

        print("\n📋  Review Taxpayer Information")
        display_taxpayers(taxpayer_review)

        if validation_errors:

            print(
                "\n⚠️  Please correct the following:"
            )

            for error in validation_errors:
                print("-", error)

        print("\nIs this information correct?")
        print("1.  ✅  Yes")
        print("2.  ✏️  No, correct a field")
        print("0.  ↩️  Cancel")

        review_choice = input(
            "Choose an option: "
        )

        if review_choice == "1":

            if validation_errors:

                print(
                    "❌  Cannot add taxpayer until "
                    "the errors are corrected."
                )

                continue

            cursor.execute(
                """
                INSERT INTO Taxpayer
                (
                    TaxpayerID,
                    FirstName,
                    MiddleInitial,
                    LastName,
                    StreetAddress,
                    ApartmentNumber,
                    City,
                    State,
                    ZIPCode
                )
                VALUES
                (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
                """,
                (
                    taxpayer_id,
                    first_name,
                    middle_initial,
                    last_name,
                    street_address,
                    apartment_number,
                    city,
                    state,
                    zip_code
                )
            )

            connection.commit()

            print(
                "\n✅  Taxpayer added successfully."
            )

            # Show the new taxpayer
            cursor.execute(
                """
                SELECT *
                FROM Taxpayer
                WHERE TaxpayerID = %s
                """,
                (taxpayer_id,)
            )

            new_taxpayer = cursor.fetchone()

            print("\n📋  New Taxpayer Record:")
            display_taxpayers([new_taxpayer])

            return

        elif review_choice == "0":

            print(
                "↩️  Add taxpayer canceled."
            )

            return

        elif review_choice == "2":

            print(
                "\n✏️  Which field would you like "
                "to correct?"
            )

            print("1. Taxpayer ID")
            print("2. First Name")
            print("3. Middle Initial")
            print("4. Last Name")
            print("5. Street Address")
            print("6. Apartment Number")
            print("7. City")
            print("8. State")
            print("9. ZIP Code")
            print("0.  ↩️  Cancel")

            field_choice = input(
                "Choose a field: "
            )

            if field_choice == "0":

                print(
                    "↩️  Add taxpayer canceled."
                )

                return

            elif field_choice == "1":

                taxpayer_id = input(
                    "New Taxpayer ID: "
                )

            elif field_choice == "2":

                first_name = input(
                    "New First Name: "
                )

            elif field_choice == "3":

                middle_initial = input(
                    "New Middle Initial "
                    "(press Enter for none): "
                )

                if middle_initial == "":
                    middle_initial = None
                else:
                    middle_initial = (
                        middle_initial.upper()
                    )

            elif field_choice == "4":

                last_name = input(
                    "New Last Name: "
                )

            elif field_choice == "5":

                street_address = input(
                    "New Street Address: "
                )

            elif field_choice == "6":

                apartment_number = input(
                    "New Apartment Number "
                    "(press Enter for none): "
                )

                if apartment_number == "":
                    apartment_number = None

            elif field_choice == "7":

                city = input(
                    "New City: "
                )

            elif field_choice == "8":

                state = input(
                    "New State: "
                )

                state = state.upper()

            elif field_choice == "9":

                zip_code = input(
                    "New ZIP Code: "
                )

            else:

                print(
                    "❌  Invalid field choice."
                )

        else:

            print(
                "❌  Invalid option. "
                "Please choose 1, 2, or 0."
            )


# UPDATE: Update a taxpayer
def update_taxpayer(cursor, connection):

    print("\n✏️  Update a Taxpayer")

    update_taxpayer_id = input(
        "Enter Taxpayer ID to update "
        "(0 to cancel): "
    )

    if update_taxpayer_id == "0":

        print(
            "↩️  Update taxpayer canceled."
        )

        return

    cursor.execute(
        """
        SELECT *
        FROM Taxpayer
        WHERE TaxpayerID = %s
        """,
        (update_taxpayer_id,)
    )

    taxpayer = cursor.fetchone()

    if not taxpayer:

        print(
            "❌  Taxpayer not found."
        )

        return

    print("\n✅  Taxpayer found:")
    display_taxpayers([taxpayer])

    updates_made = []

    # Convert tuple to list so local values can change
    taxpayer_data = list(taxpayer)

    field_map = {
        "1": ("FirstName", 1),
        "2": ("MiddleInitial", 2),
        "3": ("LastName", 3),
        "4": ("StreetAddress", 4),
        "5": ("ApartmentNumber", 5),
        "6": ("City", 6),
        "7": ("State", 7),
        "8": ("ZIPCode", 8)
    }

    while True:

        print(
            "\n✏️  Which field would you like "
            "to update?"
        )

        print("1. First Name")
        print("2. Middle Initial")
        print("3. Last Name")
        print("4. Street Address")
        print("5. Apartment Number")
        print("6. City")
        print("7. State")
        print("8. ZIP Code")
        print("0.  ↩️  Cancel")

        field_choice = input(
            "Choose a field: "
        )

        if field_choice == "0":

            connection.rollback()

            print(
                "↩️  Update taxpayer canceled."
            )

            return

        if field_choice not in field_map:

            print(
                "❌  Invalid field choice."
            )

            continue

        column_name, column_index = (
            field_map[field_choice]
        )

        old_value = taxpayer_data[
            column_index
        ]

        new_value = input(
            "Enter new value: "
        )

        # Handle Middle Initial
        if column_name == "MiddleInitial":

            if new_value == "":
                new_value = None
            else:
                new_value = new_value.upper()

            if (
                new_value is not None
                and len(new_value) != 1
            ):

                print(
                    "❌  Middle Initial must "
                    "be one letter."
                )

                continue

        # Handle Apartment Number
        if column_name == "ApartmentNumber":

            if new_value == "":
                new_value = None

        # Check required fields
        if column_name in [
            "FirstName",
            "LastName",
            "StreetAddress",
            "City",
            "State",
            "ZIPCode"
        ]:

            if new_value == "":

                print(
                    "❌ ",
                    column_name,
                    "cannot be empty."
                )

                continue

        # Validate State
        if column_name == "State":

            new_value = new_value.upper()

            if (
                len(new_value) != 2
                or not new_value.isalpha()
            ):

                print(
                    "❌  State must be two "
                    "letters, such as CA."
                )

                continue

        # Validate ZIP Code
        if column_name == "ZIPCode":

            valid_zip = (
                len(new_value) == 5
                and new_value.isdigit()
            )

            valid_zip_plus_four = (
                len(new_value) == 10
                and new_value[:5].isdigit()
                and new_value[5] == "-"
                and new_value[6:].isdigit()
            )

            if (
                not valid_zip
                and not valid_zip_plus_four
            ):

                print(
                    "❌  ZIP Code must be "
                    "5 digits or ZIP+4."
                )

                continue

        print("\n📋  Review Update")
        print(
            "Taxpayer ID:",
            update_taxpayer_id
        )
        print(
            "Field:",
            column_name
        )
        print(
            "Old Value:",
            old_value
        )
        print(
            "New Value:",
            new_value
        )

        print("\n1.  ✅  Confirm Change")
        print("0.  ↩️  Cancel")

        confirm = input(
            "Choose an option: "
        )

        if confirm == "1":

            sql = f"""
                UPDATE Taxpayer
                SET {column_name} = %s
                WHERE TaxpayerID = %s
            """

            cursor.execute(
                sql,
                (
                    new_value,
                    update_taxpayer_id
                )
            )

            updates_made.append(
                f"{column_name}: "
                f"{old_value} -> {new_value}"
            )

            taxpayer_data[
                column_index
            ] = new_value

            print(
                "✅  Change saved."
            )

        else:

            print(
                "↩️  This change was canceled."
            )

        print(
            "\nWould you like to update "
            "another field?"
        )

        print("1.  ✅  Yes")
        print("2.  🏁  No, finish update")
        print("0.  ↩️  Cancel all updates")

        continue_choice = input(
            "Choose an option: "
        )

        if continue_choice == "1":

            continue

        elif continue_choice == "2":

            if updates_made:

                connection.commit()

                print(
                    "\n✅  Updated Taxpayer "
                    + update_taxpayer_id
                    + ": "
                    + ", ".join(updates_made)
                )

                # Show updated taxpayer
                cursor.execute(
                    """
                    SELECT *
                    FROM Taxpayer
                    WHERE TaxpayerID = %s
                    """,
                    (update_taxpayer_id,)
                )

                updated_taxpayer = (
                    cursor.fetchone()
                )

                print(
                    "\n📋  Updated Taxpayer Record:"
                )

                display_taxpayers(
                    [updated_taxpayer]
                )

            else:

                print(
                    "ℹ️  No changes were made."
                )

            return

        elif continue_choice == "0":

            connection.rollback()

            print(
                "↩️  All updates canceled."
            )

            return

        else:

            print(
                "❌  Invalid option. "
                "Returning to update menu."
            )


# DELETE: Delete a taxpayer
def delete_taxpayer(cursor, connection):

    print("\n🗑️  Delete a Taxpayer")

    delete_taxpayer_id = input(
        "Enter Taxpayer ID to delete "
        "(0 to cancel): "
    )

    if delete_taxpayer_id == "0":

        print(
            "↩️  Delete taxpayer canceled."
        )

        return

    cursor.execute(
        """
        SELECT *
        FROM Taxpayer
        WHERE TaxpayerID = %s
        """,
        (delete_taxpayer_id,)
    )

    taxpayer = cursor.fetchone()

    if not taxpayer:

        print(
            "❌  Taxpayer not found."
        )

        return

    print("\n✅  Taxpayer found:")
    display_taxpayers([taxpayer])

    # Check for related tax returns
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM TaxReturn
        WHERE TaxpayerID = %s
        """,
        (delete_taxpayer_id,)
    )

    tax_return_count = cursor.fetchone()[0]

    if tax_return_count > 0:

        print(
            "\n⚠️  Cannot delete Taxpayer "
            + delete_taxpayer_id
            + "."
        )

        print(
            "This taxpayer has "
            + str(tax_return_count)
            + " related tax return record(s)."
        )

        return

    print(
        "\n⚠️  WARNING: This will permanently "
        "delete this taxpayer."
    )

    print("1.  🗑️  Confirm Delete")
    print("0.  ↩️  Cancel")

    delete_choice = input(
        "Choose an option: "
    )

    if delete_choice == "1":

        cursor.execute(
            """
            DELETE FROM Taxpayer
            WHERE TaxpayerID = %s
            """,
            (delete_taxpayer_id,)
        )

        connection.commit()

        print(
            "✅  Taxpayer "
            + delete_taxpayer_id
            + " deleted successfully."
        )

    else:

        print(
            "↩️  Delete taxpayer canceled."
        )


# Main program
try:

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("DB_NAME", "irs_project_db")
    )

    print(
        "✅  Connected to MySQL successfully!"
    )

    cursor = connection.cursor()

    while True:

        print(
            "\n🧾  IRS Database Application"
        )

        print(
            "1.  👥  View All Taxpayers"
        )

        print(
            "2.  🔍  Find Taxpayer by ID"
        )

        print(
            "3.  ➕  Add Taxpayer"
        )

        print(
            "4.  ✏️  Update Taxpayer"
        )

        print(
            "5.  🗑️  Delete Taxpayer"
        )

        print(
            "6.  👋  Exit"
        )

        choice = input(
            "Choose an option: "
        )

        if choice == "1":

            view_all_taxpayers(
                cursor
            )

        elif choice == "2":

            find_taxpayer(
                cursor
            )

        elif choice == "3":

            add_taxpayer(
                cursor,
                connection
            )

        elif choice == "4":

            update_taxpayer(
                cursor,
                connection
            )

        elif choice == "5":

            delete_taxpayer(
                cursor,
                connection
            )

        elif choice == "6":

            print(
                "\n👋  Goodbye!"
            )

            break

        else:

            print(
                "❌  Invalid option. "
                "Please choose 1-6."
            )

    # Close database resources
    cursor.close()
    connection.close()

except mysql.connector.Error as error:

    print(
        "❌  A database error occurred."
    )

    print(error)
