from unittest.mock import patch

import pytest
from pandas.testing import assert_frame_equal

from src.repositories.external_funds_repo import ExternalFundsRepo

@pytest.mark.parametrize(
    "equities, expected",
    [
        (
            "mock_equities",
            "mock_ex_funds_df"
        ),
        (
            "mock_empty_list",
            "mock_empty_df"
        )
    ]
)
@patch("src.repositories.external_funds_repo.ExternalFundsRepo.fetch_all_equities")
def test_fetch_all_equities_as_df(mock_fetch_all_equities, equities, expected, request):
    mock_equities_df = request.getfixturevalue(equities)
    expected_df = request.getfixturevalue(expected)
    mock_fetch_all_equities.return_value = mock_equities_df

    ex_funds_repo = ExternalFundsRepo()
    results = ex_funds_repo.fetch_all_equities_as_df()

    assert_frame_equal(expected_df, results)
