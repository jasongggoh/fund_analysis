import argparse
import logging
import os

from src.models.report_input import ReportInput, ReportType
from src.repositories.equity_price_repo import EquityPriceRepo
from src.repositories.equity_reference_repo import EquityReferenceRepo
from src.repositories.external_funds_repo import ExternalFundsRepo
from src.services.report_service import ReportGenerator
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

    parser = argparse.ArgumentParser()
    parser.add_argument("report", help="Report to generate")
    parser.add_argument("output_path", help="Path to output file")
    args = parser.parse_args()
    input_args = ReportInput(report_type=args.report, output_file_path=args.output_path)

    output_dir = os.path.join(PROJECT_ROOT, os.path.dirname(input_args.output_file_path))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file_name = os.path.basename(input_args.output_file_path)
    logging.info(f"Generating report {output_file_name}")

    report_service = ReportGenerator(ex_funds_repo=ex_repo, eq_ref_repo=eq_repo, eq_price_repo=eq_price_repo)

    if input_args.report_type == ReportType.price_recon:
        try:
            recon_data = report_service.get_recon_equities_report()
            FileHandler.export_report_as_excel(output_dir, output_file_name, recon_data)
            logging.info("Generated recon report")
        except Exception as e:
            logging.exception("Failed to generate recon report")
            raise e
    elif input_args.report_type == ReportType.best_perf_by_month:
        try:
            best_perf_fund_by_month = report_service.get_best_performance_by_month_report()
            FileHandler.export_report_as_excel(output_dir, output_file_name, best_perf_fund_by_month)
            logging.info("Generated performance report")
        except Exception as e:
            logging.exception("Failed to generate performance report")
            raise e
    else :
        raise RuntimeError("Invalid report type")