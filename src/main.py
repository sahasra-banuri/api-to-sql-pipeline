from pathlib import Path

from ingestion import ingest_data
from transform import transform_cart_data
from validate import validate_products
from load_data import load_data
from pipeline_logger import setup_logger
from data_quality_report import generate_data_quality_report
from pipeline_metadata import (
    start_pipeline_run,
    finalize_pipeline_run
)


logger = setup_logger()


def run_pipeline():

    # Start pipeline execution tracking
    run_metadata, start_time = start_pipeline_run()

    logger.info("========== PIPELINE STARTED ==========")

    try:

        # STEP 1: INGESTION
        logger.info("STEP 1: INGESTION")

        raw_data = ingest_data()

        run_metadata["records"]["carts_ingested"] = len(
            raw_data["carts"]
        )

        # STEP 2: TRANSFORMATION
        logger.info("STEP 2: TRANSFORMATION")

        carts_df, products_df = transform_cart_data()

        run_metadata["records"]["carts_transformed"] = len(carts_df)

        run_metadata["records"]["products_transformed"] = len(
            products_df
        )

        logger.info("Cart records: %d", len(carts_df))
        logger.info("Product records: %d", len(products_df))

        # STEP 3: VALIDATION
        logger.info("STEP 3: VALIDATION")

        valid_products, rejected_products = validate_products(
            products_df,
            carts_df
        )

        run_metadata["records"]["valid_products"] = len(
            valid_products
        )

        run_metadata["records"]["rejected_products"] = len(
            rejected_products
        )

        logger.info("Valid products: %d", len(valid_products))
        logger.info("Rejected products: %d", len(rejected_products))

        # STEP 4: DATA QUALITY REPORT
        logger.info("STEP 4: DATA QUALITY REPORT")

        quality_report = generate_data_quality_report(
            total_records=len(products_df),
            valid_records=valid_products,
            rejected_records=rejected_products
        )

        logger.info(
            "Data quality rate: %.2f%%",
            quality_report["summary"]["data_quality_rate"]
        )

        # STEP 5: QUARANTINE REJECTED RECORDS
        logger.info("STEP 5: QUARANTINE")

        if not rejected_products.empty:

            rejected_folder = Path("data/rejected")
            rejected_folder.mkdir(parents=True, exist_ok=True)

            rejected_file = rejected_folder / "rejected_products.csv"

            rejected_products.to_csv(
                rejected_file,
                index=False
            )

            logger.warning(
                "%d rejected records saved to %s",
                len(rejected_products),
                rejected_file
            )

        else:

            logger.info("No rejected records found.")

        # STEP 6: DATABASE LOADING
        logger.info("STEP 6: DATABASE LOADING")

        run_metadata["records"]["carts_submitted_for_loading"] = len(
            carts_df
        )

        run_metadata["records"]["products_submitted_for_loading"] = len(
            valid_products
        )

        run_metadata["database_load_status"] = "RUNNING"

        try:

            load_data(carts_df, valid_products)

        except Exception:

            run_metadata["database_load_status"] = "FAILED"
            raise

        else:

            run_metadata["database_load_status"] = "SUCCESS"

        # STEP 7: PIPELINE COMPLETION
        logger.info("========== PIPELINE COMPLETED ==========")

        run_metadata["status"] = "SUCCESS"

    except Exception as error:

        run_metadata["status"] = "FAILED"
        run_metadata["error"] = str(error)

        logger.exception("Pipeline execution failed")

        raise

    finally:

        # Save execution metadata regardless of pipeline outcome
        try:

            metadata = finalize_pipeline_run(
                run_metadata,
                start_time,
                run_metadata["status"],
                run_metadata["error"]
            )

            logger.info(
                "Pipeline run metadata saved. Run ID: %s",
                metadata["run_id"]
            )

            logger.info(
                "Execution duration: %.3f seconds",
                metadata["duration_seconds"]
            )

        except Exception:

            logger.exception(
                "Failed to save pipeline run metadata"
            )


if __name__ == "__main__":
    run_pipeline()