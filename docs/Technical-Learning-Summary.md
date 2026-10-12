# CS 727 IRS Database Project Technical Learning Summary

## Summary table

| Deliverable | Goal | Tools | Languages | Libraries / Functions / Techniques | Purpose |
|---|---|---|---|---|---|
| 1 | Design an IRS-inspired relational database | Markdown editor, Mermaid or diagram tooling, PDF export, IRS references | Markdown, Mermaid-style ERD notation | ERD, relational schemas, PK/FK selection, cardinality, 3NF review, business rules | Convert a real domain into a clear logical data model |
| 2 | Build and populate the database | MySQL, MySQL client, Python, CSV files | SQL, Python | DDL, `LOAD DATA LOCAL INFILE`, PK/FK/`CHECK`, temporary table, view, procedure, function, trigger, Faker, `csv`, `random`, `datetime` | Create the schema, generate test data, repair data gaps, and validate integrity |
| 3 | Test and explain 15 analytical queries | MySQL, result screenshots | SQL, Markdown | Joins, grouped aggregates, derived tables, `ROLLUP`, `CASE`, CTE, `RANK`, `DENSE_RANK`, `PERCENT_RANK`, `CUME_DIST`, `ROW_NUMBER`, `NTILE`, framed `AVG`, running `SUM` | Answer business questions and practice OLAP and window analysis |
| 4 | Implement basic CRUD in an application | Python terminal, MySQL | Python, SQL, Markdown | `mysql.connector`, `tabulate`, functions, loops, dictionaries, parameterized SQL, `commit`, `rollback`, validation, exception handling | Provide a menu-driven database client with safe updates and deletes |
| 5 | Add a web interface and complex analytics | Flask development server, browser, MySQL, Chart.js | Python, SQL, HTML, CSS, Jinja, JavaScript | Flask routes, GET/POST, forms, query strings, templates, environment variables, `UNION ALL`, `IN`, `ALL`, CTEs, window functions, dynamic charts | Combine CRUD, filtering, validation, and analytics in a reusable web UI |

### 10 Key Lessons from CS 727

1. **Relational modeling.** Start by separating the domain into entities with clear responsibilities. The project modeled taxpayers, returns, financial details, outcomes, and forms as eight related tables.
2. **Keys and relationships.** Primary keys identify rows, while foreign keys connect valid parent and child records. `TaxpayerID` links returns to taxpayers, and `ReturnID` links six child tables to each return.
3. **Normalization.** Store each fact in the appropriate table to reduce duplication and update problems. Taxpayer addresses are stored once, while repeating income and deduction items become separate rows.
4. **Constraints and business rules.** Data types, `NOT NULL`, `CHECK`, foreign keys, procedures, and triggers solve different integrity problems. The project also showed that a rule written in an ERD is not guaranteed until an enforcement mechanism is implemented.
5. **Reproducible test data.** Synthetic data makes database development safer, and fixed random seeds make results repeatable. Python, Faker, `csv`, and `random` produced linked CSV records for the eight tables.
6. **Transactions and safe CRUD.** Inserts, updates, and deletes should be parameterized, committed deliberately, and rolled back on failure or cancellation. Both Python applications used these techniques to protect changes.
7. **Joins and aggregation.** Joins reconstruct information spread across normalized tables, while `GROUP BY`, `SUM`, `AVG`, and `COUNT` answer summary questions. Deliverable 3 applied them to filing status, income type, tax year, and tax outcome.
8. **Window functions and OLAP.** Window functions add ranks, distributions, moving averages, and running totals without collapsing detail rows. The project used `RANK`, `NTILE`, `PERCENT_RANK`, `CUME_DIST`, and windowed aggregates.
9. **Application layers.** A database application connects browser or terminal input to validation, SQL, transactions, and output. The project progressed from a command-line menu to Flask routes, Jinja templates, forms, CSS, and charts.
10. **Security and maintainability.** Parameterized queries, environment variables, consistent validation, reusable templates, and deterministic setup files make an application safer and easier to reproduce. Deliverable 5 improved credential handling and reused one analytics-results template across four reports.

## Deliverable 1: database design

### Goal

The first deliverable defined the information system before writing SQL. The task was to identify six to eight entities, their attributes, relationships, constraints, users, and use cases, then reduce the ERD into relational schemas.

### Final implementation

The final design contains eight entities:

