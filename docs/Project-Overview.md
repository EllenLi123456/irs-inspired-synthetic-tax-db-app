# CS 727 IRS Database Project Overview

## My read

This project successfully developed one IRS-inspired data system through five connected stages: relational design, MySQL implementation, analytical SQL, a Python command-line CRUD program, and a Flask web application with interactive analytics. The strongest through-line is the reuse of the same eight-table model and business questions across every deliverable.

The final application is a local educational prototype built with synthetic data. It is not an IRS production system, and several rules described in the design are checked by application logic or review queries rather than fully enforced by database constraints.

### Project highlights (Markdown fallback)

| Metric | Verified value |
|---|---:|
| Relational database tables | 8 |
| Analytical SQL queries | 15 |
| Application interfaces | 2, Python CLI and Flask web app |
| Interactive Flask analytics reports | 4 |

## Project background and objective

The project was completed for CS 727, Relational Database Implementation and Applications. Its objective was to build an application with a relational database backend, starting from a real-world domain and progressing from design to implementation, querying, and an end-user interface.

The chosen domain was individual federal income tax returns, inspired by IRS Form 1040. The database organizes high-level information about taxpayers, tax returns, income, deductions, tax credits, refunds, balances due, and associated forms. The project uses fictional, synthetically generated records.

The intended users identified in Deliverable 1 were tax-processing employees, tax analysts, tax software engineers, and data analysts or data scientists. Their use cases included retrieving a complete return, comparing filing groups or years, analyzing tax outcomes, and ranking high-value returns.

## Executive summary

The completed project contains:

- An eight-entity relational design reviewed through Third Normal Form.
- A MySQL schema with primary keys, foreign keys, allowed filing-status checks, and nonnegative financial-value checks.
- Synthetic CSV data produced with Python, Faker, `csv`, `random`, and `datetime`.
- Data loading with MySQL `LOAD DATA LOCAL INFILE`.
- Database review and maintenance using a temporary table, a view, a stored procedure, a stored function, a trigger, and validation queries.
- Fifteen SQL analyses using joins, grouped aggregates, derived tables, `WITH`, `ROLLUP`, and window functions.
- A Python command-line application that performs CRUD on `Taxpayer` records.
- A Flask application that performs CRUD on `Taxpayer` and `TaxReturn` records, filters returns, validates inputs, protects related records from deletion, and displays four analytical reports with Chart.js charts.

## How the deliverables build on one another

```mermaid
flowchart LR
    D1[Deliverable 1<br/>Model the domain and rules] --> D2[Deliverable 2<br/>Create MySQL schema and synthetic data]
    D2 --> D3[Deliverable 3<br/>Test 15 analytical SQL queries]
    D3 --> D4[Deliverable 4<br/>Build Python command-line CRUD]
    D4 --> D5[Deliverable 5<br/>Extend to Flask CRUD and analytics UI]
```

### Deliverable 1: relational database design

**Goal.** Identify the important data, users, relationships, constraints, and use cases, then represent the design as an ERD and relational schemas.

**Final result.** The submitted PDF and its Markdown source define eight entities, their keys and cardinalities, seven practical use cases, and a normalization note. The design establishes `TaxReturn` as the central transaction entity between `Taxpayer` and six detail or outcome entities.

**Primary final files.** `Deliverable-1/Deliverable-1_Zhao Li.pdf` is the submitted document. `Deliverable-1/Final-Deliverable-1.md` is the matching editable source. `Deliverable-1/Final-Deliverable-1-DRAFT.md` is an earlier draft. The numbered Markdown files in this folder are supporting research, design, checklist, ERD, and reference materials.

### Deliverable 2: database creation and loading

**Goal.** Build the relational design in MySQL, load realistic mock data, and demonstrate database objects and business logic.

**Final result.** The submitted archive contains the schema, CSV files, Python data generators, loading script, screenshots, and README. The work creates all eight tables, loads initial data, adds prior-year returns so every table reaches at least 15 records, repairs missing child data, reviews relationships, classifies income with a stored function, and protects the refund versus balance-due rule with a stored procedure and trigger.

