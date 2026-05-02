import sqlite3
import pandas as pd
import os


DB_PATH = "data/food_delivery.db"
SCHEMA_PATH = "sql/schema.sql"


def get_connection(db_path=DB_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def create_tables(conn, schema_path=SCHEMA_PATH):
    with open(schema_path, "r") as f:
        schema_sql = f.read()

    conn.executescript(schema_sql)
    print(f"[Load] Tables created from {schema_path}")


def prepare_orders_for_load(orders):
    df = orders.copy()

    date_cols = ["order_date", "order_datetime"]
    for col in date_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)

    if "order_time" in df.columns:
        df["order_time"] = df["order_time"].astype(str)

    if "order_value_bucket" in df.columns:
        df["order_value_bucket"] = df["order_value_bucket"].astype(str)

    load_columns = [
        "order_id", "customer_id", "restaurant_id", "order_date", "order_time",
        "order_datetime", "order_hour", "order_day_of_week", "order_month",
        "order_value", "discount", "discount_pct", "delivery_fee", "total_amount",
        "payment_mode", "order_status", "preparation_time_min", "delivery_time_min",
        "total_delivery_duration_min", "delivery_delay_flag", "delivery_rating",
        "delivery_distance_km", "order_value_bucket"
    ]

    available = [c for c in load_columns if c in df.columns]
    return df[available]


def prepare_customers_for_load(customers):
    df = customers.copy()
    if "signup_date" in df.columns:
        df["signup_date"] = df["signup_date"].astype(str)

    load_columns = [
        "customer_id", "customer_name", "customer_city",
        "customer_rating", "signup_date", "tenure_days"
    ]
    available = [c for c in load_columns if c in df.columns]
    return df[available]


def prepare_restaurants_for_load(restaurants):
    load_columns = [
        "restaurant_id", "restaurant_name", "restaurant_city",
        "cuisine_type", "restaurant_rating", "avg_delivery_time_min"
    ]
    available = [c for c in load_columns if c in restaurants.columns]
    return restaurants[available]


def load_dataframe(conn, df, table_name):
    initial_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    final_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    new_rows = final_count - initial_count
    print(f"[Load] {table_name}: {final_count} rows loaded ({new_rows} new)")
    return final_count


def verify_load(conn):
    tables = ["dim_customers", "dim_restaurants", "fact_orders"]
    print("\n[Load] Verification:")
    for table in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")

    fk_check = conn.execute("PRAGMA foreign_key_check").fetchall()
    if fk_check:
        print(f"  ⚠️  Foreign key violations: {len(fk_check)}")
    else:
        print(f"  ✅ No foreign key violations")


def load_all(orders, customers, restaurants, db_path=DB_PATH):
    print(f"[Load] Connecting to {db_path}...")
    conn = get_connection(db_path)

    try:
        create_tables(conn)

        cust_df = prepare_customers_for_load(customers)
        load_dataframe(conn, cust_df, "dim_customers")

        rest_df = prepare_restaurants_for_load(restaurants)
        load_dataframe(conn, rest_df, "dim_restaurants")

        orders_df = prepare_orders_for_load(orders)
        load_dataframe(conn, orders_df, "fact_orders")

        verify_load(conn)
        conn.commit()
        print(f"[Load] All data committed to {db_path}")

    finally:
        conn.close()

    return db_path


if __name__ == "__main__":
    from ingest import ingest_all
    from transform import transform_all

    orders, customers, restaurants = ingest_all()
    orders, customers, restaurants = transform_all(orders, customers, restaurants)
    load_all(orders, customers, restaurants)