```text
Taxpayer -> TaxReturn -> IncomeRecord
                      -> Deduction
                      -> TaxCredit
                      -> Refund
                      -> BalanceDue
                      -> TaxForm
```

`Taxpayer` and `TaxReturn` are the core tables. The other six tables separate repeating financial details, mutually exclusive outcomes, and associated forms. The design declares `TaxpayerID`, `ReturnID`, and each child-specific ID as primary keys. Every child stores a foreign key to its parent.

The submitted document also defines seven use cases, including retrieving a complete return, comparing filing statuses or years, analyzing refund and balance-due outcomes, and ranking high-value returns.

### Tools and languages

- Markdown was used for the editable design source and supporting notes.
- A PDF was used for the submitted document.
- Text-based ERD notation and Mermaid support files were used to express entities and cardinalities.
- IRS Form 1040 and related materials were used to identify relevant concepts.

### Technical features and purpose

**Entity separation.** Income, deduction, credit, outcome, and form data were separated from the return summary. This avoids repeating return and taxpayer data for every detail row.

**Primary keys.** Each relation has a stable identifier, such as `TaxpayerID` or `IncomeID`. A primary key uniquely identifies a row and becomes the target of relationships.

**Foreign keys.** Each return stores `TaxpayerID`; each detail or outcome table stores `ReturnID`. These links allow joins and protect referential integrity after implementation.

**Cardinality.** The design distinguishes zero-to-many detail records from zero-to-one outcomes and the intended one-to-many form relationship. This is more precise than simply drawing connections.

**Normalization.** The submitted design states that the schemas were reviewed through Third Normal Form. In practical terms, the design avoids repeating taxpayer attributes in returns and stores repeating income or deduction items in child tables.

**Business rules.** Filing status uses a fixed domain. A return may have a refund, a balance due, or neither, but not both. A return should include Form 1040, and only the current accepted return for a taxpayer and year should remain.

### Example locations

- Final submitted design: `Deliverable-1/Deliverable-1_Zhao Li.pdf`
- Editable final source: `Deliverable-1/Final-Deliverable-1.md`
- ERD support: `Deliverable-1/09-ERD-Mermaid.md`
- Relationship and constraint analysis: `Deliverable-1/05-Relationships.md`, `Deliverable-1/06-Cardinality-Rationale.md`, and `Deliverable-1/07-Data-Constraints-and-Business-Rules.md`
- Earlier draft: `Deliverable-1/Final-Deliverable-1-DRAFT.md`

### Learning outcomes

- Model a real domain before choosing implementation details.
- Translate an ERD into relational schemas.
- Distinguish keys, cardinality, optionality, semantic definitions, and business rules.
- Use normalization to reduce duplication and update anomalies.
- Recognize that an ERD rule still needs a specific enforcement mechanism in SQL or application code.

## Deliverable 2: MySQL database implementation and synthetic data

### Goal

The second deliverable turned the design into a working MySQL database, loaded at least 15 records per relation, and demonstrated indexes, views, temporary tables, triggers, stored procedures, and functions.

### Final implementation

The main SQL creates `irs_project_db` and eight tables. Python scripts generate the initial CSV data. `load_data.sql` imports those files. The SQL then reviews counts and relationships, adds ten 2023 returns, raises the `BalanceDue` count to 15, fills missing child rows, validates the completed data, creates an income-classification function, and tests a trigger that blocks a conflicting balance-due insert.

The submitted Deliverable 2 CSV contains 25 returns for 2025, with ReturnIDs 1001 through 1025. The SQL review comments document a completed working state of 35 returns after adding 10 returns for 2023, and state that all eight tables met the 15-row minimum.

### Dataset count note

The count changed by stage rather than through a different committed CSV. `fakedata/TaxReturn.csv` contains 25 rows, while the documented SQL maintenance path adds 10 prior-year returns to reach the recorded 35-row database state. Deliverable 3 explicitly analyzes 35 returns. Deliverable 5 packages the same 25-row CSV and a byte-identical copy of the main Deliverable 2 SQL, so its files preserve the same 25-row seed and 35-row documented target.

No reviewed CSV, SQL dump, README, or saved count output contains or confirms 60 tax returns. If a 60-return database was used later, it was an unexported live state and cannot be reconstructed or verified from the final submitted files alone.

### MySQL DDL and constraints

