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