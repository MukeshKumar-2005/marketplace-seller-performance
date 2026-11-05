
from pydantic import BaseModel


# Top Seller Schema
class TopSeller(BaseModel):
    seller_id: int
    seller_name: str
    city: str
    total_orders: int
    total_items_sold: int
    total_revenue: float


class TopSellersResponse(BaseModel):
    status: str
    total_records: int
    data: list[TopSeller]


# Category Revenue Schema
class CategoryRevenue(BaseModel):
    category: str
    total_orders: int
    total_items_sold: int
    total_revenue: float


class CategoryRevenueResponse(BaseModel):
    status: str
    total_records: int
    data: list[CategoryRevenue]


# Monthly Revenue Schema
class MonthlyRevenue(BaseModel):
    revenue_month: str
    total_orders: int
    total_items_sold: int
    monthly_revenue: float


class MonthlyRevenueResponse(BaseModel):
    status: str
    total_records: int
    data: list[MonthlyRevenue]


# Average Order Value Schema
class AverageOrderValue(BaseModel):
    total_orders: int
    total_revenue: float
    average_order_value: float | None


class AverageOrderValueResponse(BaseModel):
    status: str
    data: AverageOrderValue


# Best-Selling Products Schema
class BestSellingProduct(BaseModel):
    product_id: int
    product_name: str
    category: str
    total_quantity_sold: int
    total_orders: int
    total_revenue: float


class BestSellingProductsResponse(BaseModel):
    status: str
    total_records: int
    data: list[BestSellingProduct]


# Seller Ranking Schema
class SellerRanking(BaseModel):
    seller_id: int
    seller_name: str
    city: str
    total_orders: int
    total_revenue: float
    average_order_value: float
    revenue_rank: int


class SellerRankingResponse(BaseModel):
    status: str
    total_records: int
    data: list[SellerRanking]
