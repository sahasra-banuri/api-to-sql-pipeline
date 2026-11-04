from database import create_connection


def load_data(carts_df, valid_products):

    connection = create_connection()
    cursor = connection.cursor()

    try:

        # Clear existing records (full refresh)
        cursor.execute("DELETE FROM cart_products")
        cursor.execute("DELETE FROM carts")


        # INSERT CART RECORDS
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
        """

        cursor.executemany(cart_query, cart_records)


        # INSERT VALID PRODUCT RECORDS
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
        """

        cursor.executemany(product_query, product_records)


        # COMMIT TRANSACTION
        connection.commit()

        print("\nData successfully loaded!")
        print("Cart records inserted:", len(cart_records))
        print("Product records inserted:", len(product_records))


    except Exception as error:

        connection.rollback()

        print("Data loading failed:", error)
        print("Transaction rolled back.")

        raise


    finally:

        cursor.close()
        connection.close()