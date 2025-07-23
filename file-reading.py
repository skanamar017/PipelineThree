import pandas as pd

# Read the data
df = pd.read_csv('sales_data.csv')

# Display first 5 rows
print("First 5 rows of sales_data:")
print(df.head()) 

# Calculate sum of quantities
print(f"Total quantity sold: {df['quantity'].sum()}")

# Calculate average unit price
print(f"Average unit price: ${df['unit_price'].mean():.2f}")

# Find min and max customer age
print(f"Customer age range: {df['customer_age'].min()} to {df['customer_age'].max()} years")

# Count sales by store
print("\nSales by store:")
print(df['store_id'].value_counts()) # Count of sales by store