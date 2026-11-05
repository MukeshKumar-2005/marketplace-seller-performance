
import pytest
from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


# Test 1: Health Check
def test_health_check():

    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"


# Tests 2-6: Analytics List Endpoints
@pytest.mark.parametrize(
    "endpoint, expected_fields",
    [
        (
            "/api/analytics/top-sellers",
            ["seller_id", "seller_name", "city",
             "total_orders", "total_items_sold", "total_revenue"]
        ),
        (
            "/api/analytics/category-revenue",
            ["category", "total_orders",
             "total_items_sold", "total_revenue"]
        ),
        (
            "/api/analytics/monthly-revenue",
            ["revenue_month", "total_orders",
             "total_items_sold", "monthly_revenue"]
        ),
        (
            "/api/analytics/best-products",
            ["product_id", "product_name", "category",
             "total_quantity_sold", "total_orders", "total_revenue"]
        ),
        (
            "/api/analytics/seller-ranking",
            ["seller_id", "seller_name", "city",
             "total_orders", "total_revenue",
             "average_order_value", "revenue_rank"]
        ),
    ]
)
def test_analytics_endpoints(endpoint, expected_fields):

    response = client.get(endpoint)

    assert response.status_code == 200

    result = response.json()

    assert result["status"] == "success"
    assert isinstance(result["data"], list)
    assert result["total_records"] == len(result["data"])

    for record in result["data"]:
        for field in expected_fields:
            assert field in record


# Test 7: Average Order Value
def test_average_order_value():

    response = client.get("/api/analytics/average-order-value")

    assert response.status_code == 200

    result = response.json()

    assert result["status"] == "success"
    assert isinstance(result["data"], dict)

    assert "total_orders" in result["data"]
    assert "total_revenue" in result["data"]
    assert "average_order_value" in result["data"]


# Test 8: Seller Ranking Order
def test_seller_ranking_order():

    response = client.get("/api/analytics/seller-ranking")

    assert response.status_code == 200

    data = response.json()["data"]

    revenues = [
        seller["total_revenue"]
        for seller in data
    ]

    assert revenues == sorted(revenues, reverse=True)