**Primary final files.** `Deliverable-2/Deliverable_2_Zhao Li.zip` is the submission archive. Its extracted counterpart is `Deliverable-2/Deliverable_2_Zhao Li/`. The archive and extracted folder match except for `load_data.sql`: the submitted version uses absolute course-environment paths, while the later extracted version uses portable relative paths and adds three missing count checks. `irs_project_db_4-9.sql` is a later working copy of sections 4 through 9, not part of the submitted archive.

### Deliverable 3: SQL querying and analytics

**Goal.** Execute at least 15 varied queries, including advanced window and OLAP features, and document each question and result.

**Final result.** The deliverable contains 15 business questions, their SQL, plain-language findings, and one result screenshot per query. The sequence moves from ranking and distributions to running totals, multidimensional grouping, outcome analysis, and a CTE-based refund analysis.

**Primary final files.** `Deliverable-3/irs_project_queries.sql`, `Deliverable-3/README.md`, and `Deliverable-3/query_results/query_01_result.png` through `query_15_result.png` form the final submission materials.

### Deliverable 4: Python command-line CRUD application

**Goal.** Connect a program to MySQL and demonstrate Create, Read, Update, and Delete operations.

**Final result.** A menu-driven Python application uses `mysql.connector` for database access and `tabulate` for readable terminal tables. It can list taxpayers, find one by ID, create a taxpayer, update selected fields, and delete a taxpayer only when no tax returns reference it. It includes confirmation and cancellation flows, field validation, parameterized queries, commits, rollbacks, and a top-level MySQL exception handler.

**Primary final files.** `Deliverable-4/Deliverable-4.zip` is the submitted archive containing `irs_app.py` and `README.md`. The standalone `Deliverable-4/irs_app.py` has one later change, `connection.autocommit = True`, and therefore is not byte-identical to the submitted program. The README is an outline rather than complete user documentation.

### Deliverable 5: Flask web application and complex analytics

**Goal.** Extend the CRUD application with a user-friendly web interface and challenging SQL covering set operations, membership, comparison, common table expressions, advanced aggregates, and OLAP.

**Final result.** The final ZIP contains a Flask application, templates, CSS, MySQL setup files, synthetic data, a README, and the demonstration video. The application supports full CRUD pages for `Taxpayer` and `TaxReturn`, protected deletes, return filtering, server-side and HTML validation, and four analytics reports rendered as tables and pie, bar, or line charts. Income, deductions, credits, refunds, balance due, and forms appear in navigation as work-in-progress areas, but they do not have CRUD pages.

**Primary final files.** `Deliverable-5/Deliverable-5_Zhao Li.zip` is the submission archive. The source files under `Deliverable-5/database/` and `Deliverable-5/flask_app/` are byte-identical to the corresponding files in the archive for the checked core files. `Deliverable-5/Deliverable 5_Zhao Li.mp4` is the submitted demonstration recording. The checklist and demo script are supporting planning and presentation materials.

### Dataset evolution and verified tax-return counts

The project files support the following count history:

| Stage | Verified or documented count | Evidence and interpretation |
|---|---:|---|
| Deliverable 2 initial CSV data | 25 | Both the submitted ZIP and extracted `fakedata/TaxReturn.csv` contain 25 data rows, with ReturnIDs 1001 through 1025. `fake_taxreturn.py` also sets `number_of_returns = 25`. |
| Deliverable 2 reviewed database state | 35 | `irs_project_db.sql` documents a final state of 25 returns for 2025 plus 10 added returns for 2023. This is the count reported by the SQL review comments and supporting Deliverable 2 documentation. |
| Deliverable 3 analysis | 35 | `Deliverable-3/README.md` explicitly states that Query 5 divides 35 tax returns into quartiles. The analytical work therefore reflects the reviewed 35-return state. |
| Deliverable 4 runtime | Not recorded | The command-line application connects to an existing MySQL database but does not include a database export or saved return-count result. |
| Deliverable 5 packaged database files | 25 initial, 35 documented target | The final ZIP again contains a 25-row `TaxReturn.csv`. Its `database/irs_project_db.sql` is byte-identical to the Deliverable 2 main SQL and documents the same 35-return reviewed state. |

