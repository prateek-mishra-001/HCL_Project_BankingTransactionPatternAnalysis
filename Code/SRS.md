# Software Requirements Specification (SRS)

## Project 10: Banking Transaction Pattern Analysis

| Field | Detail |
|---|---|
| Industry | Banking / FinTech |
| Language | Python 3 |
| Libraries | NumPy, pandas (no others) |
| Dataset | `10_bank_transactions.csv` (synthetic) |
| Student name / ID | _(fill in)_ |
| Date | _(fill in)_ |

---

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements of a command-line Python program that explores bank transaction records and summarises transaction behaviour by amount, channel, city, account type, transaction type and flagged label.

### 1.2 Scope
The program loads a CSV file, cleans it, produces a standard analysis report, and lets the user filter and sort records by parameters they choose. It does not detect fraud. The dataset is synthetic and the `Flagged` column is a supplied label only.

### 1.3 Definitions

| Term | Meaning |
|---|---|
| Credit | Money coming into an account |
| Debit | Money going out of an account |
| Channel | Medium used: ATM, UPI, Net Banking, Mobile App, Branch, POS |
| Flagged | Supplied Yes/No label; not proof of fraud |
| IQR | Interquartile range, Q3 - Q1 |
| Outlier | Value below Q1 - 1.5 IQR or above Q3 + 1.5 IQR |

---

## 2. Overall Description

### 2.1 Product perspective
A standalone console program made of two scripts: `generate_data.py` (creates data) and `main.py` (analysis and interaction).

### 2.2 Users
Students, bank analysts or operations staff who need quick summaries of transaction behaviour without writing code.

### 2.3 Operating environment
Any OS with Python 3.9+ and NumPy and pandas installed.

### 2.4 Constraints
- Only NumPy and pandas may be used.
- Must use if/else, loops, pandas and NumPy.
- Results must not be presented as fraud claims.

### 2.5 Assumptions
- `10_bank_transactions.csv` is in the same folder as `main.py`.
- Amounts are in Indian Rupees.

---

## 3. Data Description

### 3.1 Data dictionary

| Column | Type | Description |
|---|---|---|
| Transaction_ID | text | Unique ID such as TXN100001 (duplicates deliberately injected) |
| Date | date | Transaction date, 2025-01-01 to 2025-12-31 |
| Account_ID | text | Account number such as ACC1001 |
| Account_Type | text | Savings, Current, Salary, Business |
| City | text | 10 cities: Delhi, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad, Pune, Jaipur, Lucknow, Ahmedabad |
| Channel | text | ATM, UPI, Net Banking, Mobile App, Branch, POS |
| Transaction_Type | text | Credit or Debit |
| Amount | number | Transaction amount in Rs; about 3% missing |
| Flagged | text | Yes or No |

### 3.2 Dataset size and quality issues
1,820 rows: 1,800 unique transactions plus 20 duplicate rows; 55 missing Amount values; 15 deliberately extreme amounts.

---

## 4. Functional Requirements

| ID | Requirement | Task |
|---|---|---|
| FR-1 | Load the CSV and show shape, first rows, data types, missing counts and summary statistics | 139 |
| FR-2 | Detect missing amounts and fill them with the median of the same Account_Type + Transaction_Type group | 140 |
| FR-3 | Detect duplicate Transaction_ID values, display examples and remove repeats keeping the first | 141 |
| FR-4 | Calculate total credits, total debits and net flow | 142 |
| FR-5 | Calculate mean, median and standard deviation of Amount | 143 |
| FR-6 | Compare count, total value, average and share by channel | 144 |
| FR-7 | Compare total value by city | 145 |
| FR-8 | Calculate flagged count and percentage | 146 |
| FR-9 | Compare flagged percentage across channels | 147 |
| FR-10 | List the 10 largest transactions | 148 |
| FR-11 | Group credit and debit totals by account type using `groupby(['Account_Type','Transaction_Type'])` | 149 |
| FR-12 | Identify outliers using IQR with `np.percentile` | 150 |
| FR-13 | Create amount bands with `pd.cut` and summarise each | 151 |
| FR-14 | Isolate transactions above a user-chosen threshold using a NumPy Boolean mask | 152 |
| FR-15 | Generate five cautious observations and recommendations from the data | 153 |
| FR-16 | Provide a menu with: full report, custom filter and sort, valid-values help, exit | Extra |
| FR-17 | Custom filter by city, channel, account type, transaction type, flagged, amount band or min/max amount, and date range (all optional, combined with AND) | Extra |
| FR-18 | Sort results by any column, ascending or descending, and limit rows displayed | Extra |
| FR-19 | Show summary of filtered result (count, total, average, flagged, credits/debits) | Extra |
| FR-20 | Optionally save the filtered result to a CSV file | Extra |

