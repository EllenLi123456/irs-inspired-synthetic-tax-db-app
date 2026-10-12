# Database Setup

These scripts provide a clean, portfolio-safe setup path without the exploratory statements and intentional error demonstrations in the submitted coursework SQL.

## Run from the repository root

The relative paths in these scripts are resolved from the directory where the MySQL client is launched, not from the directory containing the SQL file.

For the simplest Windows and VS Code workflow:

1. In VS Code, choose **File > Open Folder** and select `GitHub-Portfolio`.
2. Choose **Terminal > New Terminal**.
3. Confirm that the terminal is in the repository root:

```powershell
Get-Location
Test-Path .\database\01_schema.sql
```

The first command should show a path ending in `GitHub-Portfolio`. The second command should return `True`. If needed, change directories first:

```powershell
Set-Location -LiteralPath "C:\path\to\GitHub-Portfolio"
```

4. From that same terminal, start the MySQL client with local file loading enabled:

```powershell
mysql --local-infile=1 -u root -p
```

5. Run these commands inside the MySQL client:

```sql
SOURCE database/01_schema.sql
SOURCE database/02_load_seed_data.sql
SOURCE database/03_database_features.sql
```

Forward slashes are intentional and work in MySQL client paths on Windows. The loader uses paths such as `database/data/Taxpayer.csv`, which are correct only when MySQL was launched from the repository root. If a `SOURCE` or `LOAD DATA LOCAL INFILE` path is not found, run `quit`, return to the repository root in PowerShell, and launch MySQL again.

## Verification status

The clean schema logic was manually verified in the separate `irs_portfolio_test` database and created all eight tables. Fresh CSV loading, execution of `03_database_features.sql` against that test database, and complete database reproduction from scratch were not completed. The expected counts below come from static inspection of the included CSV files, not a fresh loading test.

The packaged CSV seed contains 25 taxpayers and 25 tax returns, all for tax year 2025. The final course database was later expanded in SQL to 35 tax returns, with 10 additional 2023 returns. Those later rows were not exported back into the submitted CSV files, so this clean setup intentionally recreates the verifiable 25-return seed rather than claiming to reproduce the final 35-row database.

Expected seed counts:

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

The CSV data is synthetic. MySQL 8.0 or later is recommended because the project uses check constraints, common table expressions, and window functions. The test database is separate from this repository and should not be deleted or changed as part of publication cleanup.
