import mysql.connector
from getpass import getpass


def create_connection():

    password = getpass("Enter MySQL password:")

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="ecommerce_pipeline"
    )

    print("Successfully connected to MySQL!")

    return connection


if __name__ == "__main__":

    connection = create_connection()

    connection.close()

    print("Database connection closed.")