---

## 5. User Input Specification

| Parameter | Valid input | Skip |
|---|---|---|
| City | One or more listed cities, comma separated | Enter |
| Channel | One or more listed channels | Enter |
| Account type | One or more listed types | Enter |
| Transaction type | Credit and/or Debit | Enter |
| Flagged | Yes and/or No | Enter |
| Amount band | One of six band names | Enter (then min/max asked) |
| Min / Max amount | Number; min must not exceed max | Enter |
| Start / End date | `YYYY-MM-DD`; start must not be after end | Enter |
| Sort column | One of the nine column names | Enter |
| Sort order | A or D | Enter (D) |
| Rows | Positive integer or `all` | Enter (20) |

Invalid input produces an error message and the question is repeated.

---

## 6. Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-1 | Only NumPy and pandas are imported |
| NFR-2 | Report runs in under 5 seconds for 1,820 rows |
| NFR-3 | Program must not crash on invalid input or a missing data file |
| NFR-4 | Code is modular, one function per task, with comments |
| NFR-5 | Output is readable, with headings and formatted numbers |
| NFR-6 | Wording remains cautious: flagged is a label, not fraud |

---

## 7. Design

### 7.1 Program flow
1. Load CSV (error message if file missing).
2. Inspect data (Task 139).
3. Clean: fill missing amounts (140), remove duplicates (141), convert Date.
4. Show main menu in a `while` loop until the user exits.
5. Option 1 runs Tasks 142-153. Option 2 collects filters, builds a Boolean mask, sorts, displays and optionally saves. Option 3 prints valid values.

### 7.2 Key techniques
- `if / elif / else` for menu and decisions, `while` loops for validated input, `for` loops for printing observations.
- NumPy: `np.mean`, `np.median`, `np.std`, `np.percentile`, `np.ones` for filter mask, Boolean indexing.
- pandas: `read_csv`, `groupby`, `agg`, `pivot_table`, `pd.cut`, `nlargest`, `isin`, `to_csv`.

### 7.3 Filter logic
A Boolean array of `True` values is created. Each answered filter is combined into it using `&`. The final mask selects the matching rows.

---

## 8. Test Cases

| # | Input | Expected result |
|---|---|---|
| T1 | Start program with CSV present | Inspection printed, 55 missing and 20 duplicates reported, 1,800 rows remain |
| T2 | Rename CSV and start | Error message, program ends without crash |
| T3 | Menu choice `9` | "Invalid choice" and menu repeats |
| T4 | Option 1, threshold `60000` | Count and total of transactions above 60,000 shown |
| T5 | City `Paris` | Invalid value message, valid cities listed, question repeats |
| T6 | Min `20000`, Max `1000` | Error message, both asked again |
| T7 | Date `31-12-2025` | Format error, asked again |
| T8 | City `Delhi, Mumbai`, Channel `UPI`, Debit, Flagged `No`, Min 1000, Max 20000 | Only matching rows displayed with summary |
| T9 | Filters matching nothing | "No records match" message |
| T10 | Save `y`, name `out` | `out.csv` created |

---

## 9. Limitations and Future Scope
- Data is synthetic and cannot support fraud conclusions.
- Single CSV file, console interface only.
- Future work: charts, monthly trend analysis, GUI, real-time input.
