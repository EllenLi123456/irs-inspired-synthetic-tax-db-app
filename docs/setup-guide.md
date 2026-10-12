# Local Setup Guide

This guide explains how to run the educational IRS-inspired database project on Windows from VS Code. All included data is synthetic.

## 1. Prerequisites

Install:

- Python 3
- MySQL 8.0 or later
- Visual Studio Code
- A MySQL account allowed to create the `irs_project_db` database

MySQL must permit `LOCAL INFILE` for the CSV-loading step.

## 2. Open the correct folder

In VS Code, choose **File > Open Folder** and select the repository folder, `irs-inspired-synthetic-tax-db-app`. Then choose **Terminal > New Terminal**.

Confirm that the terminal is in the repository root:

```powershell
Get-Location
Test-Path .\database\01_schema.sql
```

The first command should end with `irs-inspired-synthetic-tax-db-app`, and the second should return `True`.

## 3. Create a Python virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, see the troubleshooting section below.

## 4. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The project uses Flask, MySQL Connector/Python, and `tabulate`. Exact historical versions were not preserved, so the requirements are intentionally unpinned.

## 5. Start the MySQL client

Remain in the repository root and run:

```powershell
mysql --local-infile=1 -u root -p
```

Enter your local MySQL password when prompted. Starting MySQL from the repository root is important because the SQL scripts use repository-relative paths.

## 6. Create the schema

Inside the MySQL client, run:

```sql
SOURCE database/01_schema.sql
```

The clean schema logic was manually verified in a separate test database and created all eight tables.

## 7. Load the synthetic CSV data

Still inside the same MySQL client session, run:

```sql
SOURCE database/02_load_seed_data.sql
```

This script uses paths such as `database/data/Taxpayer.csv`. They resolve from the directory where the MySQL client was launched.

Expected counts based on static inspection of the packaged CSV files:

| Table | Rows |
|---|---:|
| Taxpayer | 25 |
| TaxReturn | 25 |
| IncomeRecord | 55 |
| Deduction | 55 |
| TaxCredit | 34 |
| Refund | 17 |
| BalanceDue | 6 |
| TaxForm | 56 |

Fresh CSV loading was not completed during final portfolio testing, so these counts should not be presented as a fresh end-to-end test result.

## 8. Create stored database objects

Run:

```sql
SOURCE database/03_database_features.sql
```

This creates the relationship-summary view, stored procedure, income-level function, and balance-due trigger. Execution of this script against the final test database was not completed during portfolio testing.

Leave MySQL when finished:

```sql
quit
```

## 9. Configure database connection variables

Set the connection values in the PowerShell session used to start the applications:

```powershell
$env:MYSQL_PASSWORD = "your_local_password"
$env:DB_HOST = "localhost"
$env:DB_USER = "root"
$env:DB_NAME = "irs_project_db"
$env:FLASK_DEBUG = "0"
```

`.env.example` documents the supported values. The applications read process environment variables directly and do not automatically load a `.env` file.

## 10. Run the Flask application

```powershell
python web/app.py
```

Open `http://127.0.0.1:5000` in a browser. Stop the development server with `Ctrl+C` in the terminal.

## 11. Run the Python CLI

From a terminal with the virtual environment activated and the database variables set:

```powershell
python cli/irs_cli.py
```

The CLI supports Taxpayer CRUD. The Flask application supports Taxpayer and TaxReturn CRUD.

## Common Setup Problems

### `SOURCE` cannot find a SQL file

Exit MySQL with `quit`. In PowerShell, return to the repository root, verify that `Test-Path .\database\01_schema.sql` returns `True`, and launch MySQL again. `SOURCE` resolves relative paths from the MySQL client's launch directory.

### `LOAD DATA LOCAL INFILE` cannot find a CSV file

Confirm that MySQL was launched from the repository root and that `--local-infile=1` was included. Verify that `database\data\Taxpayer.csv` exists before reopening MySQL.

### Local data loading is disabled

The client and server must both permit `LOCAL INFILE`. Check your local MySQL configuration and restart the client with `--local-infile=1`.

### `mysql` is not recognized

Add the MySQL client `bin` directory to the Windows `PATH`, or run `mysql.exe` using its installed path.

### PowerShell blocks virtual-environment activation

Use a PowerShell session whose execution policy permits locally created activation scripts, or activate the environment from Command Prompt with `.venv\Scripts\activate.bat`.

### The application cannot connect to MySQL

Confirm that MySQL is running, the four database environment variables are set in the current terminal, and `DB_NAME` matches the database created by `01_schema.sql`.

## Reproducibility Boundary

The packaged seed recreates 25 tax returns for 2025. The later reviewed working database contained 35 returns after 10 records for 2023 were added through development SQL, but those rows were not exported into the packaged CSV files. Complete database reproduction from scratch has not been verified.