The pattern below appears throughout `Deliverable-2/Deliverable_2_Zhao Li/irs_project_db.sql`:

```sql
CREATE TABLE IncomeRecord (
    IncomeID INT,
    ReturnID INT NOT NULL,
    IncomeType VARCHAR(50) NOT NULL,
    Amount DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (IncomeID),
    FOREIGN KEY (ReturnID) REFERENCES TaxReturn(ReturnID),
    CHECK (Amount >= 0)
);
```

In plain English, every income row has its own ID, must belong to an existing return, must name an income type, and cannot store a negative amount.

`TaxReturn` adds checks for the five filing statuses and nonnegative summary amounts. `DECIMAL(12,2)` is used instead of floating-point storage for database currency values.

### Data loading

`load_data.sql` uses this MySQL pattern for all eight CSV files:

```sql
LOAD DATA LOCAL INFILE 'fakedata/Taxpayer.csv'
INTO TABLE Taxpayer
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

This performs a bulk import, interprets quoted comma-separated fields, and skips the header row. The submitted Deliverable 2 archive uses absolute course-environment file paths. A later local version changes them to relative paths, which is more portable and is the version reused in Deliverable 5.

### Python synthetic data generation

The generator scripts use:

- `Faker` for fictional names and addresses.
- Python's `csv` module for `DictReader`, `writer`, headers, and data rows.
- `random.seed(727)` and `Faker.seed(727)` for repeatability.
- Loops and lists to build one or more child records for each return.
- `random.choice`, `random.sample`, `random.randint`, and `random.uniform` for controlled variation.
- `date`, `date.fromisoformat`, and `timedelta` for filing, refund, and due dates.
- Sets to remember refund return IDs and avoid generating a balance due for the same initial return.

Example from `fakedata/fake_taxform.py`:

```python
tax_form_records.append([tax_form_id, return_id, "Form 1040"])
number_of_additional_forms = random.randint(0, 2)
selected_forms = random.sample(additional_forms, number_of_additional_forms)
```

This guarantees one Form 1040 for every generated return, then optionally adds schedules.

The income and deduction generators maintain a remaining total and give the final child row the remainder. That technique keeps the child amounts aligned with the return summary despite random splitting.

### Temporary table and data transformation

`Temp2023Returns` stages randomly generated values for existing taxpayers before inserting complete 2023 returns. The final insert calculates adjusted gross income, taxable income, and a simplified tax amount with `ROUND`, `GREATEST`, arithmetic, and `RAND()`.

Purpose: staging makes intermediate values inspectable and reusable. It is safer than hiding every calculation in one opaque insert.

### Stored procedure

`add_balance_due` accepts the new balance-due fields as parameters, counts refunds for the target return, inserts only when the count is zero, and otherwise raises `SIGNAL SQLSTATE '45000'`.

Purpose: package a write and its business-rule check into one reusable database operation.

### View

`TaxReturnRelationshipSummary` joins the parent tables to all six child tables. It uses `COUNT(DISTINCT ...)`, `CASE`, `JOIN`, `LEFT JOIN`, and `GROUP BY` to show child counts and outcome flags per return.

Purpose: reveal missing related records without writing the same large review query repeatedly. It found that new 2023 returns lacked income, deduction, credit, and form rows, which were then populated and reviewed again.

### Stored function

`income_level(ReturnID)` loads one return's income, calculates the database-wide average, and returns `High Income` or `Standard Income`.

Purpose: demonstrate a value-returning stored program that can be called inside a `SELECT`.

### Trigger

`prevent_refund_balance_due` is a `BEFORE INSERT ON BalanceDue` trigger. It counts refunds for `NEW.ReturnID` and raises a custom error if a refund exists.

Purpose: protect a cross-table rule even when the insert does not go through the stored procedure.

### Indexes and an important distinction

Primary keys and foreign keys provide or require indexes in MySQL, and the script inspects them with `SHOW INDEX`. A separate `CREATE INDEX idx_taxpayer_lastname` appears only in commented practice code. Therefore, it is accurate to say indexes were reviewed and key indexes existed, but an additional active performance index was not verified in the final SQL.

### Practical limitations

- The main SQL file records an interactive development process. Some alternative insert blocks remain active and would attempt to reuse ReturnIDs if the entire file were run from top to bottom without selecting sections.
- The final trigger protects only inserts into `BalanceDue`; it does not protect inserts into `Refund` or updates to either table.
- `ReturnID` is not unique in the outcome child tables, so the intended zero-or-one cardinality is not guaranteed by the schema.
- The trigger test deliberately ends with a custom error. That is evidence of the test, but it also means the file is not an idempotent deployment script.

### Example locations

- Submitted archive: `Deliverable-2/Deliverable_2_Zhao Li.zip`
- Main SQL: `Deliverable-2/Deliverable_2_Zhao Li/irs_project_db.sql`
- Later sections-only copy: `Deliverable-2/Deliverable_2_Zhao Li/irs_project_db_4-9.sql`
- Data loading: `Deliverable-2/Deliverable_2_Zhao Li/load_data.sql`
- Generators and CSV files: `Deliverable-2/Deliverable_2_Zhao Li/fakedata/`
- Saved evidence: `relationship_review.png`, `final_database_review.png`, `function_output.png`, and `trigger_test.png`

### Learning outcomes

- Translate logical schemas into MySQL DDL.
- Choose SQL data types and nullability.
- Load bulk CSV data and diagnose path portability.
- Generate consistent parent and child test data in Python.
- Use database objects for reuse, review, transformation, and integrity.
- Separate a rule demonstrated by current data from a rule guaranteed for all future data.
- Appreciate the value of a clean migration script that can be rerun safely.

## Deliverable 3: analytical SQL

### Goal

The third deliverable asked for at least 15 varied, relevant queries, including advanced window and OLAP queries, with an explanation and saved output for each.

### Final implementation

`Deliverable-3/irs_project_queries.sql` contains exactly 15 numbered questions. `Deliverable-3/README.md` explains the findings, and `query_results/` contains one PNG per query.

### Query-by-query technique map

| Query | Main techniques | Problem solved |
|---|---|---|
| 1 | `RANK`, `DENSE_RANK` | Compare total-income and taxable-income rankings |
| 2 | `RANK` with `PARTITION BY FilingStatus` | Rank income within each filing-status group |
| 3 | `RANK`, `PERCENT_RANK` | Locate returns in the income distribution |
| 4 | `PERCENT_RANK`, `CUME_DIST` | Compare relative rank with cumulative distribution |
| 5 | `ROW_NUMBER`, `NTILE(4)` | Divide returns into income quartiles |
| 6 | `SUM OVER`, `ROWS UNBOUNDED PRECEDING` | Calculate a running income total per filing status |
| 7 | framed `AVG OVER`, one preceding to one following | Calculate a local moving average |
| 8 | `GROUP BY`, `AVG`, `COUNT` | Compare group size and mean income |
| 9 | `GROUP BY ... WITH ROLLUP` | Add an overall average row to group averages |
| 10 | inner join, `SUM`, multidimensional grouping | Compare income type totals by filing status |
| 11 | three-table joins and three grouping dimensions | Compare average income by year, state, and type |
| 12 | derived table, `COUNT(DISTINCT)`, `CASE`, left joins | Compare income-source complexity by tax outcome |
| 13 | pre-aggregated derived tables, `COALESCE` | Avoid row multiplication when combining deductions and credits |
| 14 | refund join plus pre-aggregated child totals | Compare refund-related measures by filing status |
| 15 | `WITH`, `NTILE`, windowed `AVG`, `RANK` | Compare refunds within deduction quartiles |

### Important examples

**Window partitioning.** Query 2 resets the rank for each status:

```sql
RANK() OVER (
    PARTITION BY FilingStatus
    ORDER BY TotalIncome DESC
) AS IncomeRank
```

Without `PARTITION BY`, the rank would be global rather than group-specific.

**Window frame.** Query 7 averages the current row and neighboring filing records:

```sql
AVG(TotalIncome) OVER (
    PARTITION BY FilingStatus
    ORDER BY FilingDate, ReturnID
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
)
```

The explicit `ROWS` frame defines exactly which rows contribute to each moving average.

**Pre-aggregation before joining.** Queries 13 and 14 first total deductions and credits per return in separate subqueries. This avoids multiplying deduction rows by credit rows in a direct many-to-many join.

**Common table expression.** Query 15 names an intermediate result `RefundData`, assigns deduction quartiles, then computes a quartile average and refund rank while retaining one row per return.

### Example locations

- SQL: `Deliverable-3/irs_project_queries.sql`
- Questions and findings: `Deliverable-3/README.md`
- Results: `Deliverable-3/query_results/query_01_result.png` through `query_15_result.png`

### Learning outcomes

- Distinguish grouped aggregates from windowed aggregates.
- Use partitions and frames to control analytical context.
- Preserve detail rows while adding group statistics.
- Use derived tables and CTEs to make complex logic readable.
- Avoid double-counting when joining multiple one-to-many tables.
- Connect each query technique to a business question rather than using features only for syntax practice.

## Deliverable 4: Python command-line CRUD application

### Goal

The fourth deliverable added a programmatic interface for basic Create, Read, Update, and Delete operations and required a short demonstration.

### Final implementation

The submitted `irs_app.py` is a terminal application for the `Taxpayer` table. Its menu supports:

1. View all taxpayers.
2. Find a taxpayer by ID.
3. Add a taxpayer.
4. Update one or more fields.
5. Delete an unreferenced taxpayer.
6. Exit.

The program is organized into `display_taxpayers`, `view_all_taxpayers`, `find_taxpayer`, `add_taxpayer`, `update_taxpayer`, and `delete_taxpayer` functions.

### Libraries and language features

**`mysql.connector`.** Opens the MySQL connection, creates a cursor, sends SQL, retrieves rows, and exposes `mysql.connector.Error`.

**`tabulate`.** Formats database tuples into readable grid tables in the terminal.

**Functions.** Each CRUD responsibility is isolated in a named function.

**Loops.** The main `while True` loop keeps the menu active. Nested loops let a user review and correct create or update values before committing.

**Lists, tuples, and dictionaries.** Tuples supply SQL parameters, lists hold mutable taxpayer data and validation errors, and `field_map` maps menu choices to known column names and tuple positions.

### Parameterized SQL

```python
cursor.execute(
    "SELECT * FROM Taxpayer WHERE TaxpayerID = %s",
    (taxpayer_id,)
)
```

The value is sent separately from the SQL text. This avoids manual quoting and reduces SQL-injection risk.

The update statement uses an f-string only for the column name, and that name comes from the fixed `field_map`, not arbitrary user input. The new value and taxpayer ID remain parameterized.

### Validation

The create flow checks:

- Required text fields.
- Numeric taxpayer ID.
- Duplicate taxpayer ID through a lookup.
- One-character middle initial.
- Two-letter alphabetic state abbreviation.
- Five-digit or ZIP+4 format.
- Optional middle initial and apartment number converted to `None`, which becomes SQL `NULL`.

The update flow applies field-specific checks and does not allow the primary key to be edited.

### Transactions and cancellation

`connection.commit()` makes successful inserts, updates, and deletes permanent. `connection.rollback()` cancels staged updates when the user chooses to abandon them. The review and confirmation prompts make the transaction boundary understandable to the user.

### Protected delete

Before deleting a taxpayer, the program counts related `TaxReturn` rows. If the count is positive, it explains why deletion is refused. This prevents an integrity error and preserves the parent-child relationship.

### Error handling and security note

A top-level `try` and `except mysql.connector.Error` catches connection and database failures. The submitted program hard-codes the MySQL password in source code. This is a security weakness and should not be copied into future work. Deliverable 5 corrects it by using the `MYSQL_PASSWORD` environment variable.

The submitted ZIP version is the authoritative Deliverable 4 program. The standalone copy in the project folder adds `connection.autocommit = True` later and is therefore a post-submission variant.

### Example locations

- Submitted archive: `Deliverable-4/Deliverable-4.zip`
- Later standalone copy: `Deliverable-4/irs_app.py`
- README outline: `Deliverable-4/README.md`
- Recording instructions: `Deliverable-4/Loom-Instructions.docx`

### Learning outcomes

- Connect Python to MySQL.
- Divide application behavior into testable functions.
- Implement all four CRUD verbs with SQL.
- Use parameterized queries and transactions.
- Validate and normalize terminal input.
- Convert database constraints into clear user-facing feedback.
- Keep secrets out of source code.

## Deliverable 5: Flask web application and analytics

### Goal

The fifth deliverable extended the program with a user-friendly interface and complex SQL covering the categories in the grading criteria.

### Application structure

```text
Deliverable-5/
  database/
    irs_project_db.sql
    load_data.sql
    fakedata/
  flask_app/
    app.py
    static/style.css
    templates/
      index.html
      taxpayers.html
      create_taxpayer.html
      edit_taxpayer.html
      delete_taxpayer.html
      taxreturns.html
      create_taxreturn.html
      edit_taxreturn.html
      delete_taxreturn.html
      analytics.html
      analytics_result.html
