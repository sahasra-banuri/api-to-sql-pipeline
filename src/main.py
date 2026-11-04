from pathlib import Path

from ingestion import ingest_data
from transform import transform_cart_data
from validate import validate_products
from load_data import load_data
from pipeline_logger import setup_logger


logger = setup_logger()


def run_pipeline():

    logger.info("========== PIPELINE STARTED ==========")

    try:

        # STEP 1: INGESTION
        logger.info("STEP 1: INGESTION")

        ingest_data()


        # STEP 2: TRANSFORMATION
        logger.info("STEP 2: TRANSFORMATION")

        carts_df, products_df = transform_cart_data()

        logger.info("Cart records: %d", len(carts_df))
        logger.info("Product records: %d", len(products_df))


        # STEP 3: VALIDATION
        logger.info("STEP 3: VALIDATION")

        valid_products, rejected_products = validate_products(
            products_df,
            carts_df
        )

        logger.info("Valid products: %d", len(valid_products))
        logger.info("Rejected products: %d", len(rejected_products))


        # STEP 4: QUARANTINE REJECTED RECORDS
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


        # STEP 5: DATABASE LOADING
        logger.info("STEP 5: DATABASE LOADING")

        load_data(carts_df, valid_products)


        # STEP 6: PIPELINE SUMMARY
        logger.info("========== PIPELINE COMPLETED ==========")

        logger.info("Total carts processed: %d", len(carts_df))
        logger.info("Total products processed: %d", len(products_df))
        logger.info("Valid products: %d", len(valid_products))
        logger.info("Rejected products: %d", len(rejected_products))


    except Exception:

        logger.exception("Pipeline execution failed")

        raise


if __name__ == "__main__":
    run_pipeline()