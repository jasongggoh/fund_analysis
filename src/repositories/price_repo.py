import sqlite3
import pandas as pd
import os
import logging

from typing import List

from src.utils.common import PROJECT_ROOT
from src.utils.database_utils import transaction


class PriceRepo:
    def __init__(self):
        self.connection_string = ":memory:"
        self.conn = sqlite3.connect(self.connection_string)
        self.date_cols=[]

        self.initialise_data()

    def initialise_data(self) -> None:
        @transaction(self.conn)
        def ingest_script(cursor: sqlite3.Cursor, sql: str):
            cursor.executescript(sql)

        master_sql_file = os.path.join(PROJECT_ROOT, r"src/resources/master-reference-sql.sql")
        with open(master_sql_file, 'r') as sql_file:
            sql_script = sql_file.read()
            ingest_script(sql=sql_script)

    def fetch_as_df(self, query) -> pd.DataFrame:
        cur = self.conn.cursor()
        results = None
        columns = []
        try:
            cur.execute(query)
            results = cur.fetchall()
            columns = [col[0].lower() for col in cur.description]
        except Exception:
            logging.exception("Error occurred when fetching data")
            raise
        finally:
            cur.close()

            if results:
                return pd.DataFrame(
                    results,
                    columns=columns
                )

            return pd.DataFrame()

    def fetch_all(self):
        raise NotImplementedError("Not implemented yet")

    def fetch_all_as_df(self):
        raise NotImplementedError("Not implemented yet")

    def select_all_data(self, table_name: str) -> List[dict]:
        query = f"select * from '{table_name}'"
        df = self.fetch_as_df(query)

        if df.empty:
            return []

        # convert pd.NaN to None first before parsing
        df = df.where(pd.notnull(df), None)

        return df.to_dict("records")