import os
import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor


dotenv.load_dotenv()


def create_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv("host"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            database=os.getenv("database"),
            port=os.getenv("port")
        )

        print("PostgreSQL connected successfully")

        return connection

    except Exception as e:
        print(f"Error while connecting to PostgreSQL: {e}")
        return None



def get_cursor(connection):
    return connection.cursor(cursor_factory=RealDictCursor)


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