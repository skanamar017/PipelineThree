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
df['month'] = df['date'].dt.month_name() # Extract month name for grouping

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
monthly_sales = df.groupby('month')['revenue'].sum().reset_index() # Rename columns for clarity
print("Monthly sales totals:")
print(monthly_sales)

# Find top 3 products by revenue
product_revenue = df.groupby('product_id')['revenue'].sum().reset_index() # Rename columns for clarity
top_products = product_revenue.sort_values('revenue', ascending=False).head(3) # Get top 3 products
print("\nTop 3 products by revenue:")
print(top_products)

# Process each store
for store_id in df['store_id'].unique(): # Iterate over each store
    # Filter data for this store
    store_data = df[df['store_id'] == store_id] # Filter for this store

    # Calculate metrics
    total_revenue = store_data['revenue'].sum() # Calculate total revenue
    avg_order_value = store_data['revenue'].mean() # Calculate average order value
    transaction_count = len(store_data) # Count transactions

    # Find most popular product
    product_counts = store_data['product_id'].value_counts()
    most_popular = product_counts.index[0]

    # Create summary
    summary = pd.DataFrame({ # Create summary DataFrame
        'Metric': ['Total Revenue', 'Average Order Value', 'Transaction Count', 'Most Popular Product'],
        'Value': [f"${total_revenue:.2f}", f"${avg_order_value:.2f}", transaction_count, most_popular]
    }) 

    # Save to file
    filename = f"store_reports/{store_id}_summary.csv" # Save summary to CSV
    summary.to_csv(filename, index=False) 
    print(f"Created summary for {store_id}")

# Create a bar chart of revenue by store
store_revenue = df.groupby('store_id')['revenue'].sum() # Reset index for clarity
plt.figure(figsize=(10, 6)) # Set figure size
store_revenue.plot(kind='bar') # Create bar chart
plt.title('Total Revenue by Store') # Set title
plt.xlabel('Store ID') # Set x-label
plt.ylabel('Revenue ($)') # Set y-label
plt.savefig('store_revenue.png') # Save the figure
plt.close() # End of plotting
print("Created bar chart: store_revenue.png") # Print confirmation