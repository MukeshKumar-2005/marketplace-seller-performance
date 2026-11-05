from fastapi import APIRouter, HTTPException

from db_connection import get_connection

from api.schemas.analytics import (
    TopSellersResponse,
    CategoryRevenueResponse,
    MonthlyRevenueResponse,
    AverageOrderValueResponse,
    BestSellingProductsResponse,
    SellerRankingResponse,
)

router = APIRouter()


# Health check endpoint
@router.get("/health")
def health_check():

    return {
        "status": "success",
        "message": "Analytics API is working!"
    }


# Top sellers analytics endpoint
@router.get("/analytics/top-sellers", response_model=TopSellersResponse)

def get_top_sellers():

    connection = None
    cursor = None

    try:
        # Connect to MySQL
        connection = get_connection()

        if connection is None:
            raise HTTPException(
                status_code=500,
                detail="Database connection failed"
            )

        # Create dictionary cursor
        cursor = connection.cursor(dictionary=True)

        # Execute top sellers SQL query
        query = """
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
        """

        cursor.execute(query)

        # Fetch all five seller records
        results = cursor.fetchall()

        # Return JSON response
        return {
            "status": "success",
            "total_records": len(results),
            "data": results
        }

    except HTTPException:
        raise

    except Exception as error:
        print("Top sellers API error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch top sellers"
        )

    finally:

        # Close cursor
        if cursor:
            cursor.close()

        # Close database connection
        if connection and connection.is_connected():
            connection.close()





# Category revenue analytics endpoint
@router.get("/analytics/category-revenue", response_model=CategoryRevenueResponse)
def get_category_revenue():

    connection = None
    cursor = None

    try:
        # Connect to MySQL
        connection = get_connection()

        if connection is None:
            raise HTTPException(
                status_code=500,
                detail="Database connection failed"
            )

        # Create dictionary cursor
        cursor = connection.cursor(dictionary=True)

        # SQL query to calculate category revenue
        query = """
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
        """

        # Execute query
        cursor.execute(query)

        # Fetch results
        results = cursor.fetchall()

        # Return JSON response
        return {
            "status": "success",
            "total_records": len(results),
            "data": results
        }

    except HTTPException:
        raise

    except Exception as error:
        print("Category revenue API error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch category revenue"
        )

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()




# Monthly revenue analytics endpoint
@router.get("/analytics/monthly-revenue", response_model=MonthlyRevenueResponse)
def get_monthly_revenue():

    connection = None
    cursor = None

    try:
        # Connect to MySQL
        connection = get_connection()

        if connection is None:
            raise HTTPException(
                status_code=500,
                detail="Database connection failed"
            )

        # Create dictionary cursor
        cursor = connection.cursor(dictionary=True)

        # SQL query for monthly revenue
        query = """
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
        """

        # Execute query
        cursor.execute(query)

        # Fetch results
        results = cursor.fetchall()

        # Return JSON response
        return {
            "status": "success",
            "total_records": len(results),
            "data": results
        }

    except HTTPException:
        raise

    except Exception as error:
        print("Monthly revenue API error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch monthly revenue"
        )

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# Average order value analytics endpoint
@router.get("/analytics/average-order-value", response_model=AverageOrderValueResponse)
def get_average_order_value():

    connection = None
    cursor = None

    try:
        # Connect to MySQL
        connection = get_connection()

        if connection is None:
            raise HTTPException(
                status_code=500,
                detail="Database connection failed"
            )

        # Create dictionary cursor
        cursor = connection.cursor(dictionary=True)

        # SQL query for average order value
        query = """
            SELECT
                COUNT(DISTINCT o.order_id) AS total_orders,

                SUM(oi.quantity * oi.unit_price) AS total_revenue,

                ROUND(
                    SUM(oi.quantity * oi.unit_price)
                    / NULLIF(COUNT(DISTINCT o.order_id), 0),
                    2
                ) AS average_order_value

            FROM orders o

            INNER JOIN order_items oi
                ON o.order_id = oi.order_id;
        """

        # Execute query
        cursor.execute(query)

        # Fetch result
        result = cursor.fetchone()

        # Return JSON response
        return {
            "status": "success",
            "data": result
        }

    except HTTPException:
        raise

    except Exception as error:
        print("Average order value API error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to calculate average order value"
        )

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()




# Best-selling products analytics endpoint
@router.get("/analytics/best-products", response_model=BestSellingProductsResponse)
def get_best_selling_products():

    connection = None
    cursor = None

    try:
        # Connect to MySQL
        connection = get_connection()

        if connection is None:
            raise HTTPException(
                status_code=500,
                detail="Database connection failed"
            )

        # Create dictionary cursor
        cursor = connection.cursor(dictionary=True)

        # SQL query for best-selling products
        query = """
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

            GROUP BY
                p.product_id,
                p.product_name,
                p.category

            ORDER BY total_quantity_sold DESC

            LIMIT 10;
        """

        # Execute SQL query
        cursor.execute(query)

        # Fetch results
        results = cursor.fetchall()

        # Return JSON response
        return {
            "status": "success",
            "total_records": len(results),
            "data": results
        }

    except HTTPException:
        raise

    except Exception as error:
        print("Best-selling products API error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch best-selling products"
        )

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()



# Seller ranking analytics endpoint
@router.get("/analytics/seller-ranking", response_model=SellerRankingResponse)
def get_seller_ranking():

    connection = None
    cursor = None

    try:
        # Connect to MySQL
        connection = get_connection()

        if connection is None:
            raise HTTPException(
                status_code=500,
                detail="Database connection failed"
            )

        # Create dictionary cursor
        cursor = connection.cursor(dictionary=True)

        # SQL query for seller ranking
        query = """
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

        # Execute query
        cursor.execute(query)

        # Fetch all seller rankings
        results = cursor.fetchall()

        # Return JSON response
        return {
            "status": "success",
            "total_records": len(results),
            "data": results
        }

    except HTTPException:
        raise

    except Exception as error:
        print("Seller ranking API error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch seller rankings"
        )

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()