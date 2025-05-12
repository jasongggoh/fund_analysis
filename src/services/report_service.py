import pandas as pd

from src.repositories.equity_price_repo import EquityPriceRepo
from src.repositories.external_funds_repo import ExternalFundsRepo
from src.repositories.equity_reference_repo import EquityReferenceRepo


class ReportService:

    def __init__(
            self,
            ex_funds_repo: ExternalFundsRepo,
            eq_ref_repo: EquityReferenceRepo,
            eq_price_repo: EquityPriceRepo
    ):
        self.ex_funds_repo = ex_funds_repo
        self.eq_ref_repo = eq_ref_repo
        self.eq_price_repo = eq_price_repo

    def get_recon_equities_report(self) -> pd.DataFrame:
        fund_df = self.ex_funds_repo.fetch_all_equities_as_df()

        if fund_df.empty:
            raise RuntimeError("Funds data is not available")

        price_df = self.eq_price_repo.fetch_all_as_df()

        if price_df.empty:
            raise RuntimeError("Price data is not available")

        fund_price_df = pd.merge_asof(
            fund_df.sort_values("data_date"),
            price_df.sort_values("reference_date"),
            by="symbol",
            left_on="data_date",
            right_on="reference_date",
            direction="backward"
        )

        fund_price_df = fund_price_df[
            ["fund_name", "symbol", "security_name", "price", "data_date", "reference_date", "reference_price"]
        ]
        fund_price_df["difference_to_ref"] = fund_price_df["price"] - fund_price_df["reference_price"]

        # sort for readability
        fund_price_df.sort_values(["fund_name", "data_date", "symbol"], inplace=True)

        return fund_price_df

    def get_best_performance_by_month_report(self) -> pd.DataFrame:
        fund_df = self.ex_funds_repo.fetch_all_equities_as_df()

        if fund_df.empty:
            raise RuntimeError("Funds data is not available")

        perf_df = fund_df.groupby(["fund_name", "data_date"]).agg({
            "market_value": "sum",
            "realised_pnl": "sum"
        }).reset_index()

        # formula is (Fund_MV_end - Fund_MV_start + Realized P/L) / Fund_MV_start
        # therefore (d(Fund_MV) + realized P/L)/ Fund_MV_start
        perf_df["rate_of_return"] = (
                (perf_df["market_value"].diff() + perf_df["realised_pnl"]) / perf_df["market_value"].shift(1)
        )

        best_perf_fund_by_month = (
            perf_df
            .loc[perf_df.groupby("data_date")["rate_of_return"]
            .idxmax()][["data_date", "fund_name", "rate_of_return"]]
            .reset_index(drop=True)
        )

        #sort for readability
        best_perf_fund_by_month.sort_values(["data_date"])

        return best_perf_fund_by_month

