
import sys
from pathlib import Path

import pandas as pd

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Import MySQL connection function
from db_connection import get_connection


# Store all SQL analytics queries
QUERIES = {

    "top_sellers": """
        SELECT
            s.seller_id,
            s.seller_name,
            s.city,
            COUNT(DISTINCT oi.order_id) AS total_orders,
            SUM(oi.quantity) AS total_items_sold,
            SUM(oi.quantity * oi.unit_price) AS total_revenue
        FROM sellers s
        INNER JOIN order_items oi
            ON s.seller_id = oi.seller_id
        GROUP BY s.seller_id, s.seller_name, s.city
        ORDER BY total_revenue DESC
        LIMIT 5;
    """,

    "category_revenue": """
        SELECT
            p.category,
            COUNT(DISTINCT oi.order_id) AS total_orders,
            SUM(oi.quantity) AS total_items_sold,
            SUM(oi.quantity * oi.unit_price) AS total_revenue
        FROM products p
        INNER JOIN order_items oi
            ON p.product_id = oi.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC;
    """,

    "monthly_revenue": """
        SELECT
            DATE_FORMAT(o.order_date, '%Y-%m') AS revenue_month,
            COUNT(DISTINCT o.order_id) AS total_orders,
            SUM(oi.quantity) AS total_items_sold,
            SUM(oi.quantity * oi.unit_price) AS monthly_revenue
        FROM orders o
        INNER JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
        ORDER BY revenue_month ASC;
    """,

    "average_order_value": """
        SELECT
            COUNT(DISTINCT o.order_id) AS total_orders,
            SUM(oi.quantity * oi.unit_price) AS total_revenue,
            ROUND(
                SUM(oi.quantity * oi.unit_price)
                / COUNT(DISTINCT o.order_id), 2
            ) AS average_order_value
        FROM orders o
        INNER JOIN order_items oi
            ON o.order_id = oi.order_id;
    """,

    "best_selling_products": """
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            SUM(oi.quantity) AS total_quantity_sold,
            COUNT(DISTINCT oi.order_id) AS total_orders,
            SUM(oi.quantity * oi.unit_price) AS total_revenue
        FROM products p
        INNER JOIN order_items oi
            ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name, p.category
        ORDER BY total_quantity_sold DESC
        LIMIT 10;
    """,

    "seller_ranking": """
        SELECT
            s.seller_id,
            s.seller_name,
            s.city,
            sp.total_orders,
            sp.total_revenue,
            sp.average_order_value,
            RANK() OVER (
                ORDER BY sp.total_revenue DESC
            ) AS revenue_rank
        FROM seller_performance sp
        INNER JOIN sellers s
            ON sp.seller_id = s.seller_id
        ORDER BY revenue_rank ASC;
    """
}


def run_analytics():

    connection = None
    cursor = None

    try:
        # Connect to MySQL
        connection = get_connection()

        if connection is None:
            print("Database connection failed.")
            return

        print("\nMySQL connection successful!")

        # Create output directory
        output_dir = BASE_DIR / "data" / "processed"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create cursor
        cursor = connection.cursor(dictionary=True)

        # Execute each analytics query
        for report_name, query in QUERIES.items():

            print(f"\nRunning: {report_name}")

            cursor.execute(query)

            results = cursor.fetchall()

            # Convert SQL results into DataFrame
            df = pd.DataFrame(results)

            # Save DataFrame as CSV
            output_file = output_dir / f"{report_name}.csv"
            df.to_csv(output_file, index=False)

            print(f"Records: {len(df)}")
            print(df.to_string(index=False))
            print(f"Saved: {output_file}")

        print("\nAll analytics reports generated successfully!")

    except Exception as error:
        print("\nAnalytics failed:", error)

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()
            print("\nMySQL connection closed.")


if __name__ == "__main__":
    run_analytics()
