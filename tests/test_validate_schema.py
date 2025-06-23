import pandas as pd
import pytest

from src.utils.database_utils import validate_schema

@pytest.fixture
def mock_schema():
    return {
        "name": {"type": pd.StringDtype(), "nullable": False},
        "age": {"type": pd.Int64Dtype(), "nullable": False},
    }

def test_validate_schema_none():
    df = pd.DataFrame({"a": [1, 2]})
    result = validate_schema(df, None)
    pd.testing.assert_frame_equal(result, df)

def test_validate_schema_valid(mock_schema):
    df = pd.DataFrame({
        "name": ["Alice", "Bob"],
        "age": [25, 30]
    })
    result = validate_schema(df, mock_schema)
    assert result["name"].dtype.name == "string"
    assert result["age"].dtype == "Int64"


def test_validate_schema_missing_column(mock_schema):
    df = pd.DataFrame({"name": ["Alice", "Bob"]})
    with pytest.raises(ValueError, match="Missing column 'age'"):
        validate_schema(df, mock_schema)

def test_validate_schema_type_mismatch():
    df = pd.DataFrame({
        "age": ["twenty", "thirty"]
    })
    schema = {
        "age": {"type": pd.Int64Dtype(), "nullable": False},
    }
    with pytest.raises(Exception):  # ValueError or TypeError may occur on cast
        validate_schema(df, schema)

def test_validate_schema_null_not_allowed():
    df = pd.DataFrame({
        "name": ["Alice", None]
    })
    schema = {
        "name": {"type": pd.StringDtype(), "nullable": False},
    }
    with pytest.raises(ValueError, match="Column name contains null values"):
        validate_schema(df, schema)