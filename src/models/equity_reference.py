import pandas as pd

equity_reference_schema = {
    "symbol": {"type": pd.StringDtype(), "nullable": True},
    "country": {"type": pd.StringDtype(), "nullable": True},
    "security_name": {"type": pd.StringDtype(), "nullable": True},
    "sector": {"type": pd.StringDtype(), "nullable": True},
    "industry": {"type": pd.StringDtype(), "nullable": True},
    "currency": {"type": pd.StringDtype(), "nullable": True},
}

col_rename_dict = {
    "security name": "security_name",
}