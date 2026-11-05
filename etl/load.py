import sys
import pandas as pd
from pathlib import Path

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Add project root to Python import path
sys.path.insert(0, str(BASE_DIR))

# Import reusable MySQL connection
from db_connection import get_connection

# Processed CSV directory
PROCESSED_DIR = BASE_DIR / "data" / "processed"
def insert_data(cursor, query, dataframe):

    records = []

    for row in dataframe.itertuples(index=False, name=None):

        cleaned_row = tuple(
            value.to_pydatetime()
            if isinstance(value, pd.Timestamp)
            else value
            for value in row
        )

        records.append(cleaned_row)

    cursor.executemany(query, records)

    print(f"Inserted {cursor.rowcount} records.")

def load_data():

    connection = get_connection()

    if connection is None:
        print("Database connection failed!")
        return

    cursor = connection.cursor()

    try:

        print("\nStarting data loading...\n")

        # Read processed CSV files
        sellers = pd.read_csv(PROCESSED_DIR / "sellers.csv")

        products = pd.read_csv(PROCESSED_DIR / "products.csv")

        orders = pd.read_csv(
            PROCESSED_DIR / "orders.csv",
            parse_dates=["order_date"]
        )

        order_items = pd.read_csv(
            PROCESSED_DIR / "order_items.csv"
        )

        # --------------------------------
        # 1. Load Sellers
        # --------------------------------

        print("Loading sellers...")

        seller_query = """
            INSERT INTO sellers
            (seller_id, seller_name, email, city, state)
            VALUES (%s, %s, %s, %s, %s)
        """

        insert_data(cursor, seller_query, sellers)

        # --------------------------------
        # 2. Load Products
        # --------------------------------

        print("\nLoading products...")

        product_query = """
            INSERT INTO products
            (product_id, seller_id, product_name,
             category, price, stock_quantity)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        insert_data(cursor, product_query, products)

        # --------------------------------
        # 3. Load Orders
        # --------------------------------

        print("\nLoading orders...")

        order_query = """
            INSERT INTO orders
            (order_id, order_date, customer_id,
             order_status, total_amount)
            VALUES (%s, %s, %s, %s, %s)
        """

        insert_data(cursor, order_query, orders)

        # --------------------------------
        # 4. Load Order Items
        # --------------------------------

        print("\nLoading order items...")

        order_item_query = """
            INSERT INTO order_items
            (order_item_id, order_id, product_id,
             seller_id, quantity, unit_price)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        insert_data(cursor, order_item_query, order_items)

        # --------------------------------
        # 5. Calculate Seller Performance
        # --------------------------------

        print("\nCalculating seller performance...")

        performance_query = """
            INSERT INTO seller_performance
            (
                seller_id,
                total_orders,
                total_revenue,
                average_order_value,
                performance_date
            )
            SELECT
                seller_id,
                COUNT(DISTINCT order_id),
                SUM(quantity * unit_price),
                SUM(quantity * unit_price) /
                    COUNT(DISTINCT order_id),
                CURDATE()
            FROM order_items
            GROUP BY seller_id
        """

        cursor.execute(performance_query)

        print(
            f"Seller performance records: {cursor.rowcount}"
        )

        # Commit all database changes
        connection.commit()

        print("\nAll data loaded successfully!")

    except Exception as error:

        connection.rollback()

        print("\nData loading failed:", error)
        print("All changes have been rolled back.")

    finally:

        cursor.close()
        connection.close()

        print("MySQL connection closed.")


if __name__ == "__main__":
    load_data()
