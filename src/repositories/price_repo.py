import sqlite3
import pandas as pd
import os
import logging


from src.utils.common import PROJECT_ROOT, parse_date_cols
from src.utils.database_utils import transaction, validate_schema

class PriceRepo:
    def __init__(self):
        self.connection_string = ":memory:"
        self.conn = sqlite3.connect(self.connection_string)
        self.date_cols=[]
        self.schema = None
        self.table_name = None
        self.col_rename_dict = None

        self.initialise_data()

    def initialise_data(self) -> None:
        @transaction(self.conn)
        def ingest_script(cursor: sqlite3.Cursor, sql: str):
            cursor.executescript(sql)

        master_sql_file = os.path.join(PROJECT_ROOT, r"src/resources/master-reference-sql.sql")
        with open(master_sql_file, 'r') as sql_file:
            sql_script = sql_file.read()
            ingest_script(sql=sql_script)

    def fetch(self, query: str) -> pd.DataFrame:
        cur = self.conn.cursor()
        try:
            cur.execute(query)
            results = cur.fetchall()
            columns = [col[0].lower() for col in cur.description]
            df = pd.DataFrame(results, columns=columns)

            if self.col_rename_dict:
                df = df.rename(columns=self.col_rename_dict)
            return df
        except Exception:
            logging.exception("Error occurred when fetching data")
            raise
        finally:
            cur.close()

    def fetch_all(self) -> pd.DataFrame:
        query = f"SELECT * FROM '{self.table_name}'"
        df = self.fetch(query)

        if df.empty:
            raise RuntimeError("No data fetched from DB with table '{table_name}'.")

        df = validate_schema(df, schema=self.schema)
        df = parse_date_cols(df, self.date_cols)

        return df