from typing import List

from pydantic import BaseModel

class FileMapping(BaseModel):
    fund_name: str
    date_regex: str
    date_format: str

class FileMappingConfigs(BaseModel):
    funds: List[FileMapping]