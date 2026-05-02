# Food Delivery Data Pipeline 🍕📊

A production-style end-to-end **ETL (Extract, Transform, Load) data pipeline** built with Python, Pandas, and SQLite. This project ingests raw food delivery data, transforms it with business logic, loads it into a structured SQLite data warehouse, and generates analytical insights with visualizations.

---

## 🏗️ Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   📁 Raw     │────▶│  🔍 Ingest   │────▶│  🔄 Transform│────▶│  🗄️ Load     │────▶│  📊 Analyze  │
│   CSV Files  │     │  & Validate  │     │  & Enrich    │     │  to SQLite   │     │  & Visualize │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
    data/raw/          src/ingest.py       src/transform.py       src/load.py        src/analytics.py
                                                                 sql/schema.sql     src/visualize.py
```

**Pipeline Flow:** `Ingestion → Transformation → Loading → Analytics → Visualization`

---

## 📁 Project Structure

```
food-delivery-pipeline/
│── data/
│   ├── raw/                         # Raw CSV input files
│   │   ├── orders.csv               # 5,000 food delivery orders
│   │   ├── customers.csv            # 800 unique customers
│   │   └── restaurants.csv          # 120 restaurants across 10 cities
│   ├── processed/                   # Transformed CSV outputs
│   ├── visualizations/              # Generated charts (PNG)
│   └── food_delivery.db            # SQLite data warehouse
│── src/
│   ├── __init__.py
│   ├── ingest.py                    # Data ingestion & validation
│   ├── transform.py                 # Data cleaning & feature engineering
│   ├── load.py                      # SQLite table creation & data loading
│   ├── analytics.py                 # SQL query execution engine
│   ├── visualize.py                 # Chart generation (matplotlib)
│   └── pipeline.py                  # ETL orchestrator
│── sql/
│   ├── schema.sql                   # Star-schema DDL (fact + dimension tables)
│   └── queries.sql                  # 10 analytical SQL queries
│── generate_dataset.py              # Synthetic dataset generator
│── run.py                           # Entry point — runs full pipeline
│── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.10+** | Core programming language |
| **Pandas** | Data manipulation, cleaning, transformation |
| **SQLite** | Lightweight relational database (data warehouse) |
| **Matplotlib** | Data visualization and charting |

> SQLite is included in Python's standard library — no external database setup needed.

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/food-delivery-pipeline.git
cd food-delivery-pipeline
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate Dataset (Optional — already included)

```bash
python generate_dataset.py
```

### 5. Run the Pipeline

```bash
python run.py
```

This runs the complete ETL flow:
1. **Ingest** — Loads and validates raw CSVs
2. **Transform** — Cleans data, engineers features
3. **Load** — Creates SQLite tables, inserts data
4. **Analyze** — Runs 10 business queries
5. **Visualize** — Generates charts in `data/visualizations/`

---

## 📊 Database Schema (Star Schema)

```
                    ┌─────────────────┐
                    │  dim_customers  │
                    ├─────────────────┤
                    │ customer_id (PK)│
                    │ customer_name   │
                    │ customer_city   │
                    │ customer_rating │
                    │ signup_date     │
                    │ tenure_days     │
                    └────────┬────────┘
                             │
┌─────────────────┐   ┌──────┴──────────┐
│ dim_restaurants  │   │   fact_orders   │
├─────────────────┤   ├─────────────────┤
│restaurant_id(PK)├──▶│ order_id (PK)   │
│restaurant_name  │   │ customer_id(FK) │
│restaurant_city  │   │restaurant_id(FK)│
│cuisine_type     │   │ order_datetime  │
│restaurant_rating│   │ total_amount    │
│avg_delivery_min │   │ order_status    │
└─────────────────┘   │ delivery_time   │
                      │ delay_flag      │
                      │ value_bucket    │
                      │ ... (23 cols)   │
                      └─────────────────┘
```

---

## 📈 Analytics Queries

| # | Query | Insight |
|---|-------|---------|
| 1 | Average Delivery Time by City | Identify slowest/fastest cities |
| 2 | Revenue Per City | Top revenue-generating markets |
| 3 | Cancellation Rate by City | Markets with highest order cancellations |
| 4 | Top 10 Restaurants by Revenue | Best-performing restaurant partners |
| 5 | Peak Order Hours | Demand patterns across the day |
| 6 | Revenue by Payment Mode | Payment preference analysis |
| 7 | Order Value Bucket Distribution | Customer spending segmentation |
| 8 | Delivery Delay Analysis | Impact of delays on customer ratings |
| 9 | Day-of-Week Patterns | Weekly demand trends |
| 10 | Top Cuisines by Volume | Most popular cuisine categories |

---

## 📊 Sample Visualizations

Charts are auto-generated in `data/visualizations/`:

- `revenue_by_city.png` — Revenue distribution across cities
- `peak_order_hours.png` — Hourly order volume heatmap
- `order_status_distribution.png` — Delivered vs Cancelled vs Refunded
- `cuisine_performance.png` — Orders vs Rating by cuisine type
- `delivery_delay_impact.png` — How delays affect customer ratings

---

## 🔑 Key Features

- **Schema Validation** — Validates column names and types on ingestion
- **Referential Integrity** — Checks foreign key relationships between tables
- **Feature Engineering** — Delivery duration, delay flags, value buckets, discount %, customer tenure
- **Star Schema Design** — Fact and dimension tables with proper indexing
- **Idempotent Loads** — Pipeline can be re-run safely without duplicating data
- **Modular Architecture** — Each ETL stage is independently testable
- **Graceful Degradation** — Visualization stage is optional (works without matplotlib)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
