import logging
import sqlite3
import pandas as pd
from typing import Callable, Optional


def transaction(connection: sqlite3.Connection) -> Callable:
    def decorator(func):
        def wrapper(*args, **kwargs):

            cur = connection.cursor()
            cur.execute("BEGIN TRANSACTION")
            try:
                result = func(*args, cursor=cur, **kwargs)
                connection.commit()
                return result
            except Exception:
                logging.exception("Error occurred in transaction.")
                connection.rollback()
            finally:
                cur.close()

        return wrapper

    return decorator

def validate_schema(df: pd.DataFrame, schema: Optional[dict]) -> pd.DataFrame:
    if not schema:
        # no validation needed
        return df
    for col, att in schema.items():
        type = att.get("type")
        nullable = att.get("nullable")
        if col not in df.columns:
            raise ValueError(f"Missing column '{col}'")

        df[col] = df[col].astype(type)

        if df[col].dtype != type:
            raise ValueError(f"Column {col} has invalid type '{df[col].dtype}', expected '{type}'")
        if not nullable and df[col].isnull().any():
            raise ValueError(f"Column {col} contains null values")
    return df