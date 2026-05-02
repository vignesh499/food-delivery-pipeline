DROP TABLE IF EXISTS fact_orders;
DROP TABLE IF EXISTS dim_customers;
DROP TABLE IF EXISTS dim_restaurants;

CREATE TABLE dim_customers (
    customer_id         TEXT PRIMARY KEY,
    customer_name       TEXT NOT NULL,
    customer_city       TEXT NOT NULL,
    customer_rating     REAL,
    signup_date         TEXT,
    tenure_days         INTEGER
);

CREATE TABLE dim_restaurants (
    restaurant_id           TEXT PRIMARY KEY,
    restaurant_name         TEXT NOT NULL,
    restaurant_city         TEXT NOT NULL,
    cuisine_type            TEXT,
    restaurant_rating       REAL,
    avg_delivery_time_min   INTEGER
);

CREATE TABLE fact_orders (
    order_id                    TEXT PRIMARY KEY,
    customer_id                 TEXT NOT NULL,
    restaurant_id               TEXT NOT NULL,
    order_date                  TEXT,
    order_time                  TEXT,
    order_datetime              TEXT,
    order_hour                  INTEGER,
    order_day_of_week           TEXT,
    order_month                 INTEGER,
    order_value                 REAL,
    discount                    REAL,
    discount_pct                REAL,
    delivery_fee                REAL,
    total_amount                REAL,
    payment_mode                TEXT,
    order_status                TEXT,
    preparation_time_min        REAL,
    delivery_time_min           REAL,
    total_delivery_duration_min REAL,
    delivery_delay_flag         INTEGER,
    delivery_rating             REAL,
    delivery_distance_km        REAL,
    order_value_bucket          TEXT,
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES dim_restaurants(restaurant_id)
);

CREATE INDEX idx_orders_customer ON fact_orders(customer_id);
CREATE INDEX idx_orders_restaurant ON fact_orders(restaurant_id);
CREATE INDEX idx_orders_date ON fact_orders(order_date);
CREATE INDEX idx_orders_status ON fact_orders(order_status);
CREATE INDEX idx_orders_city ON dim_customers(customer_city);
CREATE INDEX idx_restaurants_city ON dim_restaurants(restaurant_city);
