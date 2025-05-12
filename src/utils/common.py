from typing import List
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def parse_date_cols(df: pd.DataFrame, date_cols: List[str]) -> pd.DataFrame:

    df = df.copy()

    if not df.empty:
        for col in date_cols:
            df[col] = pd.to_datetime(df[col])

    return df