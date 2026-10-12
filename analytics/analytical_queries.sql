USE irs_project_db;

-- =====================================================
-- QUERY 1
-- Business Question:
-- Does higher total income also mean higher taxable 
-- income?
-- =====================================================

SELECT
    ReturnID,
    TaxpayerID,
    FilingStatus,
    TotalIncome,
    TaxableIncome,
    RANK() OVER (
        ORDER BY TotalIncome DESC
    ) AS IncomeRank,
    RANK() OVER (
        ORDER BY TaxableIncome DESC
    ) AS TaxableIncomeRank,
    DENSE_RANK() OVER (
        ORDER BY TotalIncome DESC
    ) AS DenseRankComparison
FROM TaxReturn
ORDER BY IncomeRank;

-- =====================================================
-- QUERY 2
-- Business Question:
-- Which tax returns have the highest total income
-- within each filing status?
-- =====================================================

SELECT
    ReturnID,
    TaxpayerID,
    FilingStatus,
    TotalIncome,
    RANK() OVER (
        PARTITION BY FilingStatus
        ORDER BY TotalIncome DESC
    ) AS IncomeRank
FROM TaxReturn
ORDER BY FilingStatus, IncomeRank;

-- =====================================================
-- QUERY 3
-- Business Question:
-- Which tax returns fall toward the lower, middle,
-- or higher end of the income distribution?
-- =====================================================

SELECT
    ReturnID,
    TaxpayerID,
    FilingStatus,
    TotalIncome,
    RANK() OVER (
        ORDER BY TotalIncome
    ) AS IncomeRank,
    ROUND(
        PERCENT_RANK() OVER (
            ORDER BY TotalIncome
        ) * 100,
        2
    ) AS IncomePercentRank
FROM TaxReturn
ORDER BY TotalIncome;

-- =====================================================
-- QUERY 4
-- Business Question:
-- How does each tax return's total income compare
-- with the overall income distribution?
-- =====================================================

SELECT
    ReturnID,
    TaxpayerID,
    FilingStatus,
    TotalIncome,

    ROUND(
        PERCENT_RANK() OVER (
            ORDER BY TotalIncome
        ) * 100,
        2
    ) AS IncomePercentRank,

    ROUND(
        CUME_DIST() OVER (
            ORDER BY TotalIncome
        ) * 100,
        2
    ) AS IncomeCumeDist

FROM TaxReturn
ORDER BY TotalIncome;

-- =====================================================
-- QUERY 5
-- Business Question:
-- How can tax returns be divided into four groups
-- based on total income?
-- =====================================================

SELECT
    ROW_NUMBER() OVER (
        ORDER BY TotalIncome
    ) AS RowNumber,
    ReturnID,
    TaxpayerID,
    FilingStatus,
    TotalIncome,
    NTILE(4) OVER (
        ORDER BY TotalIncome
    ) AS IncomeQuartile
FROM TaxReturn
ORDER BY TotalIncome;

-- =====================================================
-- QUERY 6
-- Business Question:
-- How does cumulative total income grow over time
-- within each filing status?
-- =====================================================

SELECT
    ReturnID,
    FilingDate,
    FilingStatus,
    TotalIncome,
    SUM(TotalIncome) OVER (
        PARTITION BY FilingStatus
        ORDER BY FilingDate, ReturnID
        ROWS UNBOUNDED PRECEDING
    ) AS RunningTotalIncome
FROM TaxReturn
ORDER BY FilingStatus, FilingDate, ReturnID;

-- =====================================================
-- QUERY 7
-- Business Question:
-- How does each return's total income compare 
-- with the average of nearby filed returns 
-- within the same filing status?
-- =====================================================

SELECT
    ReturnID,
    FilingDate,
    FilingStatus,
    TotalIncome,
    ROUND(
        AVG(TotalIncome) OVER (
            PARTITION BY FilingStatus
            ORDER BY FilingDate, ReturnID
            ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
        ),
        2
    ) AS MovingAverageIncome
FROM TaxReturn
ORDER BY FilingStatus, FilingDate, ReturnID;

-- =====================================================
-- QUERY 8
-- Business Question:
-- How do the number of tax returns and average total
-- income differ across filing statuses?
-- =====================================================

SELECT
    FilingStatus,
    ROUND(AVG(TotalIncome), 2) AS AverageIncome,
    COUNT(ReturnID) AS NumberOfReturns
FROM TaxReturn
GROUP BY FilingStatus;

-- =====================================================
-- QUERY 9
-- Business Question:
-- How does the average total income for each filing
-- status compare with the overall average total income?
-- =====================================================

SELECT
    FilingStatus,
    ROUND(AVG(TotalIncome), 2) AS AverageTotalIncome
FROM TaxReturn
GROUP BY FilingStatus WITH ROLLUP;

-- =====================================================
-- QUERY 10
-- Business Question:
-- How does total income differ by filing status
-- and income type?
-- =====================================================

SELECT
    tr.FilingStatus,
    ir.IncomeType,
    SUM(ir.Amount) AS TotalIncome
FROM TaxReturn tr
JOIN IncomeRecord ir
    ON tr.ReturnID = ir.ReturnID
GROUP BY
    tr.FilingStatus,
    ir.IncomeType;

-- =====================================================
-- QUERY 11
-- Business Question:
-- How does average income differ by tax year,
-- taxpayer state, and income type?
-- =====================================================

