import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os


OUTPUT_DIR = "data/visualizations"


def setup_style():
    plt.rcParams.update({
        "figure.facecolor": "#1a1a2e",
        "axes.facecolor": "#16213e",
        "axes.edgecolor": "#e94560",
        "axes.labelcolor": "#ffffff",
        "text.color": "#ffffff",
        "xtick.color": "#cccccc",
        "ytick.color": "#cccccc",
        "grid.color": "#2a2a4a",
        "grid.alpha": 0.5,
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
    })


def save_fig(fig, name):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"[Viz] Saved: {path}")


def plot_revenue_by_city(conn):
    query = """
        SELECT r.restaurant_city AS city,
               ROUND(SUM(o.total_amount), 2) AS total_revenue
        FROM fact_orders o
        JOIN dim_restaurants r ON o.restaurant_id = r.restaurant_id
        WHERE o.order_status = 'Delivered'
        GROUP BY r.restaurant_city
        ORDER BY total_revenue DESC
    """
    df = pd.read_sql_query(query, conn)

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.magma([i / len(df) for i in range(len(df))])
    bars = ax.barh(df["city"], df["total_revenue"], color=colors, edgecolor="#e94560", linewidth=0.5)
    ax.set_xlabel("Total Revenue (₹)")
    ax.set_title("💰 Revenue by City")
    ax.invert_yaxis()
    ax.grid(axis="x", linestyle="--")

    for bar, val in zip(bars, df["total_revenue"]):
        ax.text(val + 1000, bar.get_y() + bar.get_height() / 2,
                f"₹{val:,.0f}", va="center", fontsize=9, color="#e94560")

    save_fig(fig, "revenue_by_city")


def plot_peak_hours(conn):
    query = """
        SELECT o.order_hour, COUNT(o.order_id) AS order_count
        FROM fact_orders o
        WHERE o.order_status = 'Delivered'
        GROUP BY o.order_hour
        ORDER BY o.order_hour
    """
    df = pd.read_sql_query(query, conn)

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#e94560" if v > df["order_count"].quantile(0.75) else "#533483" for v in df["order_count"]]
    ax.bar(df["order_hour"], df["order_count"], color=colors, edgecolor="#0f3460", linewidth=0.5)
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Number of Orders")
    ax.set_title("⏰ Peak Order Hours")
    ax.set_xticks(range(0, 24))
    ax.grid(axis="y", linestyle="--")

    save_fig(fig, "peak_order_hours")


def plot_order_status_distribution(conn):
    query = """
        SELECT order_status, COUNT(*) AS count
        FROM fact_orders
        GROUP BY order_status
    """
    df = pd.read_sql_query(query, conn)

    fig, ax = plt.subplots(figsize=(8, 8))
    colors = ["#0f3460", "#e94560", "#533483"]
    explode = [0.05] * len(df)
    wedges, texts, autotexts = ax.pie(
        df["count"], labels=df["order_status"], autopct="%1.1f%%",
        colors=colors[:len(df)], explode=explode,
        textprops={"color": "white", "fontsize": 12},
        wedgeprops={"edgecolor": "#1a1a2e", "linewidth": 2}
    )
    ax.set_title("📦 Order Status Distribution")

    save_fig(fig, "order_status_distribution")


def plot_cuisine_performance(conn):
    query = """
        SELECT r.cuisine_type,
               COUNT(o.order_id) AS order_count,
               ROUND(AVG(o.delivery_rating), 2) AS avg_rating
        FROM fact_orders o
        JOIN dim_restaurants r ON o.restaurant_id = r.restaurant_id
        WHERE o.order_status = 'Delivered'
        GROUP BY r.cuisine_type
        ORDER BY order_count DESC
        LIMIT 10
    """
    df = pd.read_sql_query(query, conn)

    fig, ax1 = plt.subplots(figsize=(14, 7))
    x = range(len(df))
    bars = ax1.bar(x, df["order_count"], color="#533483", alpha=0.8, label="Order Count", width=0.6)
    ax1.set_ylabel("Order Count", color="#533483")
    ax1.set_xlabel("Cuisine Type")
    ax1.set_title("🍕 Top 10 Cuisines: Orders vs Rating")

    ax2 = ax1.twinx()
    ax2.plot(x, df["avg_rating"], color="#e94560", marker="o", linewidth=2.5, markersize=8, label="Avg Rating")
    ax2.set_ylabel("Average Rating", color="#e94560")
    ax2.set_ylim(0, 5.5)

    ax1.set_xticks(x)
    ax1.set_xticklabels(df["cuisine_type"], rotation=45, ha="right")
    ax1.grid(axis="y", linestyle="--")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right",
               facecolor="#16213e", edgecolor="#e94560", labelcolor="white")

    save_fig(fig, "cuisine_performance")


def plot_delivery_delay_impact(conn):
    query = """
        SELECT delivery_delay_flag,
               ROUND(AVG(delivery_rating), 2) AS avg_rating,
               COUNT(*) AS order_count
        FROM fact_orders
        WHERE order_status = 'Delivered' AND delivery_delay_flag IS NOT NULL
        GROUP BY delivery_delay_flag
    """
    df = pd.read_sql_query(query, conn)
    df["label"] = df["delivery_delay_flag"].map({0: "On Time", 1: "Delayed"})

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    colors = ["#0f3460", "#e94560"]
    ax1.bar(df["label"], df["avg_rating"], color=colors, edgecolor="#1a1a2e", linewidth=2)
    ax1.set_ylabel("Average Rating")
    ax1.set_title("⭐ Rating: On Time vs Delayed")
    ax1.set_ylim(0, 5.5)
    ax1.grid(axis="y", linestyle="--")

    for i, (val, label) in enumerate(zip(df["avg_rating"], df["label"])):
        ax1.text(i, val + 0.1, f"{val:.2f}", ha="center", fontsize=13, fontweight="bold", color="#e94560")

    ax2.bar(df["label"], df["order_count"], color=colors, edgecolor="#1a1a2e", linewidth=2)
    ax2.set_ylabel("Order Count")
    ax2.set_title("📊 Volume: On Time vs Delayed")
    ax2.grid(axis="y", linestyle="--")

    for i, val in enumerate(df["order_count"]):
        ax2.text(i, val + 20, f"{val:,}", ha="center", fontsize=13, fontweight="bold", color="#e94560")

    fig.suptitle("🚚 Delivery Delay Impact Analysis", fontsize=16, y=1.02)
    save_fig(fig, "delivery_delay_impact")


def generate_all_visualizations(db_path="data/food_delivery.db"):
    print("\n[Viz] Generating visualizations...")
    setup_style()

    conn = sqlite3.connect(db_path)

    try:
        plot_revenue_by_city(conn)
        plot_peak_hours(conn)
        plot_order_status_distribution(conn)
        plot_cuisine_performance(conn)
        plot_delivery_delay_impact(conn)
        print(f"[Viz] All visualizations saved to {OUTPUT_DIR}/")
    finally:
        conn.close()


if __name__ == "__main__":
    generate_all_visualizations()
