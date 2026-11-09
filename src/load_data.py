from database import create_connection


def load_data(carts_df, valid_products):

    connection = create_connection()
    cursor = connection.cursor()

    try:

        # STEP 1: Prepare cart records

        cart_columns = [
            "cart_id",
            "user_id",
            "total",
            "discounted_total",
            "total_products",
            "total_quantity"
        ]

        cart_records = [
            tuple(row)
            for row in carts_df[cart_columns].itertuples(
                index=False,
                name=None
            )
        ]


        # STEP 2: Insert or update carts

        cart_query = """
        INSERT INTO carts (
            cart_id,
            user_id,
            total,
            discounted_total,
            total_products,
            total_quantity
        )
        VALUES (%s, %s, %s, %s, %s, %s)

        ON DUPLICATE KEY UPDATE
            user_id = VALUES(user_id),
            total = VALUES(total),
            discounted_total = VALUES(discounted_total),
            total_products = VALUES(total_products),
            total_quantity = VALUES(total_quantity)
        """

        cursor.executemany(cart_query, cart_records)


        # STEP 3: Prepare valid product records

        product_columns = [
            "cart_id",
            "product_id",
            "title",
            "price",
            "quantity",
            "total",
            "discount_percentage",
            "discounted_total"
        ]

        product_records = [
            tuple(row)
            for row in valid_products[product_columns].itertuples(
                index=False,
                name=None
            )
        ]


        # STEP 4: Insert or update products

        product_query = """
        INSERT INTO cart_products (
            cart_id,
            product_id,
            title,
            price,
            quantity,
            total,
            discount_percentage,
            discounted_total
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            price = VALUES(price),
            quantity = VALUES(quantity),
            total = VALUES(total),
            discount_percentage = VALUES(discount_percentage),
            discounted_total = VALUES(discounted_total)
        """

        cursor.executemany(product_query, product_records)


        # STEP 5: Commit transaction

        connection.commit()

        print("\nIncremental data loading successful!")
        print("Cart records processed:", len(cart_records))
        print("Product records processed:", len(product_records))


    except Exception as error:

        connection.rollback()

        print("Data loading failed:", error)
        print("Transaction rolled back.")

        raise


    finally:

        cursor.close()
        connection.close()