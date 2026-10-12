from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)


# Connect Flask to the IRS database
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("DB_NAME", "irs_project_db")
    )


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# READ: Display all taxpayers
@app.route("/taxpayers")
def taxpayers():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM Taxpayer
        ORDER BY TaxpayerID
    """)

    taxpayer_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "taxpayers.html",
        taxpayers=taxpayer_list
    )


# CREATE: Add a new taxpayer
@app.route("/taxpayers/create", methods=["GET", "POST"])
def create_taxpayer():

    if request.method == "POST":

        taxpayer_id = request.form["taxpayer_id"]
        first_name = request.form["first_name"]
        middle_initial = request.form["middle_initial"] or None
        last_name = request.form["last_name"]
        street_address = request.form["street_address"]
        apartment_number = request.form["apartment_number"] or None
        city = request.form["city"]
        state = request.form["state"].upper()
        zip_code = request.form["zip_code"]

        form_data = {
            "taxpayer_id": taxpayer_id,
            "first_name": first_name,
            "middle_initial": middle_initial or "",
            "last_name": last_name,
            "street_address": street_address,
            "apartment_number": apartment_number or "",
            "city": city,
            "state": state,
            "zip_code": zip_code
    }

        if not taxpayer_id.isdigit():
            return render_template(
                "create_taxpayer.html",
                error_message="Taxpayer ID must contain numbers only.",
                taxpayer_id_error=True,
                **form_data
            )

        if not (zip_code.isdigit() and len(zip_code) == 5):
            return render_template(
                "create_taxpayer.html",
                error_message="ZIP Code must be exactly 5 digits.",
                zip_code_error=True,
                **form_data
            )

        allowed_states = ["AZ", "CA", "NV", "OR", "WA"]

        if state not in allowed_states:
            return render_template(
                "create_taxpayer.html",
                error_message="Please select a valid state.",
                **form_data
            )
        
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
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
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            ))

            connection.commit()

        except mysql.connector.Error as error:
            connection.rollback()

            cursor.close()
            connection.close()

            return render_template(
            "create_taxpayer.html",
            error_message="Taxpayer ID already exists. Please enter a different ID.",
            taxpayer_id="",
            first_name=first_name,
            middle_initial=middle_initial or "",
            last_name=last_name,
            street_address=street_address,
            apartment_number=apartment_number or "",
            city=city,
            state=state,
            zip_code=zip_code,
            taxpayer_id_error=True
        )

        cursor.close()
        connection.close()

        return redirect("/taxpayers")

    return render_template("create_taxpayer.html")


# UPDATE: Edit and save the selected taxpayer
@app.route("/taxpayers/edit/<int:taxpayer_id>", methods=["GET", "POST"])
def edit_taxpayer(taxpayer_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        first_name = request.form["first_name"]
        middle_initial = request.form["middle_initial"] or None
        last_name = request.form["last_name"]
        street_address = request.form["street_address"]
        apartment_number = request.form["apartment_number"] or None
        city = request.form["city"]
        state = request.form["state"].upper()
        zip_code = request.form["zip_code"]

        # Server-side ZIP Code validation
        if not (zip_code.isdigit() and len(zip_code) == 5):

            taxpayer = {
                "TaxpayerID": taxpayer_id,
                "FirstName": first_name,
                "MiddleInitial": middle_initial,
                "LastName": last_name,
                "StreetAddress": street_address,
                "ApartmentNumber": apartment_number,
                "City": city,
                "State": state,
                "ZIPCode": zip_code
            }

            cursor.close()
            connection.close()

            return render_template(
                "edit_taxpayer.html",
                taxpayer=taxpayer,
                error_message="ZIP Code must be exactly 5 digits.",
                zip_code_error=True
            )

        try:
            cursor.execute("""
                UPDATE Taxpayer
                SET FirstName = %s,
                    MiddleInitial = %s,
                    LastName = %s,
                    StreetAddress = %s,
                    ApartmentNumber = %s,
                    City = %s,
                    State = %s,
                    ZIPCode = %s
                WHERE TaxpayerID = %s
            """,
            (
                first_name,
                middle_initial,
                last_name,
                street_address,
                apartment_number,
                city,
                state,
                zip_code,
                taxpayer_id
            ))

            connection.commit()

        except mysql.connector.Error as error:
            connection.rollback()

            taxpayer = {
                "TaxpayerID": taxpayer_id,
                "FirstName": first_name,
                "MiddleInitial": middle_initial,
                "LastName": last_name,
                "StreetAddress": street_address,
                "ApartmentNumber": apartment_number,
                "City": city,
                "State": state,
                "ZIPCode": zip_code
            }

            cursor.close()
            connection.close()

            return render_template(
                "edit_taxpayer.html",
                taxpayer=taxpayer,
                error_message="The database operation could not be completed."
            )

        cursor.close()
        connection.close()

        return redirect("/taxpayers")

    cursor.execute("""
        SELECT *
        FROM Taxpayer
        WHERE TaxpayerID = %s
    """, (taxpayer_id,))

    taxpayer = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit_taxpayer.html",
        taxpayer=taxpayer
    )

# DELETE: Protect related records and delete the selected taxpayer
@app.route("/taxpayers/delete/<int:taxpayer_id>", methods=["GET", "POST"])
def delete_taxpayer(taxpayer_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM Taxpayer
        WHERE TaxpayerID = %s
    """, (taxpayer_id,))

    taxpayer = cursor.fetchone()

    if request.method == "POST":

        cursor.execute("""
            SELECT COUNT(*) AS ReturnCount
            FROM TaxReturn
            WHERE TaxpayerID = %s
        """, (taxpayer_id,))

        result = cursor.fetchone()

        if result["ReturnCount"] > 0:

            cursor.close()
            connection.close()

            return render_template(
                "delete_taxpayer.html",
                taxpayer=taxpayer,
                delete_error="This taxpayer cannot be deleted because related tax return records exist."
            )

        try:
            cursor.execute("""
                DELETE FROM Taxpayer
                WHERE TaxpayerID = %s
            """, (taxpayer_id,))

            connection.commit()

        except mysql.connector.Error as error:
            connection.rollback()

            cursor.close()
            connection.close()

            return render_template(
                "delete_taxpayer.html",
                taxpayer=taxpayer,
                delete_error="The database operation could not be completed."
            )

        cursor.close()
        connection.close()

        return redirect("/taxpayers")

    cursor.close()
    connection.close()

    return render_template(
        "delete_taxpayer.html",
        taxpayer=taxpayer
    )


