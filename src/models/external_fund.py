import pandas as pd

external_fund_schema = {
    "financial_type": {"type": pd.StringDtype(), "nullable": True},
    "symbol": {"type": pd.StringDtype(), "nullable": True},
    "security_name": {"type": pd.StringDtype(), "nullable": True},
    "sedol": {"type": pd.StringDtype(), "nullable": True},
    "price": {"type": pd.Float64Dtype(), "nullable": True},
    "quantity": {"type": pd.Float64Dtype(), "nullable": True},
    "realised_pnl": {"type": pd.Float64Dtype(), "nullable": True},
    "market_value": {"type": pd.Float64Dtype(), "nullable": True},
    "fund_name": {"type": pd.StringDtype(), "nullable": False},
    "data_date": {"type": "datetime64[ns]", "nullable": False},
}

col_rename_dict = {
    "financial type": "financial_type",
    "security name": "security_name",
    "realised p/l": "realised_pnl",
    "market value": "market_value",
    "fund name": "fund_name",
    "data date": "data_date",
}