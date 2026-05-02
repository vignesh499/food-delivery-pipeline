import pandas as pd
import os
import sys


EXPECTED_SCHEMAS = {
    "orders": [
        "order_id", "customer_id", "restaurant_id", "order_date", "order_time",
        "order_value", "discount", "delivery_fee", "total_amount", "payment_mode",
        "order_status", "preparation_time_min", "delivery_time_min",
        "delivery_rating", "delivery_distance_km"
    ],
    "customers": [
        "customer_id", "customer_name", "customer_city",
        "customer_rating", "signup_date"
    ],
    "restaurants": [
        "restaurant_id", "restaurant_name", "restaurant_city",
        "cuisine_type", "restaurant_rating", "avg_delivery_time_min"
    ]
}


def validate_schema(df, name):
    expected = EXPECTED_SCHEMAS.get(name)
    if expected is None:
        raise ValueError(f"Unknown dataset name: {name}")

    actual = list(df.columns)
    missing = set(expected) - set(actual)
    extra = set(actual) - set(expected)

    if missing:
        raise ValueError(f"[{name}] Missing columns: {missing}")

    if extra:
        print(f"[{name}] Warning: Extra columns found (will be ignored): {extra}")

    return True


def validate_not_empty(df, name):
    if df.empty:
        raise ValueError(f"[{name}] Dataset is empty — aborting ingestion")
    return True


def validate_primary_key(df, name, key_col):
    duplicates = df[key_col].duplicated().sum()
    if duplicates > 0:
        print(f"[{name}] Warning: {duplicates} duplicate {key_col} values found")
    return duplicates


def load_csv(file_path, name):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    print(f"[Ingest] Loading {name} from {file_path}...")
    df = pd.read_csv(file_path)

    validate_not_empty(df, name)
    validate_schema(df, name)

    print(f"[Ingest] {name}: {df.shape[0]} rows, {df.shape[1]} columns loaded")
    return df


def ingest_all(raw_dir="data/raw"):
    orders = load_csv(os.path.join(raw_dir, "orders.csv"), "orders")
    customers = load_csv(os.path.join(raw_dir, "customers.csv"), "customers")
    restaurants = load_csv(os.path.join(raw_dir, "restaurants.csv"), "restaurants")

    validate_primary_key(orders, "orders", "order_id")
    validate_primary_key(customers, "customers", "customer_id")
    validate_primary_key(restaurants, "restaurants", "restaurant_id")

    orphan_customers = set(orders["customer_id"]) - set(customers["customer_id"])
    orphan_restaurants = set(orders["restaurant_id"]) - set(restaurants["restaurant_id"])

    if orphan_customers:
        print(f"[Ingest] Warning: {len(orphan_customers)} orders reference missing customers")
    if orphan_restaurants:
        print(f"[Ingest] Warning: {len(orphan_restaurants)} orders reference missing restaurants")

    print(f"[Ingest] All datasets loaded successfully")
    return orders, customers, restaurants


if __name__ == "__main__":
    orders, customers, restaurants = ingest_all()
    print(f"\nOrders sample:\n{orders.head(3)}")
    print(f"\nNull counts in orders:\n{orders.isnull().sum()}")