# READ: Display and filter tax returns
@app.route("/taxreturns")
def taxreturns():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    tax_year = request.args.get("tax_year", "")
    filing_status = request.args.get("filing_status", "")

    query = """
        SELECT
            tr.ReturnID,
            tr.TaxpayerID,
            t.FirstName,
            t.LastName,
            tr.TaxYear,
            tr.FilingStatus,
            tr.FilingDate,
            tr.TotalIncome,
            tr.AdjustedGrossIncome,
            tr.TotalDeductions,
            tr.TaxableIncome,
            tr.TotalNonrefundableCredits,
            tr.TotalTax
        FROM TaxReturn tr
        JOIN Taxpayer t
            ON tr.TaxpayerID = t.TaxpayerID
        WHERE 1 = 1
    """

    parameters = []

    if tax_year:
        query += " AND tr.TaxYear = %s"
        parameters.append(tax_year)

    if filing_status:
        query += " AND tr.FilingStatus = %s"
        parameters.append(filing_status)

    query += " ORDER BY tr.ReturnID"

    cursor.execute(query, parameters)

    taxreturn_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "taxreturns.html",
        taxreturns=taxreturn_list,
        selected_tax_year=tax_year,
        selected_filing_status=filing_status
    )


# CREATE: Add a new tax return
@app.route("/taxreturns/create", methods=["GET", "POST"])
def create_taxreturn():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Load taxpayers for the dropdown
    cursor.execute("""
        SELECT
            TaxpayerID,
            FirstName,
            LastName
        FROM Taxpayer
        ORDER BY TaxpayerID
    """)

    taxpayers = cursor.fetchall()

    if request.method == "POST":

        return_id = request.form["return_id"]
        taxpayer_id = request.form["taxpayer_id"]
        tax_year = request.form["tax_year"]
        filing_status = request.form["filing_status"]
        filing_date = request.form["filing_date"]
        total_income = request.form["total_income"]
        adjusted_gross_income = request.form["adjusted_gross_income"]
        total_deductions = request.form["total_deductions"]
        taxable_income = request.form["taxable_income"]
        total_nonrefundable_credits = request.form["total_nonrefundable_credits"]
        total_tax = request.form["total_tax"]

        form_data = {
            "return_id": return_id,
            "taxpayer_id": taxpayer_id,
            "tax_year": tax_year,
            "filing_status": filing_status,
            "filing_date": filing_date,
            "total_income": total_income,
            "adjusted_gross_income": adjusted_gross_income,
            "total_deductions": total_deductions,
            "taxable_income": taxable_income,
            "total_nonrefundable_credits": total_nonrefundable_credits,
            "total_tax": total_tax
        }

        # Validate Return ID
        if not (return_id.isdigit() and len(return_id) == 4):

            cursor.close()
            connection.close()

            return render_template(
                "create_taxreturn.html",
                taxpayers=taxpayers,
                error_message="Return ID must be exactly 4 digits.",
                return_id_error=True,
                **form_data
            )

        # Validate Tax Year
        if not (tax_year.isdigit() and len(tax_year) == 4):

            cursor.close()
            connection.close()

            return render_template(
                "create_taxreturn.html",
                taxpayers=taxpayers,
                error_message="Tax year must be exactly 4 digits.",
                tax_year_error=True,
                **form_data
            )

        # Validate Filing Status
        allowed_statuses = ["Single", "MFJ", "MFS", "HOH", "QSS"]

        if filing_status not in allowed_statuses:

            cursor.close()
            connection.close()

            return render_template(
                "create_taxreturn.html",
                taxpayers=taxpayers,
                error_message="Please select a valid filing status.",
                **form_data
            )

        try:
            cursor.execute("""
                INSERT INTO TaxReturn
                (
                    ReturnID,
                    TaxpayerID,
                    TaxYear,
                    FilingStatus,
                    FilingDate,
                    TotalIncome,
                    AdjustedGrossIncome,
                    TotalDeductions,
                    TaxableIncome,
                    TotalNonrefundableCredits,
                    TotalTax
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                return_id,
                taxpayer_id,
                tax_year,
                filing_status,
                filing_date,
                total_income,
                adjusted_gross_income,
                total_deductions,
                taxable_income,
                total_nonrefundable_credits,
                total_tax
            ))

            connection.commit()

        except mysql.connector.Error as error:
            connection.rollback()

            form_data["return_id"] = ""

            cursor.close()
            connection.close()

            return render_template(
                "create_taxreturn.html",
                taxpayers=taxpayers,
                error_message="The database operation could not be completed.",
                return_id_error=True,
                **form_data
            )

        cursor.close()
        connection.close()

        return redirect("/taxreturns")

    cursor.close()
    connection.close()

    return render_template(
        "create_taxreturn.html",
        taxpayers=taxpayers
    )


# UPDATE: Edit an existing tax return
@app.route("/taxreturns/edit/<int:return_id>", methods=["GET", "POST"])
def edit_taxreturn(return_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        taxpayer_id = request.form["taxpayer_id"]
        tax_year = request.form["tax_year"]
        filing_status = request.form["filing_status"]
        filing_date = request.form["filing_date"]
        total_income = request.form["total_income"]
        adjusted_gross_income = request.form["adjusted_gross_income"]
        total_deductions = request.form["total_deductions"]
        taxable_income = request.form["taxable_income"]
        total_nonrefundable_credits = request.form["total_nonrefundable_credits"]
        total_tax = request.form["total_tax"]

        form_data = {
            "ReturnID": return_id,
            "TaxpayerID": taxpayer_id,
            "TaxYear": tax_year,
            "FilingStatus": filing_status,
            "FilingDate": filing_date,
            "TotalIncome": total_income,
            "AdjustedGrossIncome": adjusted_gross_income,
            "TotalDeductions": total_deductions,
            "TaxableIncome": taxable_income,
            "TotalNonrefundableCredits": total_nonrefundable_credits,
            "TotalTax": total_tax
        }

        if not tax_year.isdigit():

            cursor.execute("""
                SELECT
                    TaxpayerID,
                    FirstName,
                    LastName
                FROM Taxpayer
                ORDER BY TaxpayerID
            """)

            taxpayers = cursor.fetchall()

            cursor.close()
            connection.close()

            return render_template(
                "edit_taxreturn.html",
                taxreturn=form_data,
                taxpayers=taxpayers,
                error_message="Tax year must be exactly 4 digits.",
                tax_year_error=True
            )

        allowed_statuses = ["Single", "MFJ", "MFS", "HOH", "QSS"]

        if filing_status not in allowed_statuses:

            cursor.execute("""
                SELECT
                    TaxpayerID,
                    FirstName,
                    LastName
                FROM Taxpayer
                ORDER BY TaxpayerID
            """)

            taxpayers = cursor.fetchall()

            cursor.close()
            connection.close()

            return render_template(
                "edit_taxreturn.html",
                taxreturn=form_data,
                taxpayers=taxpayers,
                error_message="Please select a valid filing status."
            )

        try:
            cursor.execute("""
                UPDATE TaxReturn
                SET TaxpayerID = %s,
                    TaxYear = %s,
                    FilingStatus = %s,
                    FilingDate = %s,
                    TotalIncome = %s,
                    AdjustedGrossIncome = %s,
                    TotalDeductions = %s,
                    TaxableIncome = %s,
                    TotalNonrefundableCredits = %s,
                    TotalTax = %s
                WHERE ReturnID = %s
            """,
            (
                taxpayer_id,
                tax_year,
                filing_status,
                filing_date,
                total_income,
                adjusted_gross_income,
                total_deductions,
                taxable_income,
                total_nonrefundable_credits,
                total_tax,
                return_id
            ))

            connection.commit()

        except mysql.connector.Error as error:
            connection.rollback()

            cursor.execute("""
                SELECT
                    TaxpayerID,
                    FirstName,
                    LastName
                FROM Taxpayer
                ORDER BY TaxpayerID
            """)

            taxpayers = cursor.fetchall()

            cursor.close()
            connection.close()

            return render_template(
                "edit_taxreturn.html",
                taxreturn=form_data,
                taxpayers=taxpayers,
                error_message="The database operation could not be completed."
            )

        cursor.close()
        connection.close()

        return redirect("/taxreturns")

    cursor.execute("""
        SELECT *
        FROM TaxReturn
        WHERE ReturnID = %s
    """, (return_id,))

    taxreturn = cursor.fetchone()

    cursor.execute("""
        SELECT
            TaxpayerID,
            FirstName,
            LastName
        FROM Taxpayer
        ORDER BY TaxpayerID
    """)

    taxpayers = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "edit_taxreturn.html",
        taxreturn=taxreturn,
        taxpayers=taxpayers
    )


# DELETE: Protect related records and delete the selected tax return
@app.route("/taxreturns/delete/<int:return_id>", methods=["GET", "POST"])
def delete_taxreturn(return_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM TaxReturn
        WHERE ReturnID = %s
    """, (return_id,))

    taxreturn = cursor.fetchone()

    if request.method == "POST":

        cursor.execute("""
            SELECT
                (SELECT COUNT(*) FROM IncomeRecord WHERE ReturnID = %s) AS IncomeCount,
                (SELECT COUNT(*) FROM Deduction WHERE ReturnID = %s) AS DeductionCount,
                (SELECT COUNT(*) FROM TaxCredit WHERE ReturnID = %s) AS CreditCount,
                (SELECT COUNT(*) FROM Refund WHERE ReturnID = %s) AS RefundCount,
                (SELECT COUNT(*) FROM BalanceDue WHERE ReturnID = %s) AS BalanceDueCount,
                (SELECT COUNT(*) FROM TaxForm WHERE ReturnID = %s) AS FormCount
        """,
        (
            return_id,
            return_id,
            return_id,
            return_id,
            return_id,
            return_id
        ))

        result = cursor.fetchone()

        related_records = (
            result["IncomeCount"]
            + result["DeductionCount"]
            + result["CreditCount"]
            + result["RefundCount"]
            + result["BalanceDueCount"]
            + result["FormCount"]
        )

        if related_records > 0:

            cursor.close()
            connection.close()

            return render_template(
                "delete_taxreturn.html",
                taxreturn=taxreturn,
                delete_error="This tax return cannot be deleted because related records exist."
            )

        try:
            cursor.execute("""
                DELETE FROM TaxReturn
                WHERE ReturnID = %s
            """, (return_id,))

            connection.commit()

        except mysql.connector.Error as error:
            connection.rollback()

            cursor.close()
            connection.close()

            return render_template(
                "delete_taxreturn.html",
                taxreturn=taxreturn,
                delete_error="The database operation could not be completed."
            )

        cursor.close()
        connection.close()

        return redirect("/taxreturns")

    cursor.close()
    connection.close()

    return render_template(
        "delete_taxreturn.html",
        taxreturn=taxreturn
    )