No project CSV, SQL dump, README statement, saved count output, or final submission file reviewed here confirms a 60-return dataset. A 60-row database may have existed during later interactive development, but that state was not exported into the reviewed project files and remains unverified. The documentation therefore uses 35 only for the Deliverable 2 and Deliverable 3 state that the files explicitly support, and it does not claim that the live database used at every later moment had the same count.

## Database architecture

### Tables and relationships

| Parent | Child | Implemented relationship | Intended cardinality |
|---|---|---|---|
| `Taxpayer` | `TaxReturn` | `TaxReturn.TaxpayerID` foreign key | One taxpayer to zero or many returns |
| `TaxReturn` | `IncomeRecord` | `IncomeRecord.ReturnID` foreign key | One return to zero or many income records |
| `TaxReturn` | `Deduction` | `Deduction.ReturnID` foreign key | One return to zero or many deductions |
| `TaxReturn` | `TaxCredit` | `TaxCredit.ReturnID` foreign key | One return to zero or many credits |
| `TaxReturn` | `Refund` | `Refund.ReturnID` foreign key | One return to zero or one refund |
| `TaxReturn` | `BalanceDue` | `BalanceDue.ReturnID` foreign key | One return to zero or one balance due |
| `TaxReturn` | `TaxForm` | `TaxForm.ReturnID` foreign key | One return to one or many forms |

`Taxpayer` stores identity and mailing address data. `TaxReturn` stores the filing year, status, date, and summary financial figures. `IncomeRecord`, `Deduction`, and `TaxCredit` decompose repeating financial items into separate child rows. `Refund` and `BalanceDue` represent alternative outcomes. `TaxForm` records Form 1040 and optional schedules.

This separation reduces repeated data and supports the stated 3NF objective. For example, a taxpayer address is stored once, while multiple tax returns can reference the taxpayer. Repeating income or deduction types are stored as rows rather than columns.

### Implemented constraints

- Every table has a single-column primary key.
- All child tables have foreign keys to their parent.
- `TaxReturn.FilingStatus` is restricted to `Single`, `MFJ`, `MFS`, `HOH`, or `QSS`.
- Summary financial values and child amounts use `CHECK` constraints to prevent negative values.
- Required fields use `NOT NULL`; `MiddleInitial`, `ApartmentNumber`, `RefundDate`, and `DueDate` are nullable in the SQL schema.
- MySQL creates indexes for primary keys and requires indexes for foreign-key columns. The script reviews these with `SHOW INDEX`.

## End-to-end development workflow

1. Study Form 1040 and identify the scope, entities, attributes, users, and business questions.
2. Draw the ERD, select primary and foreign keys, define cardinalities, and review the schemas for 3NF.
3. Translate the design into MySQL `CREATE TABLE` statements and constraints.
4. Generate repeatable fictional data with Python and Faker, write CSV files, and load them with `LOAD DATA LOCAL INFILE`.
5. Review table counts and relationships, identify insufficient or missing data, stage corrections in a temporary table, and add related child rows.
6. Create reusable database logic with a view, stored procedure, stored function, and trigger.
7. Explore the data with 15 SQL queries and save result screenshots.
8. Connect Python to MySQL and implement menu-driven CRUD with transactions and validation.
9. Move the interaction layer to Flask routes and Jinja templates, add CSS and browser forms, then integrate complex SQL reports and Chart.js visualizations.

## How the final application works

### Browser to Flask to MySQL

The browser sends `GET` requests to display lists, edit pages, filters, and analytics. It sends `POST` requests when a user creates, edits, or confirms deletion. Flask reads form or query-string values, performs validation, executes parameterized SQL through `mysql.connector`, commits successful changes, rolls back failures, and renders Jinja templates with query results and error messages.

The MySQL password is read from the `MYSQL_PASSWORD` environment variable in Deliverable 5. This improves on Deliverable 4, where the submitted command-line program contains a hard-coded password.

### CRUD scope

**Taxpayer.** Users can list, create, edit, and delete taxpayer records. Taxpayer ID is fixed during editing. A delete is refused if related `TaxReturn` rows exist.

**Tax return.** Users can list and filter returns by tax year and filing status, create and edit return summary data, and delete a return only when none of the six child tables contains related records.

