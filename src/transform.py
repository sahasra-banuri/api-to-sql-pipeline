import json
import pandas as pd
from pathlib import Path


def transform_cart_data():

    # Locate the raw JSON file
    input_file = Path("data/raw/carts.json")

    # Load JSON data
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    cart_records = []
    product_records = []

    # Iterate through every cart
    for cart in data["carts"]:

        # Extract cart-level information
        cart_records.append({
            "cart_id": cart["id"],
            "user_id": cart["userId"],
            "total": cart["total"],
            "discounted_total": cart["discountedTotal"],
            "total_products": cart["totalProducts"],
            "total_quantity": cart["totalQuantity"]
        })

        # Extract individual products
        for product in cart["products"]:

            product_records.append({
                "cart_id": cart["id"],
                "product_id": product["id"],
                "title": product["title"],
                "price": product["price"],
                "quantity": product["quantity"],
                "total": product["total"],
                "discount_percentage": product["discountPercentage"],
                "discounted_total": product["discountedTotal"]
            })

    # Convert records into DataFrames
    carts_df = pd.DataFrame(cart_records)
    cart_products_df = pd.DataFrame(product_records)

    return carts_df, cart_products_df


if __name__ == "__main__":

    carts_df, cart_products_df = transform_cart_data()

    print("CART DATA")
    print(carts_df.head())

    print("\nPRODUCT DATA")
    print(cart_products_df.head())

    print("\nTotal cart records:", len(carts_df))
    print("Total product records:", len(cart_products_df))