# Analytics home page
@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

# Q1: Refund and balance-due outcomes
@app.route("/analytics/refund-balance")
def refund_balance_report():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    tax_year = request.args.get("tax_year", "")

    query = """
        SELECT *
        FROM (
            SELECT
                tr.ReturnID,
                tr.TaxpayerID,
                tr.TaxYear,
                tr.FilingStatus,
                'Refund' AS OutcomeType,
                r.RefundAmount AS Amount
            FROM TaxReturn tr
            JOIN Refund r
                ON tr.ReturnID = r.ReturnID

            UNION ALL

            SELECT
                tr.ReturnID,
                tr.TaxpayerID,
                tr.TaxYear,
                tr.FilingStatus,
                'Balance Due' AS OutcomeType,
                b.AmountDue AS Amount
            FROM TaxReturn tr
            JOIN BalanceDue b
                ON tr.ReturnID = b.ReturnID
        ) AS TaxOutcomes
    """

    parameters = []

    if tax_year:
        query += " WHERE TaxYear = %s"
        parameters.append(tax_year)

    query += " ORDER BY TaxYear, ReturnID"

    cursor.execute(query, parameters)

    results = cursor.fetchall()

    refund_count = sum(
        1 for row in results
        if row["OutcomeType"] == "Refund"
    )

    balance_due_count = sum(
        1 for row in results
        if row["OutcomeType"] == "Balance Due"
    )

    cursor.close()
    connection.close()

    return render_template(
        "analytics_result.html",
        title="Refund and Balance-Due Outcomes",
        question="What are the refund and balance-due outcomes for tax returns?",
        sql_concept="UNION ALL",
        results=results,
        chart_type="pie",
        chart_labels=["Refund", "Balance Due"],
        chart_values=[refund_count, balance_due_count],
        show_year_filter=True,
        selected_tax_year=tax_year,
        sql_query=query
    )

