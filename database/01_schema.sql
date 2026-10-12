-- Reproducible schema for the CS 727 IRS database portfolio.
-- Run this file before 02_load_seed_data.sql and 03_database_features.sql.

CREATE DATABASE IF NOT EXISTS irs_project_db;
USE irs_project_db;

CREATE TABLE Taxpayer (
    TaxpayerID INT,
    FirstName VARCHAR(50) NOT NULL,
    MiddleInitial CHAR(1),
    LastName VARCHAR(50) NOT NULL,
    StreetAddress VARCHAR(100) NOT NULL,
    ApartmentNumber VARCHAR(20),
    City VARCHAR(50) NOT NULL,
    State CHAR(2) NOT NULL,
    ZIPCode VARCHAR(10) NOT NULL,
    PRIMARY KEY (TaxpayerID)
);

CREATE TABLE TaxReturn (
    ReturnID INT,
    TaxpayerID INT NOT NULL,
    TaxYear INT NOT NULL,
    FilingStatus VARCHAR(10) NOT NULL,
    FilingDate DATE NOT NULL,
    TotalIncome DECIMAL(12,2) NOT NULL,
    AdjustedGrossIncome DECIMAL(12,2) NOT NULL,
    TotalDeductions DECIMAL(12,2) NOT NULL,
    TaxableIncome DECIMAL(12,2) NOT NULL,
    TotalNonrefundableCredits DECIMAL(12,2) NOT NULL,
    TotalTax DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (ReturnID),
    FOREIGN KEY (TaxpayerID) REFERENCES Taxpayer(TaxpayerID),
    CHECK (FilingStatus IN ('Single', 'MFJ', 'MFS', 'HOH', 'QSS')),
    CHECK (TotalIncome >= 0),
    CHECK (AdjustedGrossIncome >= 0),
    CHECK (TotalDeductions >= 0),
    CHECK (TaxableIncome >= 0),
    CHECK (TotalNonrefundableCredits >= 0),
    CHECK (TotalTax >= 0)
);

CREATE TABLE IncomeRecord (
    IncomeID INT,
    ReturnID INT NOT NULL,
    IncomeType VARCHAR(50) NOT NULL,
    Amount DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (IncomeID),
    FOREIGN KEY (ReturnID) REFERENCES TaxReturn(ReturnID),
    CHECK (Amount >= 0)
);

CREATE TABLE Deduction (
    DeductionID INT,
    ReturnID INT NOT NULL,
    DeductionType VARCHAR(50) NOT NULL,
    Amount DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (DeductionID),
    FOREIGN KEY (ReturnID) REFERENCES TaxReturn(ReturnID),
    CHECK (Amount >= 0)
);

CREATE TABLE TaxCredit (
    CreditID INT,
    ReturnID INT NOT NULL,
    CreditType VARCHAR(50) NOT NULL,
    Amount DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (CreditID),
    FOREIGN KEY (ReturnID) REFERENCES TaxReturn(ReturnID),
    CHECK (Amount >= 0)
);

CREATE TABLE Refund (
    RefundID INT,
    ReturnID INT NOT NULL,
    RefundAmount DECIMAL(12,2) NOT NULL,
    RefundDate DATE,
    RefundStatus VARCHAR(20) NOT NULL,
    PRIMARY KEY (RefundID),
    FOREIGN KEY (ReturnID) REFERENCES TaxReturn(ReturnID),
    CHECK (RefundAmount >= 0)
);

CREATE TABLE BalanceDue (
    BalanceDueID INT,
    ReturnID INT NOT NULL,
    AmountDue DECIMAL(12,2) NOT NULL,
    DueDate DATE,
    BalanceStatus VARCHAR(20) NOT NULL,
    PRIMARY KEY (BalanceDueID),
    FOREIGN KEY (ReturnID) REFERENCES TaxReturn(ReturnID),
    CHECK (AmountDue >= 0)
);

CREATE TABLE TaxForm (
    TaxFormID INT,
    ReturnID INT NOT NULL,
    FormType VARCHAR(50) NOT NULL,
    PRIMARY KEY (TaxFormID),
    FOREIGN KEY (ReturnID) REFERENCES TaxReturn(ReturnID)
);
