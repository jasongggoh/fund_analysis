from src.repositories.price_repo import PriceRepo
from src.models.equity_reference import equity_reference_schema, col_rename_dict

class EquityReferenceRepo(PriceRepo):

    def __init__(self):
        super().__init__()
        self.table_name = "equity_reference"
        self.schema = equity_reference_schema
        self.col_rename_dict = col_rename_dict