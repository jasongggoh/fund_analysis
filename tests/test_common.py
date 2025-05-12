import copy

import pandas as pd
from pandas._testing import assert_frame_equal

from src.utils.common import parse_date_cols

def test_parse_date_cols():
    df = pd.DataFrame(
        {
            "id": [1,2],
            "data_date": ["1-Jan-2025", "3-Mar-2025"],
            "reference_date": ["31-Dec-2025", "31-Dec-2025"]
        }
    )

    expected = copy.deepcopy(df)
    expected["data_date"] = pd.to_datetime(expected["data_date"])
    expected["reference_date"] = pd.to_datetime(expected["reference_date"])

    results = parse_date_cols(df=df, date_cols=["data_date", "reference_date"])

    assert_frame_equal(expected, results)