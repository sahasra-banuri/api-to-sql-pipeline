# Pipeline Architecture

## 1. Overview

The API-to-MySQL Data Pipeline is a Python-based batch ETL application that extracts e-commerce data from a REST API, transforms nested JSON records, validates product data and loads valid records into MySQL.

It also maintains data quality reports, execution metadata and operational logs.

flowchart TD
    A[DummyJSON Carts API] --> B[Ingestion]
    B --> C[Raw JSON Storage]
    C --> D[Transformation]
    D --> E[Cart DataFrame]
    D --> F[Product DataFrame]
    F --> G[Validation]
    G --> H[Valid Products]
    G --> I[Rejected Products]
    E --> J[MySQL Loading]
    H --> J
    I --> K[Rejected CSV]
    G --> L[Data Quality Report]
    J --> M[(MySQL Database)]

    N[Logging and Execution Metadata] -.-> B
    N -.-> D
    N -.-> G
    N -.-> J

## 3. Component Responsibilities

| Component | Responsibility |
|---|---|
| `ingestion.py` | Retrieves paginated API data with retry handling and saves raw JSON |
| `transform.py` | Converts nested JSON into cart and product DataFrames |
| `validate.py` | Applies product-level validation and identifies rejected records |
| `data_quality_report.py` | Generates data quality metrics and rejection summaries |
| `load_data.py` | Loads cart and valid product records into MySQL using UPSERT |
| `database.py` | Manages MySQL connectivity |
| `main.py` | Orchestrates the complete pipeline |
| `pipeline_logger.py` | Records execution events and errors |
| `pipeline_metadata.py` | Tracks run IDs, durations, statuses and record counts |

## 4. End-to-End Data Flow

1. **Extract:** Retrieve all available cart records from the DummyJSON API using pagination.
2. **Preserve:** Save the original response in `data/raw/carts.json`.
3. **Transform:** Flatten nested JSON into cart-level and product-level DataFrames.
4. **Validate:** Separate valid product records from rejected records.
5. **Report:** Generate data quality metrics in `data/reports/data_quality_report.json`.
6. **Quarantine:** Save rejected product records in `data/rejected/rejected_products.csv`.
7. **Load:** Insert or update cart and valid product records in MySQL.
8. **Monitor:** Record logs and execution metadata throughout the pipeline.

## 5. Database Design

The pipeline uses two relational tables:

- `carts`: Stores one record per cart.
- `cart_products`: Stores individual product lines associated with carts.

The relationship is one-to-many, enforced through a foreign key from `cart_products.cart_id` to `carts.cart_id`.

Cart records are loaded before product records. Both loading operations run within a single transaction, with rollback on failure.

## 6. Design Considerations

| Design Decision | Purpose |
|---|---|
| API pagination | Retrieve the complete dataset |
| Retry handling | Handle temporary API failures |
| Raw JSON preservation | Support debugging and reprocessing |
| Relational transformation | Represent nested data in structured tables |
| Record validation | Prevent invalid product records from being loaded |
| Rejected-record quarantine | Preserve records requiring investigation |
| UPSERT operations | Support repeated loads and updates |
| Transaction management | Prevent partial database loads |
| Execution metadata and logging | Support monitoring and troubleshooting |

## 7. Current Limitations

- Batch processing with offset-based pagination.
- Transformation assumes expected source fields are present.
- Cart records are not independently validated.
- Historical source deletions are not reconciled.
- Rejected records and quality reports are overwritten on subsequent runs.
- No scheduling, automated alerting or streaming support.

## 8. Related Documentation

- [Data Dictionary](data_dictionary.md)
- [Business Rules](business_rules.md)