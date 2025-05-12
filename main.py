import logging
import os

from src.repositories.equity_price_repo import EquityPriceRepo
from src.repositories.equity_reference_repo import EquityReferenceRepo
from src.repositories.external_funds_repo import ExternalFundsRepo
from src.services.report_service import ReportService
from src.utils.common import PROJECT_ROOT
from src.utils.file_handler import FileHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

if __name__ == "__main__":
    eq_repo = EquityReferenceRepo()
    ex_repo = ExternalFundsRepo()
    eq_price_repo = EquityPriceRepo()

    output_dir = os.path.join(PROJECT_ROOT, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    recon_file_name = "price_recon.xlsx"
    perf_file_name = "best_fund_by_month.xlsx"

    report_service = ReportService(ex_funds_repo=ex_repo, eq_ref_repo=eq_repo, eq_price_repo=eq_price_repo)
    try:
        recon_data = report_service.get_recon_equities_report()
        FileHandler.export_report_as_excel(output_dir, recon_file_name, recon_data)
        logging.info("Generated recon report")
    except Exception as e:
        logging.exception("Failed to generate recon report")
        raise e

    try:
        best_perf_fund_by_month = report_service.get_best_performance_by_month_report()
        FileHandler.export_report_as_excel(output_dir, perf_file_name, best_perf_fund_by_month)
        logging.info("Generated performance report")
    except Exception as e:
        logging.exception("Failed to generate performance report")
        raise e