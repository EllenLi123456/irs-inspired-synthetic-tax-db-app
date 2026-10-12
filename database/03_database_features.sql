USE irs_project_db;

DROP VIEW IF EXISTS TaxReturnRelationshipSummary;
CREATE VIEW TaxReturnRelationshipSummary AS
SELECT
    tr.ReturnID,
    tr.TaxpayerID,
    CONCAT(tp.FirstName, ' ', tp.LastName) AS TaxpayerName,
    tr.TaxYear,
    tr.FilingStatus,
    COUNT(DISTINCT ir.IncomeID) AS IncomeRecordCount,
    COUNT(DISTINCT d.DeductionID) AS DeductionCount,
    COUNT(DISTINCT tc.CreditID) AS TaxCreditCount,
    COUNT(DISTINCT tf.TaxFormID) AS TaxFormCount,
    CASE WHEN r.RefundID IS NOT NULL THEN 'Yes' ELSE 'No' END AS HasRefund,
    CASE WHEN b.BalanceDueID IS NOT NULL THEN 'Yes' ELSE 'No' END AS HasBalanceDue
FROM TaxReturn tr
JOIN Taxpayer tp ON tr.TaxpayerID = tp.TaxpayerID
LEFT JOIN IncomeRecord ir ON tr.ReturnID = ir.ReturnID
LEFT JOIN Deduction d ON tr.ReturnID = d.ReturnID
LEFT JOIN TaxCredit tc ON tr.ReturnID = tc.ReturnID
LEFT JOIN TaxForm tf ON tr.ReturnID = tf.ReturnID
LEFT JOIN Refund r ON tr.ReturnID = r.ReturnID
LEFT JOIN BalanceDue b ON tr.ReturnID = b.ReturnID
GROUP BY
    tr.ReturnID, tr.TaxpayerID, tp.FirstName, tp.LastName,
    tr.TaxYear, tr.FilingStatus, r.RefundID, b.BalanceDueID;

DROP PROCEDURE IF EXISTS add_balance_due;
DELIMITER //
CREATE PROCEDURE add_balance_due(
    IN p_BalanceDueID INT,
    IN p_ReturnID INT,
    IN p_AmountDue DECIMAL(10,2),
    IN p_DueDate DATE,
    IN p_BalanceStatus VARCHAR(30)
)
BEGIN
    DECLARE refund_count INT;
    SELECT COUNT(*) INTO refund_count
    FROM Refund WHERE ReturnID = p_ReturnID;
    IF refund_count = 0 THEN
        INSERT INTO BalanceDue
            (BalanceDueID, ReturnID, AmountDue, DueDate, BalanceStatus)
        VALUES
            (p_BalanceDueID, p_ReturnID, p_AmountDue, p_DueDate, p_BalanceStatus);
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot add BalanceDue: TaxReturn already has a Refund';
    END IF;
END //
DELIMITER ;

DROP FUNCTION IF EXISTS income_level;
DELIMITER //
CREATE FUNCTION income_level(p_ReturnID INT)
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE return_income DECIMAL(12,2);
    DECLARE average_income DECIMAL(12,2);
    SELECT TotalIncome INTO return_income
    FROM TaxReturn WHERE ReturnID = p_ReturnID;
    SELECT AVG(TotalIncome) INTO average_income FROM TaxReturn;
    IF return_income > average_income THEN
        RETURN 'High Income';
    ELSE
        RETURN 'Standard Income';
    END IF;
END //
DELIMITER ;

-- This trigger protects BalanceDue inserts. The reciprocal Refund insert rule
-- remains an implementation limitation documented in the project review.
DROP TRIGGER IF EXISTS prevent_refund_balance_due;
DELIMITER //
CREATE TRIGGER prevent_refund_balance_due
BEFORE INSERT ON BalanceDue
FOR EACH ROW
BEGIN
    DECLARE refund_count INT;
    SELECT COUNT(*) INTO refund_count
    FROM Refund WHERE ReturnID = NEW.ReturnID;
    IF refund_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot add BalanceDue: TaxReturn already has a Refund';
    END IF;
END //
DELIMITER ;
