
import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_connection():
    """Create and return a MySQL database connection."""

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", "3306"))
        )

        if connection.is_connected():
            print("Successfully connected to MySQL!")
            print("Database:", connection.database)
            return connection

    except mysql.connector.Error as error:
        print("MySQL connection failed:", error)
        return None


# Run this test only when executing this file directly
if __name__ == "__main__":

    connection = get_connection()

    if connection:
        connection.close()
        print("MySQL connection closed.")
