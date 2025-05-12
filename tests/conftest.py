from datetime import datetime
from unittest.mock import MagicMock

import pandas as pd
import pytest
import sqlite3

from src.models.equity_price import EquityPrice
from src.models.external_fund import ExternalFund
from src.utils.file_handler import FileHandler
from src.models.file_mapping_config import FileMappingConfigs, FileMapping
from src.services.report_service import ReportService
from src.repositories.external_funds_repo import ExternalFundsRepo
from src.repositories.equity_price_repo import EquityPriceRepo
from src.repositories.equity_reference_repo import EquityReferenceRepo
from src.repositories.price_repo import PriceRepo

@pytest.fixture
def mock_file_handler():
    return MagicMock(spec=FileHandler)

@pytest.fixture
def mock_ex_funds_repo():
    return MagicMock(spec=ExternalFundsRepo)

@pytest.fixture
def mock_eq_price_repo():
    return MagicMock(spec=EquityPriceRepo)

@pytest.fixture
def mock_eq_ref_repo():
    return MagicMock(spec=EquityReferenceRepo)

@pytest.fixture
def mock_price_repo():
    return MagicMock(spec=PriceRepo)

@pytest.fixture
def mock_file_service(mock_ex_funds_repo, mock_eq_price_repo, mock_eq_ref_repo):
    return ReportService(
        ex_funds_repo=mock_ex_funds_repo,
        eq_ref_repo=mock_eq_ref_repo,
        eq_price_repo=mock_eq_price_repo
    )

@pytest.fixture
def mock_eq_price_df():
    df = pd.DataFrame(
        {
            "reference_date": [datetime(2022, 5, 29).date(), datetime(2022, 5, 31).date()],
            "symbol": ["APL", "BTA"],
            "reference_price": [2.1, 3.1]
        }
    )

    df["reference_date"] = pd.to_datetime(df["reference_date"])
    return df

@pytest.fixture
def mock_empty_df():
    return pd.DataFrame()

@pytest.fixture
def mock_ex_funds_df():
    df = pd.DataFrame(
        {
            "financial_type": ["Equities", "Equities"],
            "symbol": ["APL", "BTA"],
            "security_name": ["mock Applebead", "mock Beta"],
            "sedol": ["sedol1", "sedol2"],
            "price": [1.1, 2.1],
            "quantity": [1.1, 2.2],
            "realised_pnl": [2.1, 2.2],
            "market_value": [1.11, 2.22],
            "fund_name": ["Applebead", "Beta"],
            "data_date": [datetime(2022, 5, 31).date(), datetime(2022, 5, 31).date()]
        }
    )
    df["data_date"] = pd.to_datetime(df["data_date"])
    return df

@pytest.fixture
def mock_file_mappings():
    config = {
        "fund_name": "Applebead",
        "date_regex": "\\d{2}-\\d{2}-\\d{4}",
        "date_format": "%d-%m-%Y"
    }

    return FileMappingConfigs(
        funds=[FileMapping(**config)]
    )

@pytest.fixture
def mock_connection():
    return MagicMock(spec=sqlite3.Connection)

@pytest.fixture
def mock_cursor():
    return MagicMock(spec=sqlite3.Cursor)

@pytest.fixture
def mock_equities():
    return [
        ExternalFund(
            financial_type="Equities",
            symbol="APL",
            security_name="mock Applebead",
            sedol="sedol1",
            price=1.1,
            quantity=1.1,
            realised_pnl=2.1,
            market_value=1.11,
            fund_name="Applebead",
            data_date=datetime(2022, 5, 31).date()
            ),
        ExternalFund(
            financial_type="Equities",
            symbol="BTA",
            security_name="mock Beta",
            sedol="sedol2",
            price=2.1,
            quantity=2.2,
            realised_pnl=2.2,
            market_value=2.22,
            fund_name="Beta",
            data_date=datetime(2022, 5, 31).date()
        ),
    ]

@pytest.fixture
def mock_empty_list():
    return []

@pytest.fixture
def mock_eq_price():
    data = [
        {
            "reference_date": "5/29/2022",
            "symbol": "APL",
            "reference_price" : 2.1
        },
        {
            "reference_date": "5/31/2022",
            "symbol": "BTA",
            "reference_price": 3.1
        }
    ]
    return [EquityPrice(**item) for item in data]