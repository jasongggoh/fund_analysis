from enum import Enum
from pathlib import Path
from pydantic import BaseModel

class ReportType(Enum):
    price_recon = "price_recon"
    best_perf_by_month = "best_perf_by_month"

class ReportInput(BaseModel):
    report_type: ReportType
    output_file_path: Path