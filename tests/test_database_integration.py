import os
import secrets

import pandas as pd
import pytest

from database import create_connection
from load_data import load_data


# Only execute these tests when explicitly enabled.
pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.getenv("RUN_DB_INTEGRATION") != "1",
        reason="Database integration tests are disabled."
    )
]


@pytest.fixture
def test_records():

    # Safety check: never allow these tests against the main database.
    database = os.getenv("MYSQL_DATABASE")

    if database != "ecommerce_pipeline_test":
        pytest.fail(
            "Integration tests can only run against "
            "ecommerce_pipeline_test."
        )

    if not os.getenv("MYSQL_PASSWORD"):
        pytest.fail(
            "Set MYSQL_PASSWORD before running integration tests."
        )

    # Generate unique IDs for each test execution.
    cart_id = 900000 + secrets.randbelow(99999)
    product_id = 800000 + secrets.randbelow(99999)

    # Create one cart record.
    carts_df = pd.DataFrame([
        {
            "cart_id": cart_id,
            "user_id": 501,
            "total": 500.00,
            "discounted_total": 450.00,
            "total_products": 1,
            "total_quantity": 2
        }
    ])

    # Create one product record.
    products_df = pd.DataFrame([
        {
            "cart_id": cart_id,
            "product_id": product_id,
            "title": "Integration Test Product",
            "price": 250.00,
            "quantity": 2,
            "total": 500.00,
            "discount_percentage": 10.00,
            "discounted_total": 450.00
        }
    ])

    yield {
        "cart_id": cart_id,
        "product_id": product_id,
        "carts_df": carts_df,
        "products_df": products_df
    }

    # Clean up test records after execution.
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM cart_products WHERE cart_id = %s",
            (cart_id,)
        )

        cursor.execute(
            "DELETE FROM carts WHERE cart_id = %s",
            (cart_id,)
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def get_record_counts(cart_id):

    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT COUNT(*) FROM carts WHERE cart_id = %s",
            (cart_id,)
        )

        cart_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM cart_products WHERE cart_id = %s",
            (cart_id,)
        )

        product_count = cursor.fetchone()[0]

        return cart_count, product_count

    finally:
        cursor.close()
        connection.close()


def test_initial_insertion(test_records):

    carts_df = test_records["carts_df"]
    products_df = test_records["products_df"]
    cart_id = test_records["cart_id"]

    load_data(carts_df, products_df)

    cart_count, product_count = get_record_counts(cart_id)

    assert cart_count == 1
    assert product_count == 1


def test_idempotent_loading(test_records):

    carts_df = test_records["carts_df"]
    products_df = test_records["products_df"]
    cart_id = test_records["cart_id"]

    # First execution.
    load_data(carts_df, products_df)

    first_counts = get_record_counts(cart_id)

    # Second execution with identical records.
    load_data(carts_df, products_df)

    second_counts = get_record_counts(cart_id)

    assert first_counts == (1, 1)
    assert second_counts == first_counts


def test_upsert_updates_existing_records(test_records):

    carts_df = test_records["carts_df"].copy()
    products_df = test_records["products_df"].copy()

    cart_id = test_records["cart_id"]
    product_id = test_records["product_id"]

    # First load.
    load_data(carts_df, products_df)

    # Modify existing values.
    carts_df.loc[0, "user_id"] = 999
    carts_df.loc[0, "total"] = 800.00

    products_df.loc[0, "title"] = "Updated Test Product"
    products_df.loc[0, "price"] = 400.00

    # Second load should update existing records.
    load_data(carts_df, products_df)

    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT user_id, total
            FROM carts
            WHERE cart_id = %s
            """,
            (cart_id,)
        )

        cart_result = cursor.fetchone()

        cursor.execute(
            """
            SELECT title, price
            FROM cart_products
            WHERE cart_id = %s AND product_id = %s
            """,
            (cart_id, product_id)
        )

        product_result = cursor.fetchone()

        assert cart_result == (999, 800.00)
        assert product_result == ("Updated Test Product", 400.00)

    finally:
        cursor.close()
        connection.close()


def test_transaction_rollback(test_records):

    carts_df = test_records["carts_df"].copy()
    products_df = test_records["products_df"].copy()

    cart_id = test_records["cart_id"]

    # Deliberately change the product's cart ID.
    # No corresponding parent cart will exist.
    products_df.loc[0, "cart_id"] = cart_id + 1

    # Cart insertion should succeed initially,
    # but product insertion should fail due to the foreign key.
    with pytest.raises(Exception):
        load_data(carts_df, products_df)

    # The failed product insertion should also roll back
    # the preceding cart insertion.
    cart_count, product_count = get_record_counts(cart_id)

    assert cart_count == 0
    assert product_count == 0