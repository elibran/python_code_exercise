from unittest.mock import patch
from banking.loans import process_loan_application

@patch('banking.loans.check_credit_score')
def test_loan_rejected_due_to_low_score(mock_check_score):
    mock_check_score.return_value = 650
    result = process_loan_application("customer-123", 5000)
    assert result == "Rejected"

@patch('banking.loans.check_credit_score')
def test_loan_approved_with_high_score(mock_check_score):
    mock_check_score.return_value = 800
    result = process_loan_application("customer-456", 10000)
    assert result == "Approved"