-- DESCRIBE Taxpayer;
-- DESCRIBE TaxReturn;
-- DESCRIBE IncomeRecord;
-- DESCRIBE Refund;
-- DESCRIBE BalanceDue;

SELECT
    tr.TaxYear,
    t.State,
    i.IncomeType,
    ROUND(AVG(i.Amount), 2) AS AverageIncome
FROM Taxpayer t
JOIN TaxReturn tr
    ON t.TaxpayerID = tr.TaxpayerID
JOIN IncomeRecord i
    ON tr.ReturnID = i.ReturnID
GROUP BY
    tr.TaxYear,
    t.State,
    i.IncomeType
ORDER BY
    tr.TaxYear,
    t.State,
    i.IncomeType;

-- =====================================================
-- QUERY 12
-- Business Question:
-- How does the average number of income types differ
-- by tax outcome and filing status?
-- =====================================================

SELECT
    tr.FilingStatus,
    CASE
        WHEN r.RefundID IS NOT NULL THEN 'Refund'
        WHEN b.BalanceDueID IS NOT NULL THEN 'Balance Due'
        ELSE 'Neither'
    END AS TaxOutcome,
    ROUND(AVG(inc.NumberOfIncomeTypes), 2) AS AverageIncomeTypes,
    COUNT(tr.ReturnID) AS NumberOfReturns
FROM TaxReturn tr

JOIN (
    SELECT
        ReturnID,
        COUNT(DISTINCT IncomeType) AS NumberOfIncomeTypes
    FROM IncomeRecord
    GROUP BY ReturnID
) inc
    ON tr.ReturnID = inc.ReturnID

LEFT JOIN Refund r
    ON tr.ReturnID = r.ReturnID

LEFT JOIN BalanceDue b
    ON tr.ReturnID = b.ReturnID

GROUP BY
    tr.FilingStatus,
    TaxOutcome

ORDER BY
    tr.FilingStatus,
    TaxOutcome;

-- =====================================================
-- QUERY 13
-- Business Question:
-- How do average income, deductions, and tax credits
-- differ across filing statuses?
-- =====================================================

SELECT
    tr.FilingStatus,
    COUNT(*) AS ReturnCount,
    ROUND(AVG(tr.TotalIncome), 2) AS AverageIncome,
    ROUND(AVG(COALESCE(d.TotalDeduction, 0)), 2) AS AverageDeduction,
    ROUND(AVG(COALESCE(c.TotalCredit, 0)), 2) AS AverageCredit
FROM TaxReturn tr

LEFT JOIN (
    SELECT
        ReturnID,
        SUM(Amount) AS TotalDeduction
    FROM Deduction
    GROUP BY ReturnID
) d
    ON tr.ReturnID = d.ReturnID

LEFT JOIN (
    SELECT
        ReturnID,
        SUM(Amount) AS TotalCredit
    FROM TaxCredit
    GROUP BY ReturnID
) c
    ON tr.ReturnID = c.ReturnID

GROUP BY tr.FilingStatus
ORDER BY AverageIncome DESC;

-- =====================================================
-- QUERY 14
-- Business Question:
-- How do average income, deductions, credits, and
-- refund amounts compare across filing statuses
-- for returns receiving refunds?
-- =====================================================

SELECT
    tr.FilingStatus,
    COUNT(r.ReturnID) AS RefundReturnCount,
    ROUND(AVG(tr.TotalIncome), 2) AS AverageIncome,
    ROUND(AVG(COALESCE(d.TotalDeduction, 0)), 2) AS AverageDeduction,
    ROUND(AVG(COALESCE(c.TotalCredit, 0)), 2) AS AverageCredit,
    ROUND(AVG(r.RefundAmount), 2) AS AverageRefund
FROM TaxReturn tr

JOIN Refund r
    ON tr.ReturnID = r.ReturnID

LEFT JOIN (
    SELECT
        ReturnID,
        SUM(Amount) AS TotalDeduction
    FROM Deduction
    GROUP BY ReturnID
) d
    ON tr.ReturnID = d.ReturnID

LEFT JOIN (
    SELECT
        ReturnID,
        SUM(Amount) AS TotalCredit
    FROM TaxCredit
    GROUP BY ReturnID
) c
    ON tr.ReturnID = c.ReturnID

GROUP BY tr.FilingStatus
ORDER BY AverageRefund DESC;

-- =====================================================
-- QUERY 15
-- Business Question:
-- How do refund amounts compare across deduction
-- levels, and which returns have the largest
-- refunds within each deduction group?
-- =====================================================

WITH RefundData AS (
    SELECT
        tr.ReturnID,
        tr.FilingStatus,
        tr.TotalIncome,
        d.TotalDeduction,
        r.RefundAmount,

        NTILE(4) OVER (
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
    FilingStatus,
    TotalIncome,
    TotalDeduction,
    RefundAmount,
    DeductionQuartile,

    ROUND(
        AVG(RefundAmount) OVER (
            PARTITION BY DeductionQuartile
        ),
        2
    ) AS QuartileAverageRefund,

    RANK() OVER (
        PARTITION BY DeductionQuartile
        ORDER BY RefundAmount DESC
    ) AS RefundRankWithinQuartile

FROM RefundData

ORDER BY
    DeductionQuartile,
    RefundRankWithinQuartile;