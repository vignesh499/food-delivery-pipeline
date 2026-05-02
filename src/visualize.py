import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os


DB_PATH = "data/food_delivery.db"
OUTPUT_DIR = "outputs"


def get_connection():
    return sqlite3.connect(DB_PATH)


def save_chart(fig, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(filepath, dpi=150, bbox_inches="tight", facecolor="#1e1e2e")
    plt.close(fig)
    print(f"[Viz] Saved: {filepath}")


def apply_dark_theme():
    plt.rcParams.update({
        "figure.facecolor": "#1e1e2e",
        "axes.facecolor": "#2b2b3d",
        "axes.edgecolor": "#444466",
        "axes.labelcolor": "#e0e0e0",
        "text.color": "#e0e0e0",
        "xtick.color": "#b0b0b0",
        "ytick.color": "#b0b0b0",
        "grid.color": "#3a3a5c",
        "grid.alpha": 0.4,
        "font.size": 11,
        "axes.titlesize": 15,
        "axes.labelsize": 12,
        "font.family": "sans-serif",
    })


def plot_revenue_by_city():
    conn = get_connection()
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
    conn.close()

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ["#6c5ce7", "#a29bfe", "#74b9ff", "#55efc4", "#ffeaa7",
              "#fab1a0", "#fd79a8", "#e17055", "#d63031", "#636e72"]

    bars = ax.barh(df["city"], df["total_revenue"], color=colors[:len(df)],
                   edgecolor="#1e1e2e", linewidth=1.5, height=0.6)
    ax.set_xlabel("Total Revenue (₹)")
    ax.set_title("Revenue by City", fontweight="bold", pad=15)
    ax.invert_yaxis()
    ax.grid(axis="x", linestyle="--")

    for bar, val in zip(bars, df["total_revenue"]):
        ax.text(val + 2000, bar.get_y() + bar.get_height() / 2,
                f"₹{val:,.0f}", va="center", fontsize=9, fontweight="bold",
                color="#ffeaa7")

    save_chart(fig, "revenue_by_city.png")


def plot_orders_by_hour():
    conn = get_connection()
    query = """
        SELECT o.order_hour AS hour,
               COUNT(o.order_id) AS total_orders
        FROM fact_orders o
        WHERE o.order_status = 'Delivered'
        GROUP BY o.order_hour
        ORDER BY o.order_hour
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df["hour"], df["total_orders"], color="#6c5ce7", linewidth=2.5,
            marker="o", markersize=7, markerfacecolor="#ffeaa7",
            markeredgecolor="#6c5ce7", markeredgewidth=1.5)

    ax.fill_between(df["hour"], df["total_orders"], alpha=0.15, color="#a29bfe")

    peak_hour = df.loc[df["total_orders"].idxmax()]
    ax.annotate(f"Peak: {int(peak_hour['hour'])}:00\n({int(peak_hour['total_orders'])} orders)",
                xy=(peak_hour["hour"], peak_hour["total_orders"]),
                xytext=(peak_hour["hour"] + 1.5, peak_hour["total_orders"] + 10),
                fontsize=10, fontweight="bold", color="#ffeaa7",
                arrowprops=dict(arrowstyle="->", color="#ffeaa7", lw=1.5))

    ax.set_xlabel("Hour of Day (24hr)")
    ax.set_ylabel("Number of Orders")
    ax.set_title("Orders by Hour of Day", fontweight="bold", pad=15)
    ax.set_xticks(range(0, 24))
    ax.set_xticklabels([f"{h}:00" for h in range(0, 24)], rotation=45, ha="right")
    ax.grid(axis="y", linestyle="--")

    save_chart(fig, "orders_by_hour.png")


def plot_cancellation_rate_by_city():
    conn = get_connection()
    query = """
        SELECT r.restaurant_city AS city,
               COUNT(o.order_id) AS total_orders,
               SUM(CASE WHEN o.order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
               ROUND(100.0 * SUM(CASE WHEN o.order_status = 'Cancelled' THEN 1 ELSE 0 END)
                     / COUNT(o.order_id), 2) AS cancellation_rate
        FROM fact_orders o
        JOIN dim_restaurants r ON o.restaurant_id = r.restaurant_id
        GROUP BY r.restaurant_city
        ORDER BY cancellation_rate DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = ["#d63031" if rate > 10 else "#e17055" if rate > 9 else "#55efc4"
              for rate in df["cancellation_rate"]]

    bars = ax.bar(df["city"], df["cancellation_rate"], color=colors,
                  edgecolor="#1e1e2e", linewidth=1.5, width=0.6)

    ax.axhline(y=df["cancellation_rate"].mean(), color="#ffeaa7",
               linestyle="--", linewidth=1.5, label=f"Avg: {df['cancellation_rate'].mean():.1f}%")

    for bar, rate in zip(bars, df["cancellation_rate"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                f"{rate}%", ha="center", fontsize=10, fontweight="bold",
                color="#ffeaa7")

    ax.set_xlabel("City")
    ax.set_ylabel("Cancellation Rate (%)")
    ax.set_title("Cancellation Rate by City", fontweight="bold", pad=15)
    ax.legend(facecolor="#2b2b3d", edgecolor="#444466", labelcolor="#e0e0e0")
    ax.grid(axis="y", linestyle="--")
    plt.xticks(rotation=45, ha="right")

    save_chart(fig, "cancellation_rate_by_city.png")


def generate_all_visualizations(db_path=None):
    if db_path:
        global DB_PATH
        DB_PATH = db_path

    print("\n[Viz] Generating visualizations...")
    apply_dark_theme()

    plot_revenue_by_city()
    plot_orders_by_hour()
    plot_cancellation_rate_by_city()

    print(f"[Viz] All 3 charts saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    generate_all_visualizations()
