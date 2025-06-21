import logging
import sqlite3
from typing import Callable


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
