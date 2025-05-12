from unittest.mock import patch

import pytest
from pandas.testing import assert_frame_equal

from src.repositories.equity_price_repo import EquityPriceRepo

@pytest.mark.parametrize(
    "eq_price, expected",
    [
        (
            "mock_eq_price",
            "mock_eq_price_df"
        ),
        (
            "mock_empty_list",
            "mock_empty_df"
        )
    ]
)
@patch("src.repositories.equity_price_repo.EquityPriceRepo.fetch_all")
def test_fetch_all_equities_as_df(mock_fetch_all, eq_price, expected, request):
    mock_df = request.getfixturevalue(eq_price)
    expected_df = request.getfixturevalue(expected)
    mock_fetch_all.return_value = mock_df

    ex_funds_repo = EquityPriceRepo()
    results = ex_funds_repo.fetch_all_as_df()

    assert_frame_equal(expected_df, results)
