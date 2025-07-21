# Data Engineering Exercises - Simplified

**don't try this lab until you have been briefed on using pandas**

## Exercise 1: Basic File Reading and Simple Statistics

**Objective:** Read a tabular data file and calculate basic statistics on numerical columns.

**Dataset:** `sales_data.csv` (500 lines) with the following columns:
- `date` (string): Transaction date in YYYY-MM-DD format
- `store_id` (string): Store identifier (e.g., "S001", "S002")
- `product_id` (string): Product identifier (e.g., "P123", "P456")
- `quantity` (integer): Number of items sold
- `unit_price` (float): Price per item in dollars
- `customer_age` (integer): Age of the customer

**Tasks:**
1. Read the CSV file using pandas
2. Display the first 5 rows of the dataset
3. Calculate the sum of all quantities sold
4. Calculate the average unit price
5. Find the minimum and maximum customer age
6. Count how many sales were made at each store

**Example starter code:**
```python
import pandas as pd

# Read the data
df = pd.read_csv('sales_data.csv')

# Display first 5 rows
print("First 5 rows:")
print(df.head())

# Calculate sum of quantities
total_quantity = df['quantity'].sum()
print(f"Total quantity sold: {total_quantity}")

# Calculate average unit price
avg_price = df['unit_price'].mean()
print(f"Average unit price: ${avg_price:.2f}")

# Find min and max customer age
min_age = df['customer_age'].min()
max_age = df['customer_age'].max()
print(f"Customer age range: {min_age} to {max_age} years")

# Count sales by store
store_counts = df['store_id'].value_counts()
print("\nSales by store:")
print(store_counts)
```

## Exercise 2: Data Filtering and Grouping

**Objective:** Read a data file, filter records, and perform group-by operations with simple aggregations.

**Dataset:** Same `sales_data.csv` from Exercise 1

**Tasks:**
1. Read the CSV file using pandas
2. Filter the data to show only:
   - Sales with quantities greater than 5
   - Products with a unit price less than $50
3. Calculate the total revenue for each store (quantity × unit price)
4. Find the average quantity sold for each product
5. Determine which day of the week had the most sales
6. Save the filtered results to a new CSV file

**Example starter code:**
```python
import pandas as pd
from datetime import datetime

# Read the data
df = pd.read_csv('sales_data.csv')

# Filter data
high_quantity = df[df['quantity'] > 5]
print(f"Sales with quantity > 5: {len(high_quantity)}")

affordable_products = df[df['unit_price'] < 50]
print(f"Sales with unit price < $50: {len(affordable_products)}")

# Calculate revenue for each row
df['revenue'] = df['quantity'] * df['unit_price']

# Group by store and calculate total revenue
store_revenue = df.groupby('store_id')['revenue'].sum().reset_index()
print("\nTotal revenue by store:")
print(store_revenue)

# Group by product and calculate average quantity
product_avg_quantity = df.groupby('product_id')['quantity'].mean().reset_index()
print("\nAverage quantity by product (first 5):")
print(product_avg_quantity.head())

# Extract day of week from date
df['date'] = pd.to_datetime(df['date'])
df['day_of_week'] = df['date'].dt.day_name()

# Count sales by day of week
day_counts = df['day_of_week'].value_counts()
print("\nSales by day of week:")
print(day_counts)

# Save filtered results to CSV
affordable_high_quantity = df[(df['quantity'] > 5) & (df['unit_price'] < 50)]
affordable_high_quantity.to_csv('filtered_sales.csv', index=False)
print(f"\nSaved {len(affordable_high_quantity)} filtered records to 'filtered_sales.csv'")
```

## Exercise 3: Data Transformation and Multiple Files

**Objective:** Process a data file, perform transformations, and output results to multiple files.

**Dataset:** Same `sales_data.csv` from previous exercises

**Tasks:**
1. Read the CSV file using pandas
2. Create new derived columns:
   - Total revenue (quantity × unit price)
   - Month (extracted from date)
   - Age category (Young: <30, Adult: 30-50, Senior: >50)
3. Calculate monthly sales totals
4. Find the top 3 products by total revenue
5. Create a separate summary file for each store with:
   - Total revenue
   - Average order value
   - Number of transactions
   - Most popular product
6. Create a simple bar chart of revenue by store

**Example starter code:**
```python
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output directory if it doesn't exist
os.makedirs('store_reports', exist_ok=True)

# Read the data
df = pd.read_csv('sales_data.csv')

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Create derived columns
df['revenue'] = df['quantity'] * df['unit_price']
df['month'] = df['date'].dt.month_name()

# Create age category
def categorize_age(age):
    if age < 30:
        return 'Young'
    elif age <= 50:
        return 'Adult'
    else:
        return 'Senior'

df['age_category'] = df['customer_age'].apply(categorize_age)

# Calculate monthly sales
monthly_sales = df.groupby('month')['revenue'].sum().reset_index()
print("Monthly sales totals:")
print(monthly_sales)

# Find top 3 products by revenue
product_revenue = df.groupby('product_id')['revenue'].sum().reset_index()
top_products = product_revenue.sort_values('revenue', ascending=False).head(3)
print("\nTop 3 products by revenue:")
print(top_products)

# Process each store
for store_id in df['store_id'].unique():
    # Filter data for this store
    store_data = df[df['store_id'] == store_id]

    # Calculate metrics
    total_revenue = store_data['revenue'].sum()
    avg_order_value = store_data['revenue'].mean()
    transaction_count = len(store_data)

    # Find most popular product
    product_counts = store_data['product_id'].value_counts()
    most_popular = product_counts.index[0]

    # Create summary
    summary = pd.DataFrame({
        'Metric': ['Total Revenue', 'Average Order Value', 'Transaction Count', 'Most Popular Product'],
        'Value': [f"${total_revenue:.2f}", f"${avg_order_value:.2f}", transaction_count, most_popular]
    })

    # Save to file
    filename = f"store_reports/{store_id}_summary.csv"
    summary.to_csv(filename, index=False)
    print(f"Created summary for {store_id}")

# Create a bar chart of revenue by store
store_revenue = df.groupby('store_id')['revenue'].sum()
plt.figure(figsize=(10, 6))
store_revenue.plot(kind='bar')
plt.title('Total Revenue by Store')
plt.xlabel('Store ID')
plt.ylabel('Revenue ($)')
plt.savefig('store_revenue.png')
plt.close()
print("Created bar chart: store_revenue.png")
```

## Sample Data Generation

Here's a simplified Python script to generate the sample dataset for these exercises:

```python
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Generate 500 records
n_records = 500

# Create date range for the past 30 days
end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days)]

# Generate data
data = {
    'date': [random.choice(date_range).strftime('%Y-%m-%d') for _ in range(n_records)],
    'store_id': [f"S{random.randint(1, 5):03d}" for _ in range(n_records)],
    'product_id': [f"P{random.randint(1, 20):03d}" for _ in range(n_records)],
    'quantity': np.random.randint(1, 15, n_records),
    'unit_price': np.round(np.random.uniform(10, 100, n_records), 2),
    'customer_age': np.random.randint(18, 70, n_records)
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('sales_data.csv', index=False)

print(f"Created sales_data.csv with {n_records} records")
```

This simplified data generation script will create a dataset
that students can use for all three exercises, focusing on basic data engineering concepts.
