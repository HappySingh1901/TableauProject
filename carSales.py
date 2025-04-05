import random
import pandas as pd
from faker import Faker
import numpy as np
from datetime import datetime, timedelta

# Initialize Faker instance for random data generation
fake = Faker()

# Define the datasets
car_names = ["Tesla Model S", "Ford F-150", "Honda Civic", "Toyota Corolla", "Chevrolet Silverado", "BMW 3 Series", "Audi Q7", "Nissan Altima", "Hyundai Sonata", "Ford Mustang"]
fuel_types = ["Diesel", "Petrol", "EV"]
categories = {
    "Tesla Model S": "Sedan",
    "Ford F-150": "Pickup Truck",
    "Honda Civic": "Sedan",
    "Toyota Corolla": "Sedan",
    "Chevrolet Silverado": "Pickup Truck",
    "BMW 3 Series": "Sedan",
    "Audi Q7": "SUV",
    "Nissan Altima": "Sedan",
    "Hyundai Sonata": "Sedan",
    "Ford Mustang": "Coupe"
}
states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
regions = ["North", "South", "East", "West"]
price_range = [200000, 15000000]  # Min and max price for the cars (adjusted for more variance)
mileage_range = [100, 600]  # Adjusted to limit mileage to max 600 miles
quantity_range = [1, 25]  # Increased the range for quantity to allow larger variations
profit_margin_range = [0.05, 0.25]  # Wider profit margin range to allow more fluctuation
discount_range = [0, 0.25]  # Discount range adjusted to allow up to 25%

# Helper function to generate a random date within the last year
def random_date(start_date, end_date):
    return fake.date_between(start_date=start_date, end_date=end_date)

# Adjust sales for high-end vs budget cars (Increasing the price variance more)
def adjust_sales_for_car(car_name, sales):
    # Base sales multipliers based on popularity
    if car_name == "Ford F-150":
        # Ford F-150 is the highest-selling, no sales reduction, and price stays regular
        return int(sales * 1.5), 1.0  # Increase sales
    elif car_name == "Chevrolet Silverado":
        # Chevrolet Silverado has slightly reduced sales compared to other trucks
        return int(sales * 1.2), 0.9  # Slightly lower sales
    elif car_name == "Tesla Model S":
        # Tesla Model S is high-end but has lower sales
        return int(sales * 0.7), 1.1  # Lower sales but higher price
    elif car_name == "Honda Civic":
        return int(sales * 1.0), 1.0  # Normal sales
    elif car_name == "Toyota Corolla":
        return int(sales * 1.0), 1.0  # Normal sales
    elif car_name == "BMW 3 Series":
        return int(sales * 0.6), 1.5  # Lower sales, higher price
    elif car_name == "Audi Q7":
        return int(sales * 0.5), 1.6  # Low sales, premium price
    elif car_name == "Nissan Altima":
        return int(sales * 0.8), 1.0  # Lower sales
    elif car_name == "Hyundai Sonata":
        return int(sales * 0.8), 1.0  # Lower sales
    elif car_name == "Ford Mustang":
        return int(sales * 0.6), 1.2  # Lower sales, higher price
    else:
        return sales, 1.0  # Default case for any other cars

# Adjust sales during COVID (2020-2021), reducing by a factor of 0.5 during these years
def adjust_sales_for_covid(order_date, sales):
    if 2020 <= order_date.year <= 2021:
        return int(sales * 0.5)
    return sales

# Generate a list of rows
num_rows = 3000  # You can change this value to get 2000 to 5000 rows
data = []

for i in range(num_rows):
    row_id = i + 1
    car_name = random.choice(car_names)
    category = categories[car_name]  # Correct the category based on the car name
    mileage = random.randint(mileage_range[0], mileage_range[1])  # Mileage between 100 and 600
    price = random.randint(price_range[0], price_range[1])
    fuel_type = random.choice(fuel_types)
    quantity = random.randint(quantity_range[0], quantity_range[1])
    sales = price * quantity
    order_date = random_date(datetime(2018, 1, 1), datetime(2024, 11, 1))
    
    # Adjust sales based on car type and COVID period
    sales, price_multiplier = adjust_sales_for_car(car_name, sales)
    sales = adjust_sales_for_covid(order_date, sales)
    
    # Recalculate the price based on the car type and multiplier
    price = int(price * price_multiplier)
    
    # Calculate profit
    profit = sales * random.uniform(profit_margin_range[0], profit_margin_range[1])
    
    # Ship date should be after the order date
    ship_date = random_date(order_date, datetime(2024, 11, 30))
    
    # Other random values
    state = random.choice(states)
    region = random.choice(regions)
    discount = round(random.uniform(discount_range[0], discount_range[1]) * 100, 2)
    
    data.append({
        "row_id": row_id,
        "car_name": car_name,
        "mileage": mileage,
        "price": price,
        "type": fuel_type,
        "category": category,
        "quantity": quantity,
        "sales": sales,
        "order_date": order_date,
        "profit": round(profit, 2),
        "country": "USA",
        "ship_date": ship_date,
        "state": state,
        "region": region,
        "discount": discount
    })

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Save the dataset as a CSV file
df.to_csv("car_sales_final.csv", index=False)

print("Dataset created and saved as 'car_sales_final.csv'")