The application does not implement CRUD pages for the remaining six tables. The interface labels those areas as WIP.

### Validation and error handling

- Taxpayer creation validates a numeric ID, a five-digit ZIP code, and one of five supported state values.
- Taxpayer edit validates the ZIP code on the server. HTML `required`, `maxlength`, and select elements add browser-side checks.
- Tax return creation validates a four-digit return ID, a four-digit tax year, and an allowed filing status.
- Nonnegative financial inputs are enforced in HTML with `min="0"` and in MySQL with `CHECK` constraints.
- Database writes use parameter placeholders, `commit()`, `rollback()`, and caught connector exceptions.
- Submitted user values are preserved after many validation failures so the user can correct one field instead of re-entering the form.
- Delete confirmation pages explain when related records block deletion.

### Analytics functionality

1. **Refund and balance-due outcomes:** combines two result sets with `UNION ALL`, optionally filtered by tax year, and displays a pie chart.
2. **Highest deductions by filing status:** uses `IN` and `>= ALL` to find group maxima while preserving ties, with optional year and multi-status filters.
3. **Refunds by deduction level:** uses a `WITH` CTE, grouped `SUM`, `NTILE(4)`, windowed `AVG`, and `RANK`, with a bar chart.
4. **Filing-status income trends:** uses windowed `AVG`, cumulative `SUM`, and `COUNT`, with tax-year and multi-status filters and a line chart.

The reusable `analytics_result.html` template receives labels and values from Flask, converts them safely to JavaScript data with Jinja's `tojson`, and uses Chart.js from a CDN.

## Project Limitations and Future Enhancements

### A. Existing Implementation Limitations

These are verified gaps or constraints in the submitted implementation, not criticisms of the project's course-level accomplishments.

- **Some designed business rules are not fully enforced by the schema.** There is no `UNIQUE (TaxpayerID, TaxYear)` constraint. `Refund.ReturnID` and `BalanceDue.ReturnID` are not unique, so the intended zero-or-one relationship is not guaranteed. The trigger blocks a new `BalanceDue` when a refund exists, but there is no reciprocal refund trigger and no equivalent update protection. The requirement that every return have at least one Form 1040 is populated and reviewed procedurally rather than guaranteed by a database constraint.
- **The SQL is not a clean, rerunnable deployment script.** The main file preserves alternative development steps that reuse ReturnIDs, and its final trigger test deliberately raises an error. It records the work performed but should be executed section by section rather than assumed to rebuild the database safely from top to bottom.
- **The 60-return dataset is not preserved in the reviewed files.** The files verify 25 initial CSV returns and a documented 35-return reviewed state. Deliverables 4 and 5 do not include a live database export or saved count that proves a later 60-return state.
- **Validation is useful but inconsistent across routes.** For example, the tax-return edit route checks that the year is numeric but does not enforce the four-digit length promised by its error message. Some required, state, and numeric validations rely on HTML controls or database constraints instead of uniform server-side checks.
- **Error handling is uneven.** CRUD writes catch connector errors and roll back, while read and analytics routes do not provide equivalent handling. Some development paths expose raw database error text to the user.
- **Application scope is intentionally partial.** The web interface implements CRUD for `Taxpayer` and `TaxReturn`. Income, deductions, credits, refunds, balances due, and forms remain labeled WIP rather than having their own management pages.
- **Earlier credential handling was insecure.** The submitted Deliverable 4 program hard-codes the MySQL password. Deliverable 5 corrects this by reading `MYSQL_PASSWORD` from the environment.
- **A separate active performance index was not verified.** Primary-key and foreign-key indexes exist or are required by MySQL, but the explicit `CREATE INDEX` example remains commented out.

### B. Optional Future Enhancements

These improvements would make the prototype easier to maintain or safer to deploy, but they were not all required to complete the course project.

- Convert the database setup into ordered, idempotent schema, seed, migration, verification, and negative-test scripts.
- Add unique constraints or symmetric triggers for rules that must hold for every future write.
- Apply the same server-side validation and friendly error-handling pattern to every route and form.
- Disable Flask debug mode outside development, add CSRF protection, log internal errors, and show generic public error messages.
- Add `requirements.txt` or another dependency lock file plus environment-specific configuration guidance.
- Add automated tests for schema constraints, CRUD routes, protected deletes, validation, and analytics results.
- Introduce a shared Jinja base template and reusable form components to remove repeated navigation and markup.
- Add CRUD workflows for the six WIP entities if broader application coverage is desired.
- Export and version a database snapshot or deterministic seed process whenever a specific dataset size, such as 60 returns, is important to preserve.

