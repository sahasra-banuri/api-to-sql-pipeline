import os
import mysql.connector
from getpass import getpass


def create_connection():

    # Read database configuration from environment variables
    host = os.getenv("MYSQL_HOST", "localhost")
    user = os.getenv("MYSQL_USER", "root")
    database = os.getenv(
        "MYSQL_DATABASE",
        "ecommerce_pipeline"
    )

    # Prefer environment variable; otherwise request password securely
    password = os.getenv("MYSQL_PASSWORD")

    if not password:
        password = getpass("Enter MySQL password: ")

    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    print(f"Successfully connected to MySQL database: {database}")

    return connection


if __name__ == "__main__":

    connection = create_connection()

    connection.close()

    print("Database connection closed.")