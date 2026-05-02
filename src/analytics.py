import sqlite3
import pandas as pd
import os


QUERY_LABELS = [
    "Average Delivery Time by City",
    "Revenue Per City",
    "Cancellation Rate by City",
    "Top 10 Restaurants by Revenue",
    "Peak Order Hours",
    "Revenue by Payment Mode",
    "Order Value Bucket Distribution",
    "Delivery Delay Analysis",
    "Day-of-Week Order Patterns",
    "Top Cuisines by Order Volume",
]


def parse_queries(sql_path="sql/queries.sql"):
    with open(sql_path, "r") as f:
        content = f.read()

    raw_blocks = content.split("-- ====")
    queries = []

    for block in raw_blocks:
        lines = block.strip().split("\n")
        sql_lines = [
            line for line in lines
            if line.strip() and not line.strip().startswith("--") and not line.strip().startswith("====")
        ]
        if sql_lines:
            queries.append("\n".join(sql_lines))

    return queries


def run_analytics(db_path="data/food_delivery.db", sql_path="sql/queries.sql"):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found: {db_path}")

    conn = sqlite3.connect(db_path)
    queries = parse_queries(sql_path)

    results = {}

    for i, query in enumerate(queries):
        label = QUERY_LABELS[i] if i < len(QUERY_LABELS) else f"Query {i + 1}"
        try:
            df = pd.read_sql_query(query, conn)
            results[label] = df

            print(f"\n{'=' * 60}")
            print(f"  📊 {label}")
            print(f"{'=' * 60}")
            print(df.to_string(index=False))

        except Exception as e:
            print(f"\n❌ Error in '{label}': {e}")

    conn.close()

    print(f"\n[Analytics] {len(results)} queries executed successfully")
    return results


if __name__ == "__main__":
    run_analytics()
