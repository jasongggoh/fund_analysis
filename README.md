# Fund Analysis

## Description

This application generates 2 kinds of reports through the `ReportService`
- Price reconciliation report
  - Reconciliation = `price_by_fund` - `reference price`
- Best fund by month report
  - Rate of return = (`Fund_MV_end` - `Fund_MV_start` + `Realized P/L`) / `Fund_MV_start`
  - which is also = (diff(`Fund_MV`) + `Realized P/L`) / `Fund_MV_start`

## Setting up

To set up your environment, make sure you have `poetry` installed by running `pip install poetry`. Then run `poetry install` to set up your dependencies.

## Developers notes

### Overview
Columns in the data sources might not conform to snake_case convention. Therefore, the repositories serve as interfaces to handle these discrepancies and convert them to snake_case.
This takes place upon converting the data extracted to Pydantic modelling for validation.

Data repositories fetch the data from their sources and return them in the type as annotated. Services string these data repositories operations together and generate the reports.

The main code that executes the application is in `main.py`.

### Modelling
- External fund data are provided through `.csv` files and are stored within `external-funds` folder.
- Pydantic modelling of the data can be found in `src\models`
  - These serve as schema validation for the dataset
- Data repositories can be found in `src\repositories`
  - These serve as an interface between Python and the 2 data sources/
- Report services can be found in `src\services`.
  - These services generate the respective reports
- Common functions are in `src\utils` and additional resources in `src\resources`

### Onboarding New Funds
A yaml file with configuration for all the funds extracted can be found in `src\repositories\file_mapping\file_mapping_config.yml`
It contains 3 fields:
- `fund_name`: The name of the fund
- `date_regex`: Regex to extract the dates
- `date_format`: Format of the extracted dates

To onboard new funds, simply add in an additional config for it and ensure the data is coming in with the expected schema.

### linting
Run `poetry run ruff check --fix` to fix all linting issues as configured within `ruff`

### Tests
Run `poetry run pytest` to execute all tests.