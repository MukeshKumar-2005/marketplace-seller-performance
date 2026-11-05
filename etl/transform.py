
import pandas as pd
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Output directory for cleaned datasets
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def transform_data(datasets):

    print("\nStarting data transformation...\n")

    # Create copies so raw datasets remain unchanged
    sellers = datasets["sellers"].copy()
    products = datasets["products"].copy()
    orders = datasets["orders"].copy()
    order_items = datasets["order_items"].copy()

    # --------------------------------
    # 1. Remove duplicate records
    # --------------------------------

    sellers = sellers.drop_duplicates()
    products = products.drop_duplicates()
    orders = orders.drop_duplicates()
    order_items = order_items.drop_duplicates()
    # --------------------------------
    # 2. Clean text columns
    # --------------------------------

    sellers["seller_name"] = sellers["seller_name"].str.strip()
    sellers["email"] = sellers["email"].str.strip().str.lower()
    sellers["city"] = sellers["city"].fillna("Unknown").str.strip()

    products["product_name"] = products["product_name"].str.strip()
    products["category"] = products["category"].str.strip()

    orders["order_status"] = orders["order_status"].str.strip().str.title()

    # --------------------------------
    # 3. Handle data types
    # --------------------------------

    orders["order_date"] = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    if orders["order_date"].isna().any():
        raise ValueError("Invalid order dates found!")

    # --------------------------------
    # 4. Validate primary keys
    # --------------------------------

    primary_keys = {
        "sellers": (sellers, "seller_id"),
        "products": (products, "product_id"),
        "orders": (orders, "order_id"),
        "order_items": (order_items, "order_item_id")
    }

    for table_name, (df, column) in primary_keys.items():

        if df[column].isna().any():
            raise ValueError(f"Missing primary key in {table_name}")

        if df[column].duplicated().any():
            raise ValueError(f"Duplicate primary keys in {table_name}")

    # --------------------------------
    # 5. Validate foreign keys
    # --------------------------------

    if not products["seller_id"].isin(sellers["seller_id"]).all():
        raise ValueError("Invalid seller_id found in products!")

    if not order_items["order_id"].isin(orders["order_id"]).all():
        raise ValueError("Invalid order_id found in order_items!")

    if not order_items["product_id"].isin(products["product_id"]).all():
        raise ValueError("Invalid product_id found in order_items!")

    if not order_items["seller_id"].isin(sellers["seller_id"]).all():
        raise ValueError("Invalid seller_id found in order_items!")

    # Verify that an order item belongs to the
    # same seller who owns its product
    product_sellers = products.set_index("product_id")["seller_id"]

    expected_sellers = order_items["product_id"].map(product_sellers)

    if not order_items["seller_id"].eq(expected_sellers).all():
        raise ValueError("Product and seller relationship mismatch!")

    # --------------------------------
    # 6. Validate numeric values
    # --------------------------------

    if (products["price"] <= 0).any():
        raise ValueError("Invalid product prices found!")

    if (products["stock_quantity"] < 0).any():
        raise ValueError("Invalid stock quantities found!")

    if (order_items["quantity"] <= 0).any():
        raise ValueError("Invalid order quantities found!")

    if (order_items["unit_price"] <= 0).any():
        raise ValueError("Invalid order item prices found!")

    if (orders["total_amount"] < 0).any():
        raise ValueError("Invalid order totals found!")

    # --------------------------------
    # 7. Validate order amounts
    # --------------------------------

    item_totals = (
        order_items.assign(
            item_total=order_items["quantity"] *
                       order_items["unit_price"]
        )
        .groupby("order_id")["item_total"]
        .sum()
    )

    calculated_totals = orders["order_id"].map(item_totals)

    if calculated_totals.isna().any():
        raise ValueError("Some orders have no order items!")

    if not (
        (calculated_totals - orders["total_amount"]).abs() <= 0.01
    ).all():
        raise ValueError("Order total does not match order items!")

    # --------------------------------
    # 8. Store transformed datasets
    # --------------------------------

    cleaned_datasets = {
        "sellers": sellers,
        "products": products,
        "orders": orders,
        "order_items": order_items
    }

    print("Data transformation completed successfully!\n")

    return cleaned_datasets


def save_processed_data(datasets):

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    for name, df in datasets.items():

        filepath = PROCESSED_DIR / f"{name}.csv"

        df.to_csv(filepath, index=False)

        print(f"Saved {name}.csv: {len(df)} records")


if __name__ == "__main__":

    # Import extraction function
    from extract import extract_data

    # Extract raw data
    raw_datasets = extract_data()

    # Transform raw data
    cleaned_datasets = transform_data(raw_datasets)

    # Save cleaned datasets
    save_processed_data(cleaned_datasets)

    # Display final results
    print("\nFinal dataset information:")

    for name, df in cleaned_datasets.items():

        print(f"{name}: {df.shape[0]} rows, {df.shape[1]} columns")

    print("\nETL transformation stage completed!")
