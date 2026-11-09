import sys
from pathlib import Path

import pandas as pd

# Allow Python to locate modules inside src
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from load_data import load_data


# Create one synthetic cart
carts_df = pd.DataFrame([
    {
        "cart_id": 999999,
        "user_id": 999999,
        "total": 600.00,
        "discounted_total": 540.00,
        "total_products": 1,
        "total_quantity": 2
    }
])


# Create one synthetic product
products_df = pd.DataFrame([
    {
        "cart_id": 999999,
        "product_id": 999999,
        "title": "Incremental Loading Test Product",
        "price": 300.00,
        "quantity": 2,
        "total": 600.00,
        "discount_percentage": 10.00,
        "discounted_total": 540.00
    }
])


# Load synthetic data into MySQL
print("Running incremental loading test...")

load_data(carts_df, products_df)

print("Test execution completed.")