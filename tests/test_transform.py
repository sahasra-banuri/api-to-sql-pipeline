import json
import pandas as pd

from transform import transform_cart_data


def create_sample_data(tmp_path):

    sample_data = {
        "carts": [
            {
                "id": 1,
                "userId": 10,
                "total": 1500,
                "discountedTotal": 1350,
                "totalProducts": 2,
                "totalQuantity": 3,
                "products": [
                    {
                        "id": 101,
                        "title": "Laptop",
                        "price": 1000,
                        "quantity": 1,
                        "total": 1000,
                        "discountPercentage": 10,
                        "discountedTotal": 900,
                        "thumbnail": "image1.jpg"
                    },
                    {
                        "id": 102,
                        "title": "Mouse",
                        "price": 500,
                        "quantity": 2,
                        "total": 1000,
                        "discountPercentage": 10,
                        "discountedTotal": 900,
                        "thumbnail": "image2.jpg"
                    }
                ]
            },
            {
                "id": 2,
                "userId": 20,
                "total": 2500,
                "discountedTotal": 2250,
                "totalProducts": 1,
                "totalQuantity": 1,
                "products": []
            }
        ]
    }

    raw_directory = tmp_path / "data" / "raw"
    raw_directory.mkdir(parents=True)

    input_file = raw_directory / "carts.json"

    with open(input_file, "w", encoding="utf-8") as file:
        json.dump(sample_data, file)

    return sample_data


def test_cart_records_are_extracted(tmp_path, monkeypatch):

    create_sample_data(tmp_path)
    monkeypatch.chdir(tmp_path)

    carts_df, products_df = transform_cart_data()

    assert len(carts_df) == 2


def test_nested_products_are_flattened(tmp_path, monkeypatch):

    create_sample_data(tmp_path)
    monkeypatch.chdir(tmp_path)

    carts_df, products_df = transform_cart_data()

    assert len(products_df) == 2


def test_product_cart_relationship_is_preserved(tmp_path, monkeypatch):

    create_sample_data(tmp_path)
    monkeypatch.chdir(tmp_path)

    carts_df, products_df = transform_cart_data()

    assert products_df.iloc[0]["cart_id"] == 1
    assert products_df.iloc[1]["cart_id"] == 1


def test_expected_columns_are_created(tmp_path, monkeypatch):

    create_sample_data(tmp_path)
    monkeypatch.chdir(tmp_path)

    carts_df, products_df = transform_cart_data()

    expected_cart_columns = [
        "cart_id",
        "user_id",
        "total",
        "discounted_total",
        "total_products",
        "total_quantity"
    ]

    expected_product_columns = [
        "cart_id",
        "product_id",
        "title",
        "price",
        "quantity",
        "total",
        "discount_percentage",
        "discounted_total"
    ]

    assert list(carts_df.columns) == expected_cart_columns
    assert list(products_df.columns) == expected_product_columns


def test_cart_without_products_is_preserved(tmp_path, monkeypatch):

    create_sample_data(tmp_path)
    monkeypatch.chdir(tmp_path)

    carts_df, products_df = transform_cart_data()

    assert 2 in carts_df["cart_id"].values
    assert 2 not in products_df["cart_id"].values