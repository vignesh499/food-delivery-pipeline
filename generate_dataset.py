import pandas as pd
import random
import os
from datetime import datetime, timedelta

random.seed(42)

NUM_ORDERS = 5000
NUM_CUSTOMERS = 800
NUM_RESTAURANTS = 120

CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow"
]

RESTAURANT_NAMES = [
    "Spice Garden", "The Food Factory", "Curry House", "Biryani Blues",
    "Pizza Planet", "Dragon Wok", "Tandoori Nights", "Burger Barn",
    "Sushi Station", "Pasta Palace", "Dosa Corner", "Kebab King",
    "Wok & Roll", "Grill Master", "Chaat Street", "Momos Hub",
    "Royal Dhaba", "Green Leaf Cafe", "Ice Cream Dream", "Noodle Bar",
    "Samosa House", "Wrap It Up", "The Salad Bowl", "Paneer Paradise",
    "Chai Point", "Roti Republic", "Egg Factory", "South Spice",
    "North Indian Kitchen", "Coastal Flavors"
]

CUISINE_TYPES = [
    "North Indian", "South Indian", "Chinese", "Italian", "Mexican",
    "Continental", "Street Food", "Fast Food", "Mughlai", "Thai",
    "Japanese", "Korean", "Mediterranean", "Bengali", "Rajasthani"
]

ORDER_STATUSES = ["Delivered", "Delivered", "Delivered", "Delivered",
                  "Cancelled", "Delivered", "Delivered", "Refunded",
                  "Delivered", "Delivered"]

PAYMENT_MODES = ["Credit Card", "Debit Card", "UPI", "Cash on Delivery", "Wallet"]

CUSTOMER_NAMES = [
    "Aarav Sharma", "Priya Patel", "Rohan Kumar", "Sneha Gupta",
    "Vikram Singh", "Ananya Reddy", "Karan Mehta", "Divya Nair",
    "Arjun Das", "Meera Iyer", "Rahul Verma", "Pooja Joshi",
    "Aditya Rao", "Nisha Kapoor", "Siddharth Bhat", "Kavya Menon",
    "Nikhil Saxena", "Ritu Agarwal", "Manish Tiwari", "Simran Kaur"
]


def generate_customers():
    customers = []
    for i in range(1, NUM_CUSTOMERS + 1):
        customers.append({
            "customer_id": f"CUST_{i:04d}",
            "customer_name": random.choice(CUSTOMER_NAMES) + f" {random.randint(1, 99)}",
            "customer_city": random.choice(CITIES),
            "customer_rating": round(random.uniform(3.0, 5.0), 1),
            "signup_date": (datetime(2022, 1, 1) + timedelta(days=random.randint(0, 1000))).strftime("%Y-%m-%d")
        })
    return customers


def generate_restaurants():
    restaurants = []
    for i in range(1, NUM_RESTAURANTS + 1):
        city = random.choice(CITIES)
        restaurants.append({
            "restaurant_id": f"REST_{i:03d}",
            "restaurant_name": random.choice(RESTAURANT_NAMES) + f" - {city}",
            "restaurant_city": city,
            "cuisine_type": random.choice(CUISINE_TYPES),
            "restaurant_rating": round(random.uniform(2.5, 5.0), 1),
            "avg_delivery_time_min": random.randint(20, 55)
        })
    return restaurants


def generate_orders(customers, restaurants):
    orders = []
    base_date = datetime(2024, 1, 1)

    for i in range(1, NUM_ORDERS + 1):
        customer = random.choice(customers)
        restaurant = random.choice(restaurants)

        order_datetime = base_date + timedelta(
            days=random.randint(0, 364),
            hours=random.randint(8, 23),
            minutes=random.randint(0, 59)
        )

        order_value = round(random.uniform(99, 1500), 2)
        discount = round(order_value * random.choice([0, 0, 0.05, 0.1, 0.15, 0.2, 0]), 2)
        delivery_fee = random.choice([0, 20, 30, 40, 50])
        total_amount = round(order_value - discount + delivery_fee, 2)

        status = random.choice(ORDER_STATUSES)

        prep_time = random.randint(10, 40)
        delivery_time = random.randint(15, 60)

        if status == "Cancelled":
            prep_time = None
            delivery_time = None

        delivery_rating = None
        if status == "Delivered":
            delivery_rating = random.choice([1, 2, 3, 3, 4, 4, 4, 5, 5, 5, None])

        orders.append({
            "order_id": f"ORD_{i:05d}",
            "customer_id": customer["customer_id"],
            "restaurant_id": restaurant["restaurant_id"],
            "order_date": order_datetime.strftime("%Y-%m-%d"),
            "order_time": order_datetime.strftime("%H:%M:%S"),
            "order_value": order_value,
            "discount": discount,
            "delivery_fee": delivery_fee,
            "total_amount": total_amount,
            "payment_mode": random.choice(PAYMENT_MODES),
            "order_status": status,
            "preparation_time_min": prep_time,
            "delivery_time_min": delivery_time,
            "delivery_rating": delivery_rating,
            "delivery_distance_km": round(random.uniform(1.0, 15.0), 1) if status != "Cancelled" else None
        })

    return orders


def main():
    customers = generate_customers()
    restaurants = generate_restaurants()
    orders = generate_orders(customers, restaurants)

    os.makedirs("data/raw", exist_ok=True)

    df_orders = pd.DataFrame(orders)
    df_customers = pd.DataFrame(customers)
    df_restaurants = pd.DataFrame(restaurants)

    df_orders.to_csv("data/raw/orders.csv", index=False)
    df_customers.to_csv("data/raw/customers.csv", index=False)
    df_restaurants.to_csv("data/raw/restaurants.csv", index=False)

    print(f"Generated {len(df_orders)} orders")
    print(f"Generated {len(df_customers)} customers")
    print(f"Generated {len(df_restaurants)} restaurants")
    print(f"Files saved to data/raw/")


if __name__ == "__main__":
    main()