```

`app.py` contains database connection logic, routes, SQL, validation, chart-data preparation, and template rendering. Templates define each page. The shared CSS styles navigation, tables, and action buttons.

### Flask routes and HTTP methods

| Route group | Methods | Role |
|---|---|---|
| `/` | GET | Home page |
| `/taxpayers` | GET | Read all taxpayers |
| `/taxpayers/create` | GET, POST | Show form and insert taxpayer |
| `/taxpayers/edit/<id>` | GET, POST | Show form and update taxpayer |
| `/taxpayers/delete/<id>` | GET, POST | Confirm and conditionally delete taxpayer |
| `/taxreturns` | GET | Read and filter tax returns |
| `/taxreturns/create` | GET, POST | Show form and insert return |
| `/taxreturns/edit/<id>` | GET, POST | Show form and update return |
| `/taxreturns/delete/<id>` | GET, POST | Confirm and conditionally delete return |
| `/analytics` | GET | Analytics menu |
| Four `/analytics/...` routes | GET | Execute filters, render results, and prepare charts |

GET reads or displays a form. POST submits a state-changing form. Successful writes return `redirect(...)`, which implements the post-redirect-get pattern and avoids an immediate repeat submission on refresh.

### Database connectivity and credentials

```python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="irs_project_db"
    )
