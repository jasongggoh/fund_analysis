from unittest.mock import patch

import pandas as pd
import pytest
from pandas import Timestamp
from pandas.testing import assert_frame_equal

from src.repositories.price_repo import PriceRepo


@pytest.mark.parametrize("mock_data, mock_description, expected_df", [
    (
        [(1, "APL"), (2, "BTA")],
        [("ID", ), ("SYMBOL", )],
        pd.DataFrame({"id": [1,2],  "symbol": ["APL", "BTA"]}),
    ),
    (
        [],
        [],
        pd.DataFrame(columns=[]), # pandas special handling where there are no data and no columns
    )
])
def test_fetch(mock_data, mock_description, expected_df, mock_connection, mock_cursor):
    mock_data = mock_data
    mock_description = mock_description
    mock_cursor.fetchall.return_value = mock_data
    mock_cursor.description = mock_description

    mock_connection.cursor.return_value = mock_cursor

    price_repo = PriceRepo()
    price_repo.conn = mock_connection
    results = price_repo.fetch("select * from query")
    assert_frame_equal(expected_df, results)

@pytest.fixture
def expected_df():
    return pd.DataFrame(
        [
            {
                "reference_date": Timestamp('2022-05-29 00:00:00'),
                "symbol": "APL",
                "reference_price": 2.1
            },
            {
                "reference_date": Timestamp('2022-05-31 00:00:00'),
                "symbol": "BTA",
                "reference_price": 3.1
            }
        ]
    )


@patch("src.repositories.price_repo.PriceRepo.fetch")
def test_select_all_data(mock_fetch, mock_eq_price_df, expected_df):
    mock_fetch.return_value = mock_eq_price_df

    price_repo = PriceRepo()
    results = price_repo.fetch_all()

    assert_frame_equal(expected_df, results)


@patch("src.repositories.price_repo.PriceRepo.fetch")
def test_fetch_all_no_data(mock_fetch, mock_empty_df):
    mock_fetch.return_value = mock_empty_df

    price_repo = PriceRepo()
    with pytest.raises(RuntimeError):
        price_repo.fetch_all()