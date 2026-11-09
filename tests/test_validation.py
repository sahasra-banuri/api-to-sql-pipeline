import pandas as pd
import pytest

from validate import validate_products


def create_cart_data():
    return pd.DataFrame([
        {"cart_id": 1},
        {"cart_id": 2}
    ])


def create_product_data():
    return pd.DataFrame([
        {
            "cart_id": 1,
            "product_id": 101,
            "title": "Laptop",
            "price": 500.00,
            "quantity": 2,
            "total": 1000.00,
            "discount_percentage": 10.00,
            "discounted_total": 900.00
        }
    ])


def test_valid_product_is_accepted():

    products = create_product_data()
    carts = create_cart_data()

    valid, rejected = validate_products(products, carts)

    assert len(valid) == 1
    assert len(rejected) == 0


def test_negative_price_is_rejected():

    products = create_product_data()
    products.loc[0, "price"] = -100

    valid, rejected = validate_products(products, create_cart_data())

    assert len(valid) == 0
    assert len(rejected) == 1
    assert "invalid_price" in rejected.iloc[0]["rejection_reason"]


def test_zero_quantity_is_rejected():

    products = create_product_data()
    products.loc[0, "quantity"] = 0

    valid, rejected = validate_products(products, create_cart_data())

    assert len(valid) == 0
    assert "invalid_quantity" in rejected.iloc[0]["rejection_reason"]


def test_empty_title_is_rejected():

    products = create_product_data()
    products.loc[0, "title"] = "   "

    valid, rejected = validate_products(products, create_cart_data())

    assert len(valid) == 0
    assert "missing_product_title" in rejected.iloc[0]["rejection_reason"]


def test_unknown_cart_is_rejected():

    products = create_product_data()
    products.loc[0, "cart_id"] = 999

    valid, rejected = validate_products(products, create_cart_data())

    assert len(valid) == 0
    assert "unknown_cart_id" in rejected.iloc[0]["rejection_reason"]


def test_duplicate_cart_product_is_rejected():

    products = create_product_data()

    duplicate = products.copy()

    products = pd.concat(
        [products, duplicate],
        ignore_index=True
    )

    valid, rejected = validate_products(products, create_cart_data())

    assert len(valid) == 1
    assert len(rejected) == 1
    assert "duplicate_cart_product" in rejected.iloc[0]["rejection_reason"]


def test_multiple_validation_errors_are_recorded():

    products = create_product_data()

    products.loc[0, "price"] = -100
    products.loc[0, "quantity"] = 0

    valid, rejected = validate_products(products, create_cart_data())

    reasons = rejected.iloc[0]["rejection_reason"]

    assert len(valid) == 0
    assert "invalid_price" in reasons
    assert "invalid_quantity" in reasons


def test_original_dataframe_remains_unchanged():

    products = create_product_data()
    original = products.copy(deep=True)

    validate_products(products, create_cart_data())

    pd.testing.assert_frame_equal(products, original)