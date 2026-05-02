import pandas as pd
import numpy as np
import os


def convert_datetime_columns(orders):
    orders["order_date"] = pd.to_datetime(orders["order_date"], format="%Y-%m-%d")
    orders["order_time"] = pd.to_datetime(orders["order_time"], format="%H:%M:%S").dt.time
    orders["order_datetime"] = pd.to_datetime(
        orders["order_date"].astype(str) + " " + orders["order_time"].astype(str)
    )
    orders["order_hour"] = orders["order_datetime"].dt.hour
    orders["order_day_of_week"] = orders["order_datetime"].dt.day_name()
    orders["order_month"] = orders["order_datetime"].dt.month
    return orders


def create_delivery_duration(orders):
    orders["total_delivery_duration_min"] = (
        orders["preparation_time_min"].fillna(0) + orders["delivery_time_min"].fillna(0)
    )
    orders.loc[orders["order_status"] == "Cancelled", "total_delivery_duration_min"] = np.nan
    return orders


def add_delivery_delay_flag(orders, threshold_min=50):
    orders["delivery_delay_flag"] = (
        orders["total_delivery_duration_min"] > threshold_min
    ).astype(int)
    orders.loc[orders["order_status"] == "Cancelled", "delivery_delay_flag"] = np.nan
    return orders


def add_order_value_bucket(orders):
    bins = [0, 200, 500, 1000, float("inf")]
    labels = ["Budget", "Mid-Range", "Premium", "Luxury"]
    orders["order_value_bucket"] = pd.cut(
        orders["order_value"], bins=bins, labels=labels, right=True
    )
    return orders


def handle_missing_values(orders, customers, restaurants):
    orders["delivery_rating"] = orders["delivery_rating"].fillna(
        orders["delivery_rating"].median()
    )

    orders["preparation_time_min"] = orders["preparation_time_min"].fillna(0)
    orders["delivery_time_min"] = orders["delivery_time_min"].fillna(0)
    orders["delivery_distance_km"] = orders["delivery_distance_km"].fillna(0)

    customers["customer_name"] = customers["customer_name"].fillna("Unknown")
    customers["customer_city"] = customers["customer_city"].fillna("Unknown")

    restaurants["cuisine_type"] = restaurants["cuisine_type"].fillna("Other")
    restaurants["restaurant_rating"] = restaurants["restaurant_rating"].fillna(
        restaurants["restaurant_rating"].median()
    )

    return orders, customers, restaurants


def convert_customer_dates(customers):
    customers["signup_date"] = pd.to_datetime(customers["signup_date"], format="%Y-%m-%d")
    return customers


def add_customer_tenure_days(customers, reference_date="2024-12-31"):
    ref = pd.to_datetime(reference_date)
    customers["tenure_days"] = (ref - customers["signup_date"]).dt.days
    return customers


def add_discount_percentage(orders):
    orders["discount_pct"] = np.where(
        orders["order_value"] > 0,
        round((orders["discount"] / orders["order_value"]) * 100, 2),
        0
    )
    return orders


def save_processed(df, filename, output_dir="data/processed"):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    df.to_csv(path, index=False)
    print(f"[Transform] Saved {filename}: {df.shape[0]} rows → {path}")


def transform_all(orders, customers, restaurants):
    print("[Transform] Starting transformations...")

    orders, customers, restaurants = handle_missing_values(orders, customers, restaurants)
    print("[Transform] Missing values handled")

    orders = convert_datetime_columns(orders)
    print("[Transform] Datetime columns created")

    orders = create_delivery_duration(orders)
    print("[Transform] Delivery duration computed")

    orders = add_delivery_delay_flag(orders)
    print("[Transform] Delivery delay flags added")

    orders = add_order_value_bucket(orders)
    print("[Transform] Order value buckets assigned")

    orders = add_discount_percentage(orders)
    print("[Transform] Discount percentages calculated")

    customers = convert_customer_dates(customers)
    customers = add_customer_tenure_days(customers)
    print("[Transform] Customer tenure computed")

    save_processed(orders, "orders_transformed.csv")
    save_processed(customers, "customers_transformed.csv")
    save_processed(restaurants, "restaurants_transformed.csv")

    print(f"[Transform] All transformations complete")
    return orders, customers, restaurants


if __name__ == "__main__":
    from ingest import ingest_all
    orders, customers, restaurants = ingest_all()
    orders, customers, restaurants = transform_all(orders, customers, restaurants)
    print(f"\nTransformed orders columns: {list(orders.columns)}")
    print(f"\nSample:\n{orders.head(3).to_string()}")
