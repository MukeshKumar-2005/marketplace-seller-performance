
import csv
import random
import os
from datetime import datetime, timedelta

# Make generated data reproducible
random.seed(42)

# Project data directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

os.makedirs(RAW_DIR, exist_ok=True)


def generate_sellers():

    sellers = []

    cities = [
        "Chandigarh", "Mohali", "Delhi",
        "Mumbai", "Bangalore", "Pune",
        "Jaipur", "Hyderabad"
    ]

    for seller_id in range(1, 21):

        sellers.append({
            "seller_id": seller_id,
            "seller_name": f"Seller_{seller_id}",
            "email": f"seller{seller_id}@example.com",
            "city": random.choice(cities),
            "state": "India"
        })

    return sellers


def generate_products(sellers):

    products = []

    categories = {
        "Electronics": ["Laptop", "Mouse", "Keyboard", "Monitor"],
        "Fashion": ["T-Shirt", "Jeans", "Jacket", "Shoes"],
        "Home": ["Chair", "Table", "Lamp", "Sofa"],
        "Accessories": ["Watch", "Bag", "Wallet", "Belt"]
    }

    for product_id in range(1, 101):

        seller = random.choice(sellers)
        category = random.choice(list(categories.keys()))
        product_name = random.choice(categories[category])

        products.append({
            "product_id": product_id,
            "seller_id": seller["seller_id"],
            "product_name": product_name,
            "category": category,
            "price": round(random.uniform(200, 60000), 2),
            "stock_quantity": random.randint(0, 500)
        })

    return products


def generate_orders_and_items(products):

    orders = []
    order_items = []

    start_date = datetime(2026, 1, 1)

    for order_id in range(1, 501):

        order_date = start_date + timedelta(
            days=random.randint(0, 300),
            hours=random.randint(0, 23)
        )

        customer_id = random.randint(1, 200)

        order_status = random.choice([
            "Delivered",
            "Shipped",
            "Processing",
            "Cancelled"
        ])

        # Select 1 to 4 different products
        selected_products = random.sample(
            products,
            random.randint(1, 4)
        )

        total_amount = 0

        for product in selected_products:

            quantity = random.randint(1, 5)
            unit_price = product["price"]

            item_total = quantity * unit_price
            total_amount += item_total

            order_items.append({
                "order_item_id": len(order_items) + 1,
                "order_id": order_id,
                "product_id": product["product_id"],
                "seller_id": product["seller_id"],
                "quantity": quantity,
                "unit_price": unit_price
            })

        orders.append({
            "order_id": order_id,
            "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "customer_id": customer_id,
            "order_status": order_status,
            "total_amount": round(total_amount, 2)
        })

    return orders, order_items


def save_csv(filename, data):

    if not data:
        return

    filepath = os.path.join(RAW_DIR, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=data[0].keys()
        )

        writer.writeheader()
        writer.writerows(data)

    print(f"Created {filename}: {len(data)} records")


def main():

    print("Generating marketplace datasets...")

    sellers = generate_sellers()

    products = generate_products(sellers)

    orders, order_items = generate_orders_and_items(products)

    save_csv("sellers.csv", sellers)
    save_csv("products.csv", products)
    save_csv("orders.csv", orders)
    save_csv("order_items.csv", order_items)

    print("\nAll marketplace datasets generated successfully!")


if __name__ == "__main__":
    main()
