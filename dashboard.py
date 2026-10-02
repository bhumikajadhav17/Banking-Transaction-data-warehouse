import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect database
conn = sqlite3.connect("banking_dw.db")

# -----------------------------
# 1. Transaction Type Analysis
# -----------------------------

query = """
SELECT transaction_type,
       COUNT(*) AS total_transactions,
       SUM(amount) AS total_amount
FROM fact_transaction
GROUP BY transaction_type
"""

df = pd.read_sql_query(query, conn)

plt.figure(figsize=(8, 5))

plt.bar(df["transaction_type"], df["total_amount"])

plt.title("Transaction Amount by Type")
plt.xlabel("Transaction Type")
plt.ylabel("Amount")

plt.tight_layout()
plt.savefig("transaction_type.png")
plt.show()


# -----------------------------
# 2. Branch-wise Analysis
# -----------------------------

query = """
SELECT b.branch_name,
       SUM(f.amount) AS total_amount
FROM fact_transaction f
JOIN dim_branch b
ON f.branch_id = b.branch_id
GROUP BY b.branch_name
"""

branch_df = pd.read_sql_query(query, conn)

plt.figure(figsize=(9, 5))

plt.bar(branch_df["branch_name"], branch_df["total_amount"])

plt.title("Branch-wise Transaction Amount")
plt.xlabel("Branch")
plt.ylabel("Amount")

plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig("branch_analysis.png")
plt.show()


# -----------------------------
# 3. Customer-wise Analysis
# -----------------------------

query = """
SELECT c.customer_name,
       SUM(f.amount) AS total_amount
FROM fact_transaction f
JOIN dim_customer c
ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_amount DESC
"""

customer_df = pd.read_sql_query(query, conn)

plt.figure(figsize=(8, 5))

plt.bar(customer_df["customer_name"],
         customer_df["total_amount"])

plt.title("Customer-wise Transaction Amount")
plt.xlabel("Customer")
plt.ylabel("Amount")

plt.tight_layout()

plt.savefig("customer_analysis.png")
plt.show()


conn.close()

print("Dashboard charts created successfully!")