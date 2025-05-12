import pandas as pd

import pytest
from pandas._testing import assert_frame_equal

from src.services.report_service import ReportService

@pytest.fixture
def report_service(mock_ex_funds_repo, mock_eq_ref_repo, mock_eq_price_repo):
    return ReportService(
        ex_funds_repo=mock_ex_funds_repo,
        eq_ref_repo=mock_eq_ref_repo,
        eq_price_repo=mock_eq_price_repo
    )

def test_get_reconcile_equities_report(report_service, mock_ex_funds_repo, mock_eq_price_repo, mock_ex_funds_df, mock_eq_price_df):
    mock_ex_funds_repo.fetch_all_equities_as_df.return_value = mock_ex_funds_df
    mock_eq_price_repo.fetch_all_as_df.return_value = mock_eq_price_df

    result = report_service.get_recon_equities_report()

    # also tests for latest available ref data
    expected = pd.DataFrame(
        {
            "fund_name": ["Applebead", "Beta"],
            "symbol": ["APL", "BTA"],
            "security_name": ["mock Applebead", "mock Beta"],
            "price": [1.1, 2.1],
            "data_date": ["2022-05-31", "2022-05-31"],
            "reference_date": ["2022-05-29", "2022-05-31"],
            "reference_price": [2.1, 3.1],
            "difference_to_ref": [-1.0, -1.0]
        }
    )
    for col in ["reference_date", "data_date"]:
        expected[col] = pd.to_datetime(expected[col])
    assert_frame_equal(result, expected)

def test_get_best_perf_by_month(report_service, mock_ex_funds_repo, mock_ex_funds_df):
    mock_ex_funds_repo.fetch_all_equities_as_df.return_value = mock_ex_funds_df

    result = report_service.get_best_performance_by_month_report()

    expected = pd.DataFrame(
        {
            "data_date": ["2022-05-31"],
            "fund_name": ["Beta"],
            "rate_of_return": [2.981982]
        }
    )
    expected["data_date"] = pd.to_datetime(expected["data_date"])
    assert_frame_equal(result, expected)