
import pandas as pd
from pathlib import Path


# Find project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Location of raw CSV files
RAW_DIR = BASE_DIR / "data" / "raw"


def extract_data():

    print("Starting data extraction...\n")

    # Read CSV files
    sellers_df = pd.read_csv(RAW_DIR / "sellers.csv")

    products_df = pd.read_csv(RAW_DIR / "products.csv")

    orders_df = pd.read_csv(RAW_DIR / "orders.csv")

    order_items_df = pd.read_csv(RAW_DIR / "order_items.csv")

    # Store all datasets in a dictionary
    datasets = {
        "sellers": sellers_df,
        "products": products_df,
        "orders": orders_df,
        "order_items": order_items_df
    }

    print("All CSV files extracted successfully!\n")

    return datasets


if __name__ == "__main__":

    datasets = extract_data()

    # Inspect extracted datasets
    for name, df in datasets.items():

        print("=" * 50)
        print(f"Dataset: {name}")

        print("\nFirst 5 records:")
        print(df.head())

        print("\nDataset shape:")
        print(df.shape)

        print("\nColumn information:")
        df.info()

        print("\nMissing values:")
        print(df.isnull().sum())

        print("\nDuplicate records:")
        print(df.duplicated().sum())

        print()
