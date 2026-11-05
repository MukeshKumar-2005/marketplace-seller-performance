
import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Reusable MySQL connection function
def get_connection():

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
            return connection

    except mysql.connector.Error as error:
        print("MySQL connection failed:", error)
        return None


# Execute connection test only when running this file directly
if __name__ == "__main__":

    connection = get_connection()

    if connection:
        print("Database:", connection.database)

        connection.close()
        print("MySQL connection closed.")





# Create database tables
def create_tables():

    connection = get_connection()

    if connection is None:
        print("Database connection failed.")
        return

    cursor = connection.cursor()

    try:

        # 1. Sellers Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sellers (
                seller_id INT AUTO_INCREMENT PRIMARY KEY,
                seller_name VARCHAR(100) NOT NULL,
                email VARCHAR(150) UNIQUE,
                city VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. Products Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                seller_id INT,
                product_name VARCHAR(150) NOT NULL,
                category VARCHAR(100),
                price DECIMAL(10,2),
                stock INT DEFAULT 0,
                FOREIGN KEY (seller_id)
                REFERENCES sellers(seller_id)
            )
        """)

        # 3. Orders Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                seller_id INT,
                order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                order_status VARCHAR(50),
                total_amount DECIMAL(10,2),
                FOREIGN KEY (seller_id)
                REFERENCES sellers(seller_id)
            )
        """)

        # 4. Order Items Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                item_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT,
                product_id INT,
                quantity INT,
                unit_price DECIMAL(10,2),
                FOREIGN KEY (order_id)
                REFERENCES orders(order_id),
                FOREIGN KEY (product_id)
                REFERENCES products(product_id)
            )
        """)

        # 5. Payments Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                payment_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT,
                payment_method VARCHAR(50),
                payment_status VARCHAR(50),
                amount DECIMAL(10,2),
                payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id)
                REFERENCES orders(order_id)
            )
        """)

        connection.commit()

        print("All tables created successfully!")

    except mysql.connector.Error as error:
        connection.rollback()
        print("Error creating tables:", error)

    finally:
        cursor.close()
        connection.close()
        print("MySQL connection closed.")


if __name__ == "__main__":
    create_tables()
