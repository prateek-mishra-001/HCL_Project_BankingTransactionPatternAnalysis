# Project 10: Banking Transaction Pattern Analysis

**Industry:** Banking / FinTech  
**Language:** Python (only **NumPy** and **pandas** are used)  
**Dataset:** `10_bank_transactions.csv` (1,820 rows; 1,800 unique transactions + 20 duplicate rows)

> The dataset is **synthetic**. The `Flagged` column is a supplied label, **not proof of fraud**.

## Files

| File | Purpose |
|---|---|
| `generate_data.py` | Creates the synthetic CSV (run only if you need to regenerate it) |
| `10_bank_transactions.csv` | The dataset |
| `main.py` | Main program: analysis report + interactive filter/sort |
| `README.md` | This guide |
| `SRS.md` | Software Requirements Specification (for LMS upload) |

## How to run

```bash
pip install numpy pandas        # once
python generate_data.py         # optional, creates the CSV
python main.py                  # starts the program
```

## Menu

```
1. Full analysis report (Tasks 142 - 153)
2. Custom filter and sort
3. Show valid input values
4. Exit
```

On start, the program automatically runs Task 139 (inspect), Task 140 (missing amounts) and Task 141 (duplicates), then shows the menu.

## Task coverage

| Task | What it does | Where |
|---|---|---|
| 139 | Load and inspect records | `inspect_data()` |
| 140 | Find and fill missing amounts (group median by Account_Type + Transaction_Type) | `handle_missing()` |
| 141 | Check and remove duplicate Transaction_ID | `handle_duplicates()` |
| 142 | Total credits and debits | `credit_debit_totals()` |
| 143 | Mean, median, standard deviation | `amount_statistics()` |
| 144 | Volume by channel | `channel_summary()` |
| 145 | Total value by city | `city_summary()` |
| 146 | Flagged count and percentage | `flagged_summary()` |
| 147 | Flagged % by channel | `flagged_by_channel()` |
| 148 | 10 largest transactions | `top_ten()` |
| 149 | Credit/debit totals by account type (`groupby(['Account_Type','Transaction_Type'])`) | `account_type_totals()` |
| 150 | IQR outliers (`np.percentile`) | `iqr_outliers()` |
| 151 | Amount bands (`pd.cut`) | `amount_bands()` |
| 152 | NumPy Boolean indexing above a threshold | `numpy_threshold()` |
| 153 | Five cautious observations | `observations()` |

## Option 2: Custom filter and sort. What to enter

Every question can be **skipped by pressing Enter**. Filters are combined with **AND** (a record must satisfy all filters you give).

| # | Parameter | What to type | Example |
|---|---|---|---|
| 1 | City | One or more cities, comma separated | `Delhi` or `Delhi, Mumbai` |
| 2 | Channel | `ATM`, `UPI`, `Net Banking`, `Mobile App`, `Branch`, `POS` | `UPI, ATM` |
| 3 | Account type | `Savings`, `Current`, `Salary`, `Business` | `Business` |
| 4 | Transaction type | `Credit` or `Debit` | `Debit` |
| 5 | Flagged | `Yes` or `No` | `Yes` |
| 6 | Amount band | Exact band name (see below). If used, min/max are skipped | `High (10K-25K)` |
| 7 | Minimum amount | A number | `5000` |
| 8 | Maximum amount | A number | `25000` |
| 9 | Start date | `YYYY-MM-DD` | `2025-03-01` |
| 10 | End date | `YYYY-MM-DD` | `2025-09-30` |
| 11 | Sort by column | Any column name | `Amount` |
| 12 | Sort order | `A` ascending or `D` descending (default D) | `D` |
| 13 | Rows to display | A number or `all` (default 20) | `50` |
| 14 | Save to CSV? | `y` or `n`, then a file name | `y`, `my_result.csv` |

### Amount bands

| Band name | Range (Rs) |
|---|---|
| Very Low (<1K) | 0 to 999.99 |
| Low (1K-5K) | 1,000 to 4,999.99 |
| Medium (5K-10K) | 5,000 to 9,999.99 |
| High (10K-25K) | 10,000 to 24,999.99 |
| Very High (25K-50K) | 25,000 to 49,999.99 |
| Premium (50K+) | 50,000 and above |

### Ways a user can slice the data

- **Where:** City
- **How:** Channel
- **Who:** Account type
- **Direction:** Credit or Debit
- **Risk label:** Flagged Yes / No
- **How big:** Amount band, or min/max amount
- **When:** Date range
- **Order and size of the output:** sort column, order, number of rows

### Sample sessions

**1. Large flagged debits in Delhi**
City `Delhi` → Transaction type `Debit` → Flagged `Yes` → Minimum amount `25000` → Sort `Amount`, `D`.

**2. Low-value UPI activity in the first quarter**
Channel `UPI` → Amount band `Low (1K-5K)` → Start `2025-01-01` → End `2025-03-31` → Sort `Date`, `A`.

**3. Business account credits above 1 lakh, saved to a file**
Account type `Business` → Transaction type `Credit` → Minimum amount `100000` → Save `y`, name `business_credits.csv`.

Type `3` in the main menu any time to see all valid values and ranges.

## Constraints followed

- Only `numpy` and `pandas` are imported (no `os`, `sys`, `datetime`, matplotlib, etc.).
- Uses `if / elif / else`, `while` and `for` loops, functions, NumPy Boolean masks, and pandas `groupby`, `pivot_table`, `pd.cut`.
- Input is validated: bad values are rejected with a message and the question is asked again.

## Upload to GitHub (for LMS submission)

```bash
git init
git add main.py generate_data.py 10_bank_transactions.csv README.md SRS.md
git commit -m "Banking transaction pattern analysis"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

Then submit on the LMS: SRS document, `main.py`, and the GitHub repository link.

## Possible viva questions

1. Why was the group median used to fill missing amounts? *It is robust to extreme values and keeps similar account/transaction types comparable.*
2. Why is IQR used for outliers? *It does not assume a normal distribution; bounds are Q1 - 1.5 IQR and Q3 + 1.5 IQR.*
3. What is Boolean indexing? *A True/False NumPy array used as a mask to select elements: `amounts[amounts > 50000]`.*
4. Does a flagged transaction mean fraud? *No. It is only a supplied label in synthetic data.*
5. Why `ddof=1` in standard deviation? *It gives the sample standard deviation, matching pandas' default.*
