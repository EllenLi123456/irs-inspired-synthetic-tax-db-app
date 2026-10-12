## 1. Application Overview

This project designs a relational database for organizing individual federal income tax return information. The database is inspired by IRS Form 1040 and is designed to store and connect high-level information about taxpayers, tax returns, income, deductions, tax credits, refunds, balances due, and associated tax forms. (IRS Form 1040, 2025)

The purpose of the database is to provide a structured way for different users to retrieve individual return information and analyze patterns across multiple tax returns. 

## 2. Users and User Needs

| User | Role and User Needs | How the Database Helps |
|---|---|---|
| **Tax Processing Employee** | Retrieves and reviews individual taxpayer returns and related information. | Connects each taxpayer to returns, income, deductions, credits, forms, refunds, and balances due, allowing the employee to retrieve a complete return record. |
| **Tax Analyst** | Compares tax return information across taxpayers and tax years to understand tax-related patterns. | Provides structured income, deduction, credit, filing-status, tax-form, refund, and balance-due data that can be grouped and compared. |
| **Tax Software Engineer** | Uses tax return data to develop and test tax-related applications and verify data relationships. | Provides structured and related tax data that can be used to retrieve test cases, verify relationships, and test application behavior. |
| **Data Analyst / Data Scientist** | Analyzes groups of tax returns to identify patterns, comparisons, and trends. | Supports aggregate analysis across tax years, filing statuses, income types, tax forms, refunds, balances due, and other return characteristics. |

### 2.1 Interesting Use Cases

1. **Retrieve Taxpayer Return Information**  
   Retrieve a taxpayer's return for a selected tax year and review the related income, deductions, credits, tax forms, and refund or balance-due information.

2. **Compare Income by Tax Year and Filing Status**  
   Compare income across different tax years or filing statuses to identify differences among groups of returns.

3. **Analyze Income Sources and Tax Forms**  
   Compare returns based on different income types or associated tax forms, such as Schedule C.

4. **Analyze Refund and Balance-Due Outcomes**  
   Compare which returns result in a refund, a balance due, or neither, and examine how those outcomes differ across groups.

5. **Analyze Deductions and Tax Credits**  
   Compare deduction and tax-credit amounts by tax year, filing status, or type.

6. **Analyze Tax Return Trends Over Time**  
   Examine changes in taxable income, total tax, refunds, or other return information across multiple tax years.

7. **Identify High-Value Returns**  
   Identify and rank returns with the highest total income, total tax, refund amount, or balance due.

## 3. Entity Relationship Diagram

The ERD below represents the eight entities in the database and their relationships. Primary keys (PK), foreign keys (FK), and relationship cardinalities are included in the diagram.

```text
┌──────────────────────┐                         ┌──────────────────────────────┐
│       TAXPAYER       │                         │          TAX_RETURN          │
├──────────────────────┤ 1..1 --- files --- 0..* ├──────────────────────────────┤
│ TaxpayerID {PK}      │─────────────────────────│ ReturnID {PK}                │
│ FirstName            │                         │ TaxpayerID {FK}              │
│ MiddleInitial        │                         │ TaxYear                      │
│ LastName             │                         │ FilingStatus                 │
│ StreetAddress        │                         │ FilingDate                   │
│ ApartmentNumber      │                         │ TotalIncome                  │
│ City                 │                         │ AdjustedGrossIncome          │
│ State                │                         │ TotalDeductions              │
│ ZIPCode              │                         │ TaxableIncome                │
└──────────────────────┘                         │ TotalNonrefundableCredits    │
                                                 │ TotalTax                     │
                                                 └──────────────┬───────────────┘
                                                                │
                     ┌──────────────────────────────────────────┼─────────────────────────────────────────┐
               1..1  │              1..1  │               1..1  │              1..1  │              1..1  │
                  contains             contains              contains             may have             may have
                     │                    │                     │                    │                    │ 
                     │                    │                     │                    │                    │
                     ▼  0..*              ▼  0..*               ▼  0..*              ▼  0..1              ▼  0..1

          ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
          │  INCOME_RECORD   │   │    DEDUCTION     │   │    TAX_CREDIT    │   │      REFUND      │   │   BALANCE_DUE    │
          ├──────────────────┤   ├──────────────────┤   ├──────────────────┤   ├──────────────────┤   ├──────────────────┤
          │ IncomeID {PK}    │   │ DeductionID {PK} │   │ CreditID {PK}    │   │ RefundID {PK}    │   │ BalanceDueID {PK}│
          │ ReturnID {FK}    │   │ ReturnID {FK}    │   │ ReturnID {FK}    │   │ ReturnID {FK}    │   │ ReturnID {FK}    │
          │ IncomeType       │   │ DeductionType    │   │ CreditType       │   │ RefundAmount     │   │ AmountDue        │
          │ Amount           │   │ Amount           │   │ Amount           │   │ RefundDate       │   │ DueDate          │
          │                  │   │                  │   │                  │   │ RefundStatus     │   │ BalanceStatus    │
          └──────────────────┘   └──────────────────┘   └──────────────────┘   └──────────────────┘   └──────────────────┘


                                                 ┌──────────────────────────────┐
                                                 │          TAX_RETURN          │
                                                 └──────────────┬───────────────┘
                                                         1..1   │
                                                             includes
                                                                │ 
                                                                │
                                                                ▼  1..*
                                                 ┌──────────────────────────────┐
                                                 │           TAX_FORM           │
                                                 ├──────────────────────────────┤
                                                 │ TaxFormID {PK}               │
                                                 │ ReturnID {FK}                │
                                                 │ FormType                     │
                                                 └──────────────────────────────┘
```
## 4. Relational Schemas and Data Design