# Q2: Highest deductions within selected filing statuses for one tax year
@app.route("/analytics/high-income")
def high_income_report():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    tax_year = request.args.get("tax_year", "")

    # Allows more than one filing status
    filing_statuses = request.args.getlist("filing_status")

    query = """
        SELECT
            tr.ReturnID,
            tr.TaxpayerID,
            tr.TaxYear,
            tr.FilingStatus,
            tr.TotalDeductions
        FROM TaxReturn tr

        WHERE tr.ReturnID IN (
            SELECT ReturnID
            FROM Deduction
        )

        AND tr.TotalDeductions >= ALL (
            SELECT tr2.TotalDeductions
            FROM TaxReturn tr2
            WHERE tr2.FilingStatus = tr.FilingStatus
              AND tr2.TaxYear = tr.TaxYear
        )
    """

    parameters = []

    # One tax year
    if tax_year:
        query += " AND tr.TaxYear = %s"
        parameters.append(tax_year)

    # Multiple filing statuses
    if filing_statuses:

        placeholders = ", ".join(
            ["%s"] * len(filing_statuses)
        )

        query += f"""
            AND tr.FilingStatus IN ({placeholders})
        """

        parameters.extend(filing_statuses)

    query += """
        ORDER BY
            tr.TaxYear,
            tr.FilingStatus
    """

    cursor.execute(
        query,
        parameters
    )

    results = cursor.fetchall()

    chart_labels = [
        f"{row['TaxYear']} {row['FilingStatus']}"
        for row in results
    ]

    chart_values = [
        float(row["TotalDeductions"])
        for row in results
    ]

    chart_colors = [
        "#4E79A7",
        "#F28E2B",
        "#E15759",
        "#76B7B2",
        "#59A14F",
        "#EDC948",
        "#B07AA1",
        "#FF9DA7",
        "#9C755F",
        "#BAB0AC"
    ]

    cursor.close()
    connection.close()

    return render_template(
        "analytics_result.html",
        title="Highest Deductions by Filing Status",
        question="Which returns have the highest total deductions within the selected filing statuses for one tax year?",
        sql_concept="IN and ALL",
        results=results,
        chart_type="bar",
        chart_labels=chart_labels,
        chart_values=chart_values,
        chart_colors=chart_colors,
        show_q2_filters=True,
        selected_tax_year=tax_year,
        selected_filing_statuses=filing_statuses,
        sql_query=query
    )

