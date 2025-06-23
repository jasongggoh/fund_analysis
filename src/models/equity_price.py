import pandas as pd

equity_price_schema = {
    "reference_date": {"type": "datetime64[ns]", "nullable": False},
    "symbol": {"type": pd.StringDtype(), "nullable": False},
    "reference_price": {"type": pd.Float64Dtype(), "nullable": False},
}

col_rename_dict = {
    "datetime": "reference_date",
    "price": "reference_price"
}