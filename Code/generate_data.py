"""
generate_data.py
----------------
Creates the SYNTHETIC dataset  10_bank_transactions.csv
(1,800 unique transactions + 20 duplicate rows = 1,820 rows).

Only NumPy and pandas are used.
The data is artificial and must NOT be used for fraud claims.
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)          # fixed seed -> same file every time

N_UNIQUE = 1800
N_DUPLICATES = 20
N_ACCOUNTS = 400

cities = ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata",
          "Hyderabad", "Pune", "Jaipur", "Lucknow", "Ahmedabad"]
city_prob = [0.18, 0.17, 0.14, 0.10, 0.09, 0.09, 0.07, 0.06, 0.05, 0.05]

channels = ["ATM", "UPI", "Net Banking", "Mobile App", "Branch", "POS"]
channel_prob = [0.15, 0.30, 0.12, 0.20, 0.08, 0.15]
channel_median = {"ATM": 5000, "UPI": 1500, "Net Banking": 12000,
                  "Mobile App": 3000, "Branch": 25000, "POS": 1200}

account_types = ["Savings", "Current", "Salary", "Business"]
account_prob = [0.40, 0.20, 0.25, 0.15]
account_multiplier = {"Savings": 1.0, "Current": 2.0, "Salary": 1.5, "Business": 4.0}

# ---- account table (each account has a fixed type and home city) ----------
account_ids = np.array([f"ACC{1000 + i}" for i in range(N_ACCOUNTS)])
acc_type = rng.choice(account_types, size=N_ACCOUNTS, p=account_prob)
acc_city = rng.choice(cities, size=N_ACCOUNTS, p=city_prob)

# ---- transactions --------------------------------------------------------
acc_idx = rng.integers(0, N_ACCOUNTS, size=N_UNIQUE)
channel = rng.choice(channels, size=N_UNIQUE, p=channel_prob)
txn_type = rng.choice(["Credit", "Debit"], size=N_UNIQUE, p=[0.40, 0.60])

base = np.array([channel_median[c] for c in channel], dtype=float)
mult = np.array([account_multiplier[t] for t in acc_type[acc_idx]])
amount = rng.lognormal(mean=np.log(base * mult), sigma=0.9)

# ATM withdrawals cannot be huge
atm_debit = (channel == "ATM") & (txn_type == "Debit")
amount[atm_debit] = np.minimum(amount[atm_debit], 40000)

# a few extreme transactions so the IQR outlier task has something to find
extreme = rng.choice(N_UNIQUE, size=15, replace=False)
amount[extreme] = amount[extreme] * rng.uniform(6, 12, size=15)

amount = np.round(np.clip(amount, 50, 900000), 2)

# flagged label (a supplied label only - NOT proof of fraud)
p_flag = 0.02 + 0.12 * (amount > 50000) + 0.03 * np.isin(channel, ["Net Banking", "UPI"])
flagged = np.where(rng.random(N_UNIQUE) < p_flag, "Yes", "No")

dates = pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, size=N_UNIQUE), unit="D")

df = pd.DataFrame({
    "Transaction_ID": [f"TXN{100001 + i}" for i in range(N_UNIQUE)],
    "Date": dates.strftime("%Y-%m-%d"),
    "Account_ID": account_ids[acc_idx],
    "Account_Type": acc_type[acc_idx],
    "City": acc_city[acc_idx],
    "Channel": channel,
    "Transaction_Type": txn_type,
    "Amount": amount,
    "Flagged": flagged,
})

# ---- inject data-quality problems ---------------------------------------
# 1) about 3% missing amounts
missing_rows = rng.choice(N_UNIQUE, size=int(0.03 * N_UNIQUE), replace=False)
df.loc[missing_rows, "Amount"] = np.nan

# 2) exact duplicate rows (same Transaction_ID)
dup_rows = df.sample(n=N_DUPLICATES, random_state=7)
df = pd.concat([df, dup_rows], ignore_index=True)

# shuffle and save
df = df.sample(frac=1, random_state=11).reset_index(drop=True)
df.to_csv("10_bank_transactions.csv", index=False)

print("File created: 10_bank_transactions.csv")
print("Rows        :", len(df))
print("Missing amt :", int(df["Amount"].isna().sum()))
print("Dup IDs     :", int(df["Transaction_ID"].duplicated().sum()))
