from unittest.mock import patch
from banking.transfers import international_transfer

@patch('banking.transfers.get_exchange_rate')
def test_international_transfer(mock_get_rate):
    mock_get_rate.return_value = 1.25
    converted = international_transfer(None, None, 100, 'EUR')
    assert converted == 125.0
