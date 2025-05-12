import os

import yaml
import re
import pandas as pd
import logging

from pathlib import Path
from src.models.file_mapping_config import FileMappingConfigs, FileMapping

class FileHandler:

    @staticmethod
    def initialize_file_mapping(config_file: str) -> FileMappingConfigs:
        with open(config_file) as yaml_file:
            data = yaml.safe_load(yaml_file)

            return FileMappingConfigs(
                funds=[
                    FileMapping(**mapping) for mapping in data.get("funds") or {}
                ]
            )

    @staticmethod
    def load_files(file_mappings: FileMappingConfigs, config_dir: str) -> pd.DataFrame:
        files = [f for f in Path(config_dir).glob("*.csv")]

        dfs = []
        for config in file_mappings.funds:
            for file in files:
                if config.fund_name.lower() in file.name.lower():
                    df = pd.read_csv(str(file))
                    df["FUND NAME"] = config.fund_name
                    data_date = re.search(config.date_regex, file.name)
                    if data_date:
                        df["DATA DATE"] = data_date.group(0)
                        df["DATA DATE"] = pd.to_datetime(df["DATA DATE"], format=config.date_format)
                    else:
                        logging.warning("no date found")
                    dfs.append(df)

        return pd.concat(dfs).rename(columns=lambda x: x.lower()) if len(dfs) != 0 else pd.DataFrame()

    @staticmethod
    def export_report_as_excel(directory: os.path, file_name: str, df: pd.DataFrame) -> None:
        df.to_excel(os.path.join(directory, file_name), index=False)