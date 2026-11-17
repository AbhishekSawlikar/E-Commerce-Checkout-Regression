# E-Commerce Checkout Regression

A small Playwright + Python/pytest framework for checking the SauceDemo shopping
journey. The suite uses one Chromium browser and the demo site's fictional
checkout; it does not make real payments.

## Requirements

- Python 3.10+
- Dependencies in `requirements.txt`
- Playwright Chromium browser
- Allure Commandline and Java (to view or generate the Allure report)

## Setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Install Allure Commandline using your preferred Windows package manager, for
example:

```powershell
scoop install allure
```

Ensure `allure --version` works in your terminal before generating a report.

## Run

```powershell
pytest
```

Each test run creates the existing self-contained HTML report at
`reports/report.html` and fresh Allure result files in `allure-results/`.
To open an interactive Allure report:

```powershell
allure serve allure-results
```

Or generate a report into `allure-report/` for later viewing:

```powershell
allure generate allure-results -o allure-report --clean
```

Open `allure-report/index.html` in a browser to view the generated report.

The eight tests independently cover valid and locked-out login, required
username validation, adding/removing a cart item, ascending price sorting,
checkout validation, and successful checkout. Pytest writes a self-contained
HTML report to `reports/report.html` and Allure results for the same test run.

The tests use SauceDemo's `standard_user` and `locked_out_user` accounts with
the demo password `secret_sauce`. Prices are read from the application at
runtime; the subtotal check compares the checkout review against its displayed
items and does not assume a tax rate.