## Major accomplishments

- Maintained one coherent domain model across all five deliverables.
- Converted business concepts into normalized tables and foreign-key relationships.
- Produced reproducible synthetic data with fixed random seeds.
- Detected data gaps through review queries and repaired them while keeping related tables consistent.
- Used both transactional SQL and analytical SQL, including stored programs and a broad range of window functions.
- Built two database clients, first a command-line program and then a multi-page web application.
- Added layered validation, protected deletes, transaction control, filters, and interactive charts.
- Improved credential handling between Deliverables 4 and 5 by moving the MySQL password to an environment variable.

## Technical challenges and lessons

### Preserving relationships while extending the data

The initial synthetic set did not provide at least 15 `BalanceDue` rows. The project solved this by adding prior-year returns for existing taxpayers, using a temporary table to stage calculations, calling a stored procedure that rejects a balance due when a refund already exists, and then creating the missing child rows. The relationship-summary view exposed incomplete child data and supported a second verification pass.

### Preventing unsafe deletion

Foreign keys would reject some deletes, but a raw database error is poor user experience. Both Python applications first count related rows and present an understandable refusal. This is a practical example of combining database integrity with application-level feedback.

### Moving from terminal interaction to the web

Deliverable 4 contains a long input, review, correct, confirm, commit loop. Deliverable 5 replaces this with HTTP routes, forms, redirects, persistent error values, and templates. The core SQL concepts remain the same, but state is passed through request data and rendered pages rather than a continuous terminal session.

### Reusing analytics without duplicating presentation code

Deliverable 5 adapts earlier analytical patterns and sends all four reports to one results template. That template dynamically builds filters, a chart, and a result table. This is a meaningful step toward reusable web design.

### Reproducibility and security

Fixed random seeds make the synthetic dataset repeatable. Parameterized queries reduce SQL-injection risk. Environment-variable credential loading in Deliverable 5 improves on the hard-coded credential in Deliverable 4. The consolidated limitations and optional improvements are listed in the preceding section.

## Important file map

- Design: `Deliverable-1/Deliverable-1_Zhao Li.pdf`, `Deliverable-1/Final-Deliverable-1.md`
- Database submission: `Deliverable-2/Deliverable_2_Zhao Li.zip`
- Database source: `Deliverable-2/Deliverable_2_Zhao Li/irs_project_db.sql`
- Synthetic data: `Deliverable-2/Deliverable_2_Zhao Li/fakedata/`
- Analytics SQL: `Deliverable-3/irs_project_queries.sql`
- Analytics explanations and findings: `Deliverable-3/README.md`
- Command-line submission: `Deliverable-4/Deliverable-4.zip`
- Web application submission: `Deliverable-5/Deliverable-5_Zhao Li.zip`
- Flask backend: `Deliverable-5/flask_app/app.py`
- Jinja templates: `Deliverable-5/flask_app/templates/`
- Shared CSS: `Deliverable-5/flask_app/static/style.css`
- Database setup reused by the web app: `Deliverable-5/database/`

## Review boundaries

The review inspected the assignment timeline, all five grading-criteria documents, the submitted archive inventories, the main final source files, the Deliverable 1 submitted PDF, README and supporting documentation, SQL scripts, Python generators, CSV structure, Flask templates, CSS, query-result file set, and archive-to-folder differences. The source files in the final Deliverable 5 archive were matched against the corresponding project files.

The MySQL scripts and Flask application were not executed against a live MySQL server during this documentation review. Successful behavior is supported by the source, saved screenshots, README findings, and demonstration script, but runtime behavior on a newly configured machine remains unverified. The large MP4 was identified as part of the final submission, but its audiovisual content was not transcribed. The IRS reference PDFs and the Deliverable 1 research files were treated as supporting sources rather than line-by-line implementation files.
