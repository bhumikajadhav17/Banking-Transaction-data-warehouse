import sqlite3
import pandas as pd

# 1. Database connection
conn = sqlite3.connect("banking_dw.db")

# 2. Customer data
customers = pd.DataFrame({
    "customer_id": [101, 102, 103, 104, 105],
    "customer_name": ["Aarav", "Priya", "Rohan", "Sneha", "Aditya"],
    "city": ["Mumbai", "Pune", "Mumbai", "Nashik", "Thane"]
})

# 3. Account data
accounts = pd.DataFrame({
    "account_id": [501, 502, 503, 504, 505],
    "customer_id": [101, 102, 103, 104, 105],
    "account_type": ["Savings", "Savings", "Current", "Savings", "Current"]
})

# 4. Branch data
branches = pd.DataFrame({
    "branch_id": [1, 2, 3, 4],
    "branch_name": [
        "Mumbai Central", "Pune Camp",
        "Andheri", "Nashik Main"
    ],
    "city": ["Mumbai", "Pune", "Mumbai", "Nashik"]
})

# 5. Transaction data
transactions = pd.DataFrame({
    "transaction_id": [
        "T001", "T002", "T003", "T004",
        "T005", "T006", "T007", "T008"
    ],
    "customer_id": [101, 102, 101, 103, 104, 105, 102, 103],
    "account_id": [501, 502, 501, 503, 504, 505, 502, 503],
    "branch_id": [1, 2, 1, 3, 4, 2, 2, 3],
    "transaction_date": [
        "2026-09-01", "2026-09-02",
        "2026-09-05", "2026-09-07",
        "2026-09-10", "2026-09-12",
        "2026-09-15", "2026-09-18"
    ],
    "transaction_type": [
        "Deposit", "Withdrawal", "Transfer", "Deposit",
        "Withdrawal", "Deposit", "Transfer", "Withdrawal"
    ],
    "amount": [25000, 8000, 12000, 35000, 5000, 45000, 15000, 7000]
})

# 6. Load data into database
customers.to_sql("dim_customer", conn, if_exists="replace", index=False)
accounts.to_sql("dim_account", conn, if_exists="replace", index=False)
branches.to_sql("dim_branch", conn, if_exists="replace", index=False)
transactions.to_sql("fact_transaction", conn, if_exists="replace", index=False)

print("Data loaded successfully!")

# 7. SQL Analysis

# Analysis 1: Total transactions
print("\n1. Total Transaction Amount")
query = """
SELECT SUM(amount) AS total_amount
FROM fact_transaction
"""
print(pd.read_sql_query(query, conn))

# Analysis 2: Total deposits
print("\n2. Total Deposits")
query = """
SELECT SUM(amount) AS total_deposit
FROM fact_transaction
WHERE transaction_type = 'Deposit'
"""
print(pd.read_sql_query(query, conn))

# Analysis 3: Total withdrawals
print("\n3. Total Withdrawals")
query = """
SELECT SUM(amount) AS total_withdrawal
FROM fact_transaction
WHERE transaction_type = 'Withdrawal'
"""
print(pd.read_sql_query(query, conn))

# Analysis 4: Transaction type summary
print("\n4. Transaction Type Analysis")
query = """
SELECT transaction_type,
       COUNT(*) AS number_of_transactions,
       SUM(amount) AS total_amount
FROM fact_transaction
GROUP BY transaction_type
"""
print(pd.read_sql_query(query, conn))

# Analysis 5: Customer-wise transactions
print("\n5. Customer-wise Analysis")
query = """
SELECT c.customer_name,
       COUNT(f.transaction_id) AS total_transactions,
       SUM(f.amount) AS total_amount
FROM fact_transaction f
JOIN dim_customer c
ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_amount DESC
"""
print(pd.read_sql_query(query, conn))

# Analysis 6: Branch-wise transactions
print("\n6. Branch-wise Analysis")
query = """
SELECT b.branch_name,
       COUNT(f.transaction_id) AS total_transactions,
       SUM(f.amount) AS total_amount
FROM fact_transaction f
JOIN dim_branch b
ON f.branch_id = b.branch_id
GROUP BY b.branch_id, b.branch_name
ORDER BY total_amount DESC
"""
print(pd.read_sql_query(query, conn))

# Analysis 7: Monthly transactions
print("\n7. Monthly Transaction Analysis")
query = """
SELECT strftime('%Y-%m', transaction_date) AS month,
       COUNT(*) AS total_transactions,
       SUM(amount) AS total_amount
FROM fact_transaction
GROUP BY month
ORDER BY month
"""
print(pd.read_sql_query(query, conn))

# Analysis 8: Account type analysis
print("\n8. Account Type Analysis")
query = """
SELECT a.account_type,
       COUNT(f.transaction_id) AS total_transactions,
       SUM(f.amount) AS total_amount
FROM fact_transaction f
JOIN dim_account a
ON f.account_id = a.account_id
GROUP BY a.account_type
"""
print(pd.read_sql_query(query, conn))

# 8. Save analysis output
summary = pd.read_sql_query("""
SELECT transaction_type,
       COUNT(*) AS total_transactions,
       SUM(amount) AS total_amount
FROM fact_transaction
GROUP BY transaction_type
""", conn)

summary.to_csv("transaction_summary.csv", index=False)

print("\nSummary saved successfully!")

# 9. Close connection
conn.close()
print("\nProject completed successfully!")