```

`os.getenv` reads the password from the process environment. The README shows how to set it in PowerShell before running `python app.py`.

Dictionary cursors let templates and route code access columns by names such as `row["OutcomeType"]` rather than tuple positions.

### CRUD behavior

**Taxpayer pages.** View, create, edit, and protected delete are implemented. Forms preserve values on validation errors. Edit keeps the taxpayer ID read-only.

**Tax-return pages.** View, create, edit, and protected delete are implemented. The list joins `TaxReturn` to `Taxpayer` so it can display both IDs and names. Optional query-string filters add parameterized `WHERE` conditions for year and filing status.

**Protected delete.** A taxpayer cannot be deleted while returns reference it. A tax return cannot be deleted while any row exists in `IncomeRecord`, `Deduction`, `TaxCredit`, `Refund`, `BalanceDue`, or `TaxForm`.

### Form handling and validation

HTML provides the first layer:

- `<input>`, `<select>`, `<option>`, and `<button>` elements create forms and controls.
- `required` blocks empty required fields in normal browser submission.
- `type="number"`, `type="date"`, `step="0.01"`, `min="0"`, and `maxlength="1"` constrain input.
- `readonly` protects displayed primary keys during edit.

Flask provides a second layer for selected fields:

- Taxpayer creation checks numeric ID, exact five-digit ZIP, and the allowed state list.
- Taxpayer edit checks exact five-digit ZIP.
- Return creation checks exact four-digit return ID, exact four-digit year, and allowed filing status.
- Return edit checks numeric year and allowed filing status.
- MySQL supplies the final layer for primary keys, foreign keys, required columns, filing status, and nonnegative values.

The layers complement one another, but server-side checks are not fully consistent. The return edit route accepts any all-numeric year length despite displaying an exact-four-digit error message. State and several required-field checks rely on browser controls and database constraints rather than repeated server validation.

### Jinja templates

Templates use:

- `{{ ... }}` to print values.
- `{% for ... %}` to repeat table rows and select options.
- `{% if ... %}` to show errors, preserve selected filters, and choose chart configuration.
- `url_for('static', filename='style.css')` to load shared CSS.
- `|tojson` to safely serialize Python lists into JavaScript arrays.
- `loop.last` to format dynamic JavaScript dataset lists.

The shared analytics template dynamically builds its table headers from `results[0].keys()` and row cells from `row.values()`. This allows the same page to display four reports with different columns.

### CSS and interface design

`static/style.css` supplies a neutral page background, full-width collapsed-border tables, dark headers, alternating rows, hover behavior, colored create, edit, and delete buttons, and a persistent top navigation style. Individual templates also contain page-specific inline style blocks.

The navigation clearly distinguishes working sections from WIP sections. This accurately communicates scope, although future work could use a shared base template to remove repeated navigation markup.

### Analytics integration

**Report 1, set operation.** Two compatible `SELECT` statements for refunds and balances due are joined with `UNION ALL`. Python counts each outcome to create pie-chart values.

**Report 2, set membership and comparison.** `IN` keeps returns that appear in `Deduction`. `>= ALL` compares one return's deductions with every return in the same filing-status and year group, preserving ties.

**Report 3, CTE and OLAP.** A `WITH RefundData` CTE aggregates deductions, joins refunds, and assigns `NTILE(4)` within each year. The outer query adds a quartile-level windowed average and rank.

**Report 4, windowed trends.** `AVG OVER` calculates group mean income, `SUM OVER ... ROWS UNBOUNDED PRECEDING` calculates cumulative income by filing date, and `COUNT OVER` supplies group size. Python groups rows into Chart.js line datasets.

### Chart.js and JavaScript

`analytics_result.html` loads Chart.js from jsDelivr. Flask supplies chart type, labels, values, colors, or multiple datasets. A short JavaScript block calls `new Chart(...)` with those serialized values.

Purpose: retain the exact SQL result table while adding a visual summary appropriate to the report.

### Error handling and transaction control

CRUD writes use `try`, `except mysql.connector.Error`, `commit`, and `rollback`. Error templates preserve user input and highlight selected fields. Several handlers display the connector's raw error text, which is useful during development but should be replaced with a logged internal error and a safer public message in a production system.

Read and analytics routes do not wrap connection and query execution in equivalent error handling or `finally` cleanup. The submitted coursework application also ran with `debug=True` and had no CSRF protection or `requirements.txt`. The public portfolio copy now defaults debug mode to off and supplies dependency documentation; the remaining items are reasonable improvement targets if the prototype is reused.

### Example locations

- Final archive: `Deliverable-5/Deliverable-5_Zhao Li.zip`
- Backend: `Deliverable-5/flask_app/app.py`
- Templates: `Deliverable-5/flask_app/templates/`
- Shared stylesheet: `Deliverable-5/flask_app/static/style.css`
- Setup and feature guide: `Deliverable-5/README.md`
- Analytics and demo rationale: `Deliverable-5/Deliverable-5-Demo-Script.md`
- Database setup: `Deliverable-5/database/`

### Learning outcomes

- Map URL routes and HTTP methods to CRUD operations.
- Pass browser form and filter values to parameterized SQL.
- Render database results with Jinja loops and conditionals.
- Combine browser, server, and database validation.
- Use redirects, commits, rollbacks, and protected deletes.
- Adapt analytical SQL into interactive reports.
- Prepare data structures for client-side charts.
- Use environment variables for secrets.
- Recognize the additional concerns needed for production security, reuse, and error handling.

## Cross-deliverable lessons to retain

1. **Design rules need enforcement plans.** A statement in an ERD is not automatically a constraint. Decide whether each rule belongs in a key, `CHECK`, unique constraint, trigger, procedure, transaction, or application validation.
2. **Generate related data from parent data.** Reading `TaxReturn.csv` to produce child rows preserves referential integrity better than generating every table independently.
3. **Aggregate before joining multiple child tables.** This prevents accidental row multiplication and incorrect sums.
4. **Use window functions when detail rows must remain visible.** `GROUP BY` collapses rows; `OVER` adds group context without losing them.
5. **Parameterize values.** Do not concatenate user values into SQL.
6. **Treat transactions as a user-facing feature.** Confirmation, commit, rollback, and helpful delete messages make integrity understandable.
7. **Keep secrets and environment-specific paths out of source.** Deliverable 5's environment variable and relative data paths are more portable than the earlier versions.
8. **Keep deployment scripts rerunnable.** Separate schema creation, seed data, migrations, demonstrations, and deliberately failing tests so a new environment can be rebuilt predictably.
9. **Validate on the server even when HTML validates.** Browser controls improve usability but can be bypassed.
10. **Refactor repeated UI structure.** A Flask base template and shared form components would reduce repeated navigation and style markup.

## Verification note

This guide is based on the actual project sources and submitted archive contents. It distinguishes requested features from verified source implementation and identifies post-submission variants where hashes differed. The review did not start a live MySQL instance or execute the Flask application, so saved query outcomes and demo behavior were checked against source, screenshots, README findings, and the demo script rather than reproduced in a fresh runtime.
