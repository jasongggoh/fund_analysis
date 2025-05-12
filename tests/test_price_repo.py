from unittest.mock import patch

import pandas as pd
import pytest
from pandas import Timestamp
from pandas.testing import assert_frame_equal

from src.repositories.price_repo import PriceRepo, transaction


def test_transaction_commit_on_success(mock_connection, mock_cursor):
    mock_connection.cursor.return_value = mock_cursor

    @transaction(mock_connection)
    def dummy_func(cursor=None) -> None:
        cursor.execute("some sql")

    # function call
    dummy_func()

    mock_connection.cursor.assert_called_once()
    mock_cursor.execute.assert_any_call("BEGIN TRANSACTION")
    mock_connection.commit.assert_called_once()
    mock_cursor.close.assert_called_once()

def test_transaction_rollback_on_failure(mock_connection, mock_cursor):
    mock_connection.cursor.return_value = mock_cursor

    @transaction(mock_connection)
    def dummy_func(cursor=None) -> None:
        cursor.execute("some sql")
        raise RuntimeError("Something went wrong")

    dummy_func()

    mock_connection.cursor.assert_called_once()
    mock_connection.commit.assert_not_called()
    mock_connection.rollback.assert_called_once()
    mock_cursor.close.assert_called_once()

@pytest.mark.parametrize("mock_data, mock_description, expected_df", [
    (
        [(1, "APL"), (2, "BTA")],
        [("ID", ), ("SYMBOL", )],
        pd.DataFrame({"id": [1,2],  "symbol": ["APL", "BTA"]}),
    ),
    (
        [],
        [],
        pd.DataFrame()
    )
])
def test_fetch_as_df(mock_data, mock_description, expected_df, mock_connection, mock_cursor):
    mock_data = mock_data
    mock_description = mock_description
    mock_cursor.fetchall.return_value = mock_data
    mock_cursor.description = mock_description

    mock_connection.cursor.return_value = mock_cursor

    price_repo = PriceRepo()
    price_repo.conn = mock_connection
    results = price_repo.fetch_as_df("select * from query")
    assert_frame_equal(expected_df, results)


@pytest.mark.parametrize(
    "mock_df, expected",
    [
        (
            "mock_eq_price_df",
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
                },
            ]
        ),
        (
            "mock_empty_df",
            []
        )

    ]
)
@patch("src.repositories.price_repo.PriceRepo.fetch_as_df")
def test_select_all_data(mock_fetch_as_df, mock_df, expected, request):
    mock_price_df = request.getfixturevalue(mock_df)
    mock_fetch_as_df.return_value = mock_price_df

    price_repo = PriceRepo()
    results = price_repo.select_all_data("equities")

    assert results == expected