# Q3: Refund analysis by deduction quartile for selected tax year
@app.route("/analytics/deduction-quartiles")
def deduction_quartile_report():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    tax_year = request.args.get("tax_year", "")

    query = """
        WITH RefundData AS (
            SELECT
                tr.ReturnID,
                tr.TaxYear,
                tr.FilingStatus,
                tr.TotalIncome,
                d.TotalDeduction,
                r.RefundAmount,

                NTILE(4) OVER (
                    PARTITION BY tr.TaxYear
                    ORDER BY d.TotalDeduction
                ) AS DeductionQuartile

            FROM TaxReturn tr

            JOIN Refund r
                ON tr.ReturnID = r.ReturnID

            JOIN (
                SELECT
                    ReturnID,
                    SUM(Amount) AS TotalDeduction
                FROM Deduction
                GROUP BY ReturnID
            ) d
                ON tr.ReturnID = d.ReturnID
        )

        SELECT
            ReturnID,
            TaxYear,
            FilingStatus,
            TotalIncome,
            TotalDeduction,
            RefundAmount,
            DeductionQuartile,

            ROUND(
                AVG(RefundAmount) OVER (
                    PARTITION BY TaxYear, DeductionQuartile
                ),
                2
            ) AS QuartileAverageRefund,

            RANK() OVER (
                PARTITION BY TaxYear, DeductionQuartile
                ORDER BY RefundAmount DESC
            ) AS RefundRank

        FROM RefundData
    """

    parameters = []

    if tax_year:
        query += " WHERE TaxYear = %s"
        parameters.append(tax_year)

    query += """
        ORDER BY
            TaxYear,
            DeductionQuartile,
            RefundRank
    """

    cursor.execute(query, parameters)

    results = cursor.fetchall()

    chart_labels = [
        f"Return {row['ReturnID']} - Q{row['DeductionQuartile']}"
        for row in results
    ]

    chart_values = [
        float(row["RefundAmount"])
        for row in results
    ]

    cursor.close()
    connection.close()

    return render_template(
        "analytics_result.html",
        title="Refunds by Deduction Level",
        question="How do refund amounts compare across deduction quartiles for the selected tax year?",
        sql_concept="WITH, SUM, NTILE, AVG OVER, and RANK",
        results=results,
        chart_type="bar",
        chart_labels=chart_labels,
        chart_values=chart_values,
        show_q3_year_filter=True,
        selected_tax_year=tax_year,
        sql_query=query
    )

