import os
import pandas as pd
import yaml
from pandas.testing import assert_frame_equal
from numpy import nan

from src.utils.common import PROJECT_ROOT
from src.utils.file_handler import FileHandler
from src.models.file_mapping_config import FileMappingConfigs

def test_initialize_file_mapping(mock_file_mappings, tmp_path):
    config = {
        "funds": [mapping.model_dump() for mapping in mock_file_mappings.funds]
    }

    config_file = tmp_path / "config.yaml"
    with open(config_file, "w") as file:
        yaml.dump(config, file, default_flow_style=False)
        file.seek(0)

    result = FileHandler.initialize_file_mapping(str(config_file))

    assert isinstance(result, FileMappingConfigs)
    assert len(result.funds) == 1
    assert result.funds[0].fund_name == "Applebead"

def test_load_files(mock_file_mappings):
    df = FileHandler.load_files(mock_file_mappings, os.path.join(PROJECT_ROOT, "tests/resources"))
    result = df[df["symbol"] == "TJX"]

    expected = pd.DataFrame(
        {
            "financial type": ["Equities"],
            "symbol": ["TJX"],
            "security name": ["TJX Companies"],
            "sedol": [nan],
            "price": [79.11000],
            "quantity": [37548.17313],
            "realised p/l": [12225.84771],
            "market value": [2970435.97613],
            "fund name": ["Applebead"],
            "data date": ["30-11-2022"],
        }
    )
    expected["data date"] = pd.to_datetime(expected["data date"])
    assert_frame_equal(result, expected)
