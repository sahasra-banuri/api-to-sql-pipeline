import pandas as pd


def validate_products(cart_products_df, carts_df):

    df = cart_products_df.copy()

    # Store rejection reasons for each record
    rejection_reasons = [[] for _ in range(len(df))]

    def add_reason(condition, reason):

        for index, is_invalid in enumerate(condition):
            if is_invalid:
                rejection_reasons[index].append(reason)

    # Check mandatory fields
    add_reason(
        df["cart_id"].isna(),
        "missing_cart_id"
    )

    add_reason(
        df["product_id"].isna(),
        "missing_product_id"
    )

    add_reason(
        df["title"].isna() | df["title"].astype(str).str.strip().eq(""),
        "missing_product_title"
    )

    # Check numerical conditions
    add_reason(
        df["price"].isna() | (df["price"] < 0),
        "invalid_price"
    )

    add_reason(
        df["quantity"].isna() | (df["quantity"] <= 0),
        "invalid_quantity"
    )

    add_reason(
        df["total"].isna() | (df["total"] < 0),
        "invalid_total"
    )

    add_reason(
        df["discount_percentage"].isna()
        | ~df["discount_percentage"].between(0, 100),
        "invalid_discount_percentage"
    )

    add_reason(
        df["discounted_total"].isna() | (df["discounted_total"] < 0),
        "invalid_discounted_total"
    )

    # Check whether cart exists
    add_reason(
        ~df["cart_id"].isin(carts_df["cart_id"]),
        "unknown_cart_id"
    )

    # Check duplicate cart-product combinations
    duplicates = df.duplicated(
        subset=["cart_id", "product_id"],
        keep="first"
    )

    add_reason(
        duplicates,
        "duplicate_cart_product"
    )

    # Combine rejection reasons
    df["rejection_reason"] = [
        ", ".join(reasons) for reasons in rejection_reasons
    ]

    # Separate valid and rejected records
    valid_records = df[df["rejection_reason"] == ""].copy()

    rejected_records = df[df["rejection_reason"] != ""].copy()

    return valid_records, rejected_records


if __name__ == "__main__":

    from transform import transform_cart_data

    carts_df, cart_products_df = transform_cart_data()

    valid_products, rejected_products = validate_products(
        cart_products_df,
        carts_df
    )

    print("Total products:", len(cart_products_df))
    print("Valid products:", len(valid_products))
    print("Rejected products:", len(rejected_products))

    print("\nRejected records:")
    print(rejected_products.to_string(index=False))
