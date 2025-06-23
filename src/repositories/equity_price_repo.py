from src.repositories.price_repo import PriceRepo
from src.models.equity_price import equity_price_schema, col_rename_dict


class EquityPriceRepo(PriceRepo):
    def __init__(self):
        super().__init__()
        self.table_name = "equity_prices"
        self.date_cols = ["reference_date"]
        self.schema = equity_price_schema
        self.col_rename_dict = col_rename_dict