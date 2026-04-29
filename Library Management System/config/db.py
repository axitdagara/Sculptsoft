

import mysql.connector
from mysql.connector import Error


def create_connection():
    """
    Create and return MySQL database connection
    """

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="library_management_system"
        )

        if connection.is_connected():
            print("Database connected successfully")

        return connection

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def get_cursor(connection):
    """
    Return cursor object
    """

    return connection.cursor(dictionary=True)



if __name__ == "__main__":

    connection = create_connection()

    if connection:

        cursor = get_cursor(connection)

        cursor.execute("SELECT * FROM books")

        books = cursor.fetchall()

        print("\nBooks Table:\n")

        for book in books:
            print(book)

        cursor.close()
        connection.close()

        print("\nDatabase connection closed")
