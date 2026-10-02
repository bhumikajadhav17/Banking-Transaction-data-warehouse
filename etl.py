import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("banking_dw.db")

print("Starting ETL process...")

# Extract
transactions = pd.read_sql_query(
    "SELECT * FROM fact_transaction",
    conn
)

print("Data extracted successfully.")

# Transform
transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"]
)

transactions["amount"] = transactions["amount"].astype(float)

transactions["month"] = transactions["transaction_date"].dt.month
transactions["year"] = transactions["transaction_date"].dt.year

print("Data transformed successfully.")

# Load
transactions.to_sql(
    "fact_transaction_clean",
    conn,
    if_exists="replace",
    index=False
)

print("Clean data loaded into warehouse.")

# Check result
result = pd.read_sql_query(
    "SELECT * FROM fact_transaction_clean",
    conn
)

print("\nCleaned Transaction Data:")
print(result)

conn.close()

print("\nETL process completed successfully!")