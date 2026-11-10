# API-to-MySQL Data Pipeline

A Python-based batch ETL pipeline that extracts e-commerce data from a REST API, transforms nested JSON records, validates data quality, quarantines rejected records and loads valid data into MySQL using UPSERT operations.

## Project Overview

This project demonstrates an end-to-end data pipeline covering API ingestion, data transformation, validation, relational database loading and automated testing.

**Data source:** [DummyJSON Carts API](https://dummyjson.com/carts)

### Key Features

- REST API ingestion with pagination and retry handling.
- Raw JSON data preservation.
- Nested JSON transformation using Pandas.
- Record-level data validation and duplicate detection.
- Rejected-record quarantine.
- Automated data quality reporting.
- Incremental database loading using MySQL UPSERT.
- Transaction management and rollback.
- Pipeline logging and execution metadata.
- Unit and database integration testing.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Pipeline development and orchestration |
| Requests | API communication |
| Pandas | Data transformation and validation |
| MySQL | Relational data storage |
| mysql-connector-python | Database connectivity |
| pytest | Automated testing |
| Git | Version control |

## Pipeline Workflow

The pipeline processes data through the following stages:

1. **Ingestion:** Retrieve paginated data from the REST API.
2. **Transformation:** Flatten nested JSON into relational DataFrames.
3. **Validation:** Identify valid and rejected product records.
4. **Quarantine:** Store rejected records separately.
5. **Quality Reporting:** Generate data quality metrics.
6. **Database Loading:** Insert or update records in MySQL.
7. **Monitoring:** Record execution logs and run metadata.

For detailed architecture, data flow and processing rules, refer to the documentation in the `docs/` directory.

## Project Structure

```text
api-to-sql-pipeline/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── rejected/
│   └── reports/
│
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   └── business_rules.md
│
├── logs/
│
├── src/
│   ├── ingestion.py
│   ├── transform.py
│   ├── validate.py
│   ├── database.py
│   ├── load_data.py
│   ├── data_quality_report.py
│   ├── pipeline_metadata.py
│   ├── pipeline_logger.py
│   └── main.py
│
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
│
├── tests/
│   ├── conftest.py
│   ├── test_transform.py
│   ├── test_validation.py
│   └── test_database_integration.py
│
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Setup and Installation

### Prerequisites

- Python 3.10 or later
- MySQL Server
- Git

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd api-to-sql-pipeline
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Execute the SQL statements in `sql/schema.sql` using MySQL Workbench to create the database and tables.

Configure the connection using environment variables:

```powershell
$env:MYSQL_HOST = "localhost"
$env:MYSQL_USER = "root"
$env:MYSQL_DATABASE = "ecommerce_pipeline"
```

If `MYSQL_PASSWORD` is not configured, the application securely prompts for the password.

Never commit database credentials to Git.

## Running the Pipeline

From the project root:

```bash
python src/main.py
```

The pipeline retrieves API data, processes and validates records, generates quality reports, quarantines rejected records and loads valid records into MySQL.

## Testing

The project includes unit tests and opt-in MySQL integration tests.

### Run unit tests

```bash
python -m pytest -v
```

### Run database integration tests

Create a separate MySQL database named `ecommerce_pipeline_test` using the project schema.

Configure the test environment in PowerShell:

```powershell
$env:MYSQL_HOST = "localhost"
$env:MYSQL_USER = "root"
$env:MYSQL_DATABASE = "ecommerce_pipeline_test"
$env:RUN_DB_INTEGRATION = "1"

$securePassword = Read-Host "Enter MySQL password" -AsSecureString
$env:MYSQL_PASSWORD = [System.Net.NetworkCredential]::new("", $securePassword).Password
```

Execute:

```bash
python -m pytest tests/test_database_integration.py -v
```

Integration tests verify:

- Initial record insertion.
- Idempotent loading.
- UPSERT update behaviour.
- Transaction rollback.

Integration tests are skipped during ordinary test execution unless explicitly enabled.

## Current Results

One successful sample execution produced:

| Metric | Records |
|---|---:|
| Carts ingested | 208 |
| Products transformed | 800 |
| Valid products | 788 |
| Rejected products | 12 |
| Data quality rate | 98.50% |

Results may vary depending on the source API response.

## Current Limitations

- Uses sample API data rather than a production data source.
- Raw data, quarantine files and reports are overwritten on subsequent runs.
- Transformation assumes expected source fields are present.
- Uses offset-based pagination.
- Does not reconcile records deleted from the source.
- UPSERT operations process the submitted dataset rather than only changed records.

## Future Improvements

- Source schema validation.
- Historical data and report retention.
- Improved incremental extraction.
- Enhanced monitoring and alerting.
- Docker-based deployment.
- Cloud deployment and scheduled execution.

---

**Project Category:** Data Engineering | ETL | Database Integration  
**Language:** Python  
**Database:** MySQL