# Q4: Filing-status income trends for selected tax year and filing statuses
@app.route("/analytics/filing-status-trends")
def filing_status_trends_report():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    tax_year = request.args.get("tax_year", "")
    filing_statuses = request.args.getlist("filing_status")

    query = """
        SELECT
            ReturnID,
            TaxYear,
            FilingDate,
            FilingStatus,
            TotalIncome,

            ROUND(
                AVG(TotalIncome) OVER (
                    PARTITION BY TaxYear, FilingStatus
                ),
                2
            ) AS FilingStatusAverageIncome,

            SUM(TotalIncome) OVER (
                PARTITION BY TaxYear, FilingStatus
                ORDER BY FilingDate, ReturnID
                ROWS UNBOUNDED PRECEDING
            ) AS CumulativeIncomeByFilingDate,

            COUNT(ReturnID) OVER (
                PARTITION BY TaxYear, FilingStatus
            ) AS ReturnCount

        FROM TaxReturn
        WHERE 1 = 1
    """

    parameters = []

    if tax_year:
        query += " AND TaxYear = %s"
        parameters.append(tax_year)

    if filing_statuses:

        placeholders = ", ".join(
            ["%s"] * len(filing_statuses)
        )

        query += f"""
            AND FilingStatus IN ({placeholders})
        """

        parameters.extend(filing_statuses)

    query += """
        ORDER BY
            TaxYear,
            FilingStatus,
            FilingDate,
            ReturnID
    """

    cursor.execute(query, parameters)

    results = cursor.fetchall()

    # Build all dates for the x-axis
    chart_labels = sorted(
        list({
            str(row["FilingDate"])
            for row in results
        })
    )

    # Group data by Tax Year + Filing Status
    grouped_data = {}

    for row in results:

        group_name = f"{row['TaxYear']} - {row['FilingStatus']}"

        if group_name not in grouped_data:
            grouped_data[group_name] = {}

        grouped_data[group_name][
            str(row["FilingDate"])
        ] = float(
            row["CumulativeIncomeByFilingDate"]
        )

    # Create one chart dataset for each group
    chart_datasets = []

    for group_name, values_by_date in grouped_data.items():

        data_points = []

        for date in chart_labels:

            if date in values_by_date:
                data_points.append(values_by_date[date])
            else:
                data_points.append(None)

        chart_datasets.append({
            "label": group_name,
            "data": data_points
        })

    cursor.close()
    connection.close()

    return render_template(
        "analytics_result.html",
        title="Filing-Status Income Trends",
        question="How does income compare and accumulate over time within selected filing statuses for a selected tax year?",
        sql_concept="AVG OVER, SUM OVER, COUNT OVER, and PARTITION BY",
        results=results,
        chart_type="line",
        chart_labels=chart_labels,
        chart_datasets=chart_datasets,
        show_q4_filters=True,
        selected_tax_year=tax_year,
        selected_filing_statuses=filing_statuses,
        sql_query=query
    )
# Run the Flask application locally
if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
