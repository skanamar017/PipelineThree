import pandas as pd
from datetime import datetime

# Read the data
df = pd.read_csv('sales_data.csv')

# Filter data
high_quantity = df[df['quantity'] > 5] # Filter sales with quantity greater than 5
print(f"Sales with quantity > 5: {len(high_quantity)}")

affordable_products = df[df['unit_price'] < 50] # Filter sales with unit price less than 50
print(f"Sales with unit price < $50: {len(affordable_products)}")

# Calculate revenue for each row
df['revenue'] = df['quantity'] * df['unit_price']

# Group by store and calculate total revenue
store_revenue = df.groupby('store_id')['revenue'].sum().reset_index() # Rename columns for clarity
print("\nTotal revenue by store:") #
print(store_revenue)

# Group by product and calculate average quantity
product_avg_quantity = df.groupby('product_id')['quantity'].mean().reset_index() # Rename columns for clarity
print("\nAverage quantity by product (first 5):")
print(product_avg_quantity)

# Extract day of week from date
df['date'] = pd.to_datetime(df['date']) # Convert date string to datetime
df['day_of_week'] = df['date'].dt.day_name() # Extract day of week

# Count sales by day of week
day_counts = df['day_of_week'].value_counts() # Rename index for clarity
print("\nSales by day of week:")
print(day_counts)

# Save filtered results to CSV
affordable_high_quantity = df[(df['quantity'] > 5) & (df['unit_price'] < 50)] # Filter for affordable products with high quantity
affordable_high_quantity.to_csv('filtered_sales.csv', index=False) # Save to CSV
print(f"\nSaved {len(affordable_high_quantity)} filtered records to 'filtered_sales.csv'") # End of file