### 4.1 Relational Schemas

**Taxpayer** (**TaxpayerID [PK]**, FirstName, MiddleInitial, LastName, StreetAddress, ApartmentNumber, City, State, ZIPCode)

**TaxReturn** (**ReturnID [PK]**, TaxpayerID [FK], TaxYear, FilingStatus, FilingDate, TotalIncome, AdjustedGrossIncome, TotalDeductions, TaxableIncome, TotalNonrefundableCredits, TotalTax)

**IncomeRecord** (**IncomeID [PK]**, ReturnID [FK], IncomeType, Amount)

**Deduction** (**DeductionID [PK]**, ReturnID [FK], DeductionType, Amount)

**TaxCredit** (**CreditID [PK]**, ReturnID [FK], CreditType, Amount)

**Refund** (**RefundID [PK]**, ReturnID [FK], RefundAmount, RefundDate, RefundStatus)

**BalanceDue** (**BalanceDueID [PK]**, ReturnID [FK], AmountDue, DueDate, BalanceStatus)

**TaxForm** (**TaxFormID [PK]**, ReturnID [FK], FormType)

**PK** = Primary Key  
**FK** = Foreign Key

### 4.2 Data and Semantics

| Entity | Data and Semantics |
|---|---|
| **Taxpayer** | Stores the taxpayer's name and address information. (IRS Form 1040, 2025) |
| **TaxReturn** | Stores the main information from a taxpayer's federal income tax return for a specific tax year, such as filing status, income, deductions, taxable income, credits, and total tax. (IRS Form 1040, 2025) |
| **IncomeRecord** | Stores the types of income reported on a tax return and their amounts. (IRS Form 1040, 2025) |
| **Deduction** | Stores the types of deductions reported on a tax return and their amounts. (IRS Form 1040, 2025) |
| **TaxCredit** | Stores the types of tax credits reported on a tax return and their amounts. (IRS Form 1040, 2025) |
| **Refund** | Stores refund information when a tax return results in a refund (IRS Form 1040, 2025). The database also tracks the refund date and status. |
| **BalanceDue** | Stores balance-due information when a tax return results in an amount owed (IRS Form 1040, 2025). The database also tracks the due date and status. |
| **TaxForm** | Stores the forms and schedules associated with a tax return, such as Form 1040 or Schedule C. (IRS Form 1040, 2025; IRS Schedules for Form 1040) |

### 4.3 Relationships and Constraints

| Relationship | Cardinality | Constraint |
|---|---|---|
| **Taxpayer → TaxReturn** | 1..1 → 0..* | Each tax return belongs to one taxpayer. A taxpayer may have zero or multiple tax returns. |
| **TaxReturn → IncomeRecord** | 1..1 → 0..* | Each income record belongs to one tax return. A tax return may contain zero or multiple income records. |
| **TaxReturn → Deduction** | 1..1 → 0..* | Each deduction belongs to one tax return. A tax return may contain zero or multiple deductions. |
| **TaxReturn → TaxCredit** | 1..1 → 0..* | Each tax credit belongs to one tax return. A tax return may contain zero or multiple tax credits. |
| **TaxReturn → Refund** | 1..1 → 0..1 | Each refund belongs to one tax return. A tax return may have zero or one refund. |
| **TaxReturn → BalanceDue** | 1..1 → 0..1 | Each balance due belongs to one tax return. A tax return may have zero or one balance due. |
| **TaxReturn → TaxForm** | 1..1 → 1..* | Each tax form belongs to one tax return. A tax return must include one or more tax forms. |

#### Additional Constraints

- For each taxpayer and tax year, only the most current IRS-accepted return is stored. If an amended return is accepted, it replaces the previously stored version.
- A `TaxReturn` may have a `Refund`, a `BalanceDue`, or neither, but it cannot have both.
- `FilingStatus` must use one of the allowed values: `Single`, `MFJ`, `MFS`, `HOH`, or `QSS`. (IRS Instructions for Form 1040, 2025)
- Every child record in `IncomeRecord`, `Deduction`, `TaxCredit`, `Refund`, `BalanceDue`, and `TaxForm` must reference an existing `TaxReturn`.
- Every `TaxReturn` must include at least one `TaxForm`, including Form 1040.
- `MiddleInitial` and `ApartmentNumber` are optional. All other attributes are required when their associated record exists.

### 4.4 Normalization Note

As an additional design check, the final relational schemas were reviewed through Third Normal Form (3NF).

## 5. References

1. **IRS Form 1040 (2025)**  
   Used as the primary reference for the high-level tax return data and Form 1040 line items represented in the database.  
   https://www.irs.gov/pub/irs-pdf/f1040.pdf

2. **IRS Instructions for Form 1040 (2025)**  
   Used to understand the meaning of Form 1040 information, including filing status, income, deductions, credits, refunds, and amounts owed.  
   https://www.irs.gov/pub/irs-pdf/i1040gi.pdf

3. **IRS Schedules for Form 1040 and Form 1040-SR**  
   Used to identify and understand the additional forms and schedules that may be associated with Form 1040, such as Schedule C.  
   https://www.irs.gov/forms-pubs/schedules-for-form-1040
