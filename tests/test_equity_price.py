import datetime

import pytest

from src.models.equity_price import EquityPrice

def test_equity_price():
    data = {
        "reference_date": "5/31/2022",
        "symbol": "APL",
        "reference_price": 1.1
    }

    result = EquityPrice(**data)

    assert result.reference_date == datetime.date(2022, 5, 31)

@pytest.mark.parametrize("mock_data", [
    {"reference_date": "5-31-2022", "symbol": "APL", "reference_price": 1.1},
    {"reference_date": "31/5/2022", "symbol": "APL", "reference_price": 1.1}
])
def test_equity_price_wrong_format(mock_data):
    with pytest.raises(ValueError):
        EquityPrice(**mock_data)