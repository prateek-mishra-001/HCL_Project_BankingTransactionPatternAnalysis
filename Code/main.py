"""
Project 10 : Banking Transaction Pattern Analysis
-------------------------------------------------
Industry : Banking / FinTech
Libraries: ONLY NumPy and pandas (no other library is imported).

The dataset is SYNTHETIC and must NOT be used for fraud claims.
'Flagged' is a supplied label, not proof of fraud.

Menu
  1. Full analysis report         (Tasks 139 - 153)
  2. Custom filter and sort       (user decides the parameters)
  3. Show valid input values      (help for the user)
  4. Exit
"""

import numpy as np
import pandas as pd

DATA_FILE = "10_bank_transactions.csv"

pd.set_option("display.width", 220)
pd.set_option("display.max_columns", 30)
pd.set_option("display.float_format", "{:,.2f}".format)

SORT_COLUMNS = ["Transaction_ID", "Date", "Account_ID", "Account_Type",
                "City", "Channel", "Transaction_Type", "Amount", "Flagged"]

BAND_BINS = [0, 1000, 5000, 10000, 25000, 50000, np.inf]
BAND_LABELS = ["Very Low (<1K)", "Low (1K-5K)", "Medium (5K-10K)",
               "High (10K-25K)", "Very High (25K-50K)", "Premium (50K+)"]


# --------------------------------------------------------------------------
# helper functions
# --------------------------------------------------------------------------
def heading(text):
    print("\n" + "=" * 75)
    print(text)
    print("=" * 75)


def load_data(path):
    """Task 139 - load the CSV file."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print("ERROR: '" + path + "' not found.")
        print("Run  python generate_data.py  first to create the file.")
        return None


def ask_choice(label, valid_values, skip_text="Enter = all"):
    """Ask for one or more comma separated values. Enter = skip (None)."""
    lookup = {str(v).lower(): v for v in valid_values}
    while True:
        text = input(label + " [" + skip_text + "]: ").strip()
        if text == "":
            return None
        chosen = []
        bad = []
        for part in text.split(","):
            key = part.strip().lower()
            if key in lookup:
                chosen.append(lookup[key])
            else:
                bad.append(part.strip())
        if len(bad) == 0:
            return chosen
        print("  Invalid value(s):", ", ".join(bad))
        print("  Valid values are:", ", ".join(str(v) for v in valid_values))


def ask_number(label):
    """Ask for a number. Enter = skip (None). Repeats until valid."""
    while True:
        text = input(label + " [Enter = skip]: ").strip().replace(",", "")
        if text == "":
            return None
        try:
            return float(text)
        except ValueError:
            print("  Please type a number such as 5000 or 25000.50")


def ask_date(label):
    """Ask for a date in YYYY-MM-DD format. Enter = skip (None)."""
    while True:
        text = input(label + " (YYYY-MM-DD) [Enter = skip]: ").strip()
        if text == "":
            return None
        try:
            return pd.to_datetime(text, format="%Y-%m-%d")
        except ValueError:
            print("  Wrong format. Example: 2025-06-30")


# --------------------------------------------------------------------------
# Tasks 139 - 141 : inspect and clean
# --------------------------------------------------------------------------
def inspect_data(df):
    heading("TASK 139 - LOAD AND INSPECT TRANSACTION RECORDS")
    print("Rows x Columns :", df.shape)
    print("\nFirst 5 records:")
    print(df.head())
    print("\nData types:")
    print(df.dtypes)
    print("\nMissing values per column:")
    print(df.isnull().sum())
    print("\nStatistical summary of Amount:")
    print(df["Amount"].describe())


def handle_missing(df):
    """Task 140 - fill missing Amount with the median of the same
    Account_Type + Transaction_Type group (fallback: overall median)."""
    heading("TASK 140 - MISSING TRANSACTION AMOUNTS")
    missing_count = int(df["Amount"].isnull().sum())
    print("Missing amounts found :", missing_count)
    print("Percentage            : {:.2f}%".format(missing_count / len(df) * 100))

    if missing_count > 0:
        group_median = df.groupby(["Account_Type", "Transaction_Type"])["Amount"].transform("median")
        df["Amount"] = df["Amount"].fillna(group_median)
        df["Amount"] = df["Amount"].fillna(df["Amount"].median())
        print("Handling method       : filled with group median "
              "(Account_Type + Transaction_Type)")
        print("Missing after fixing  :", int(df["Amount"].isnull().sum()))
    else:
        print("No missing amounts - nothing to fix.")
    return df


def handle_duplicates(df):
    """Task 141 - check duplicate Transaction_ID values."""
    heading("TASK 141 - DUPLICATE TRANSACTION_ID CHECK")
    dup_extra = int(df["Transaction_ID"].duplicated().sum())
    dup_all = df[df["Transaction_ID"].duplicated(keep=False)]
    print("Extra duplicate rows        :", dup_extra)
    print("Rows involved in duplicates :", len(dup_all))

    if dup_extra > 0:
        print("\nSample duplicate records:")
        print(dup_all.sort_values("Transaction_ID").head(6))
        df = df.drop_duplicates(subset="Transaction_ID", keep="first").reset_index(drop=True)
        print("\nDuplicates removed (first record kept).")
        print("Rows after cleaning:", len(df))
    else:
        print("No duplicate Transaction_ID found.")
    return df


def prepare(df):
    """Run cleaning steps and fix the Date column."""
    df = handle_missing(df)
    df = handle_duplicates(df)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


# --------------------------------------------------------------------------
# Tasks 142 - 153 : analysis
# --------------------------------------------------------------------------
def credit_debit_totals(df):
    heading("TASK 142 - TOTAL CREDITS AND TOTAL DEBITS")
    credits = df.loc[df["Transaction_Type"] == "Credit", "Amount"].sum()
    debits = df.loc[df["Transaction_Type"] == "Debit", "Amount"].sum()
    print("Total Credits : Rs {:,.2f}".format(credits))
    print("Total Debits  : Rs {:,.2f}".format(debits))
    print("Net Flow      : Rs {:,.2f}".format(credits - debits))
    if credits > debits:
        print("Result        : Credits are higher than debits.")
    elif debits > credits:
        print("Result        : Debits are higher than credits.")
    else:
        print("Result        : Credits and debits are equal.")


def amount_statistics(df):
    heading("TASK 143 - MEAN, MEDIAN AND STANDARD DEVIATION")
    amounts = df["Amount"].to_numpy()
    print("Mean               : Rs {:,.2f}".format(np.mean(amounts)))
    print("Median             : Rs {:,.2f}".format(np.median(amounts)))
    print("Standard deviation : Rs {:,.2f}".format(np.std(amounts, ddof=1)))
    if np.mean(amounts) > np.median(amounts):
        print("Note: mean > median, so a few large transactions pull the average up.")


def channel_summary(df):
    heading("TASK 144 - TRANSACTION VOLUME BY CHANNEL")
    table = df.groupby("Channel")["Amount"].agg(
        Transactions="count", Total_Value="sum", Average="mean")
    table["Share_%"] = table["Transactions"] / table["Transactions"].sum() * 100
    print(table.sort_values("Transactions", ascending=False))


def city_summary(df):
    heading("TASK 145 - TOTAL TRANSACTION VALUE BY CITY")
    table = df.groupby("City")["Amount"].agg(
        Transactions="count", Total_Value="sum", Average="mean")
    print(table.sort_values("Total_Value", ascending=False))


def flagged_summary(df):
    heading("TASK 146 - FLAGGED TRANSACTION COUNT AND PERCENTAGE")
    is_flagged = (df["Flagged"] == "Yes").to_numpy()
    count = int(is_flagged.sum())
    pct = np.mean(is_flagged) * 100
    print("Flagged transactions :", count, "of", len(df))
    print("Flagged percentage   : {:.2f}%".format(pct))
    print("Value of flagged txn : Rs {:,.2f}".format(df.loc[df["Flagged"] == "Yes", "Amount"].sum()))
    print("(Flagged is a supplied label, NOT proof of fraud.)")


def flagged_by_channel(df):
    heading("TASK 147 - FLAGGED PERCENTAGE BY CHANNEL")
    table = df.groupby("Channel").agg(
        Transactions=("Flagged", "count"),
        Flagged=("Flagged", lambda s: int((s == "Yes").sum())))
    table["Flagged_%"] = table["Flagged"] / table["Transactions"] * 100
    print(table.sort_values("Flagged_%", ascending=False))


def top_ten(df):
    heading("TASK 148 - 10 LARGEST TRANSACTIONS")
    print(df.nlargest(10, "Amount")[["Transaction_ID", "Date", "Account_Type", "City",
                                     "Channel", "Transaction_Type", "Amount", "Flagged"]]
          .to_string(index=False))


def account_type_totals(df):
    heading("TASK 149 - CREDIT / DEBIT TOTALS BY ACCOUNT TYPE")
    grouped = df.groupby(["Account_Type", "Transaction_Type"])["Amount"].agg(
        Count="count", Total="sum", Average="mean")
    print(grouped)
    print("\nSide-by-side totals:")
    side = df.pivot_table(index="Account_Type", columns="Transaction_Type",
                          values="Amount", aggfunc="sum")
    side["Net"] = side["Credit"] - side["Debit"]
    print(side)


def iqr_outliers(df):
    heading("TASK 150 - OUTLIERS USING IQR")
    amounts = df["Amount"].to_numpy()
    q1, q3 = np.percentile(amounts, [25, 75])
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    print("Q1 = {:,.2f}   Q3 = {:,.2f}   IQR = {:,.2f}".format(q1, q3, iqr))
    print("Lower bound = {:,.2f}   Upper bound = {:,.2f}".format(lower, upper))
    outliers = df[(df["Amount"] < lower) | (df["Amount"] > upper)]
    print("Outliers found:", len(outliers),
          "({:.2f}% of records)".format(len(outliers) / len(df) * 100))
    if len(outliers) > 0:
        print("\nLargest 5 outliers:")
        print(outliers.nlargest(5, "Amount")[["Transaction_ID", "Channel", "City", "Amount"]]
              .to_string(index=False))
    return outliers


def amount_bands(df):
    heading("TASK 151 - TRANSACTION AMOUNT BANDS")
    df = df.copy()
    df["Amount_Band"] = pd.cut(df["Amount"], bins=BAND_BINS, labels=BAND_LABELS, right=False)
    table = df.groupby("Amount_Band", observed=False)["Amount"].agg(Transactions="count", Total="sum")
    table["Share_%"] = table["Transactions"] / table["Transactions"].sum() * 100
    print(table)


def numpy_threshold(df, threshold=None):
    heading("TASK 152 - NUMPY BOOLEAN INDEXING ABOVE A THRESHOLD")
    if threshold is None:
        threshold = ask_number("Enter threshold amount (default 50000)")
        if threshold is None:
            threshold = 50000.0
    amounts = df["Amount"].to_numpy()
    mask = amounts > threshold                 # NumPy Boolean array
    print("Threshold            : Rs {:,.2f}".format(threshold))
    print("Transactions above   :", int(mask.sum()))
    if mask.sum() > 0:
        print("Total value above    : Rs {:,.2f}".format(amounts[mask].sum()))
        print("Average value above  : Rs {:,.2f}".format(amounts[mask].mean()))
        print("\nFirst 10 matching records:")
        print(df[mask].head(10).to_string(index=False))
    else:
        print("No transaction is above this threshold.")


def observations(df):
    heading("TASK 153 - FIVE CAUTIOUS OBSERVATIONS AND RECOMMENDATIONS")
    obs = []

    # 1 channel concentration
    ch = df["Channel"].value_counts()
    obs.append("The busiest channel is {} with {:.1f}% of transactions. Capacity planning "
               "may need to focus on it, but this is synthetic data, so confirm with real "
               "volumes before acting.".format(ch.index[0], ch.iloc[0] / len(df) * 100))

    # 2 city value
    city = df.groupby("City")["Amount"].sum().sort_values(ascending=False)
    obs.append("{} has the highest total transaction value (Rs {:,.0f}). Branch and ATM "
               "planning could be reviewed there; city totals reflect the sample only."
               .format(city.index[0], city.iloc[0]))

    # 3 flagged
    flag_rate = df.groupby("Channel")["Flagged"].apply(lambda s: (s == "Yes").mean() * 100)
    obs.append("{} has the highest flagged share ({:.1f}%). 'Flagged' is only a supplied "
               "label, so use it to prioritise manual review, not to claim fraud."
               .format(flag_rate.idxmax(), flag_rate.max()))

    # 4 outliers
    q1, q3 = np.percentile(df["Amount"], [25, 75])
    upper = q3 + 1.5 * (q3 - q1)
    n_out = int((df["Amount"] > upper).sum())
    if n_out > 0:
        obs.append("{} transactions are above the IQR upper bound (Rs {:,.0f}). Review "
                   "whether limits and alerts suit very large transfers.".format(n_out, upper))
    else:
        obs.append("No high-side IQR outliers exist, so current limits look consistent "
                   "with this sample.")

    # 5 credit vs debit
    credits = df.loc[df["Transaction_Type"] == "Credit", "Amount"].sum()
    debits = df.loc[df["Transaction_Type"] == "Debit", "Amount"].sum()
    if debits > credits:
        obs.append("Debits exceed credits by Rs {:,.0f}. Monitor liquidity trends over a "
                   "longer period before drawing conclusions.".format(debits - credits))
    else:
        obs.append("Credits exceed debits by Rs {:,.0f}. Monitor this over a longer "
                   "period before drawing conclusions.".format(credits - debits))

    for number, text in enumerate(obs, start=1):
        print("{}. {}".format(number, text))


def full_report(df):
    credit_debit_totals(df)
    amount_statistics(df)
    channel_summary(df)
    city_summary(df)
    flagged_summary(df)
    flagged_by_channel(df)
    top_ten(df)
    account_type_totals(df)
    iqr_outliers(df)
    amount_bands(df)
    numpy_threshold(df)
    observations(df)


# --------------------------------------------------------------------------
# Custom filter and sort (user-driven)
# --------------------------------------------------------------------------
def show_valid_values(df):
    heading("VALID INPUT VALUES")
    print("City             :", ", ".join(sorted(df["City"].unique())))
    print("Channel          :", ", ".join(sorted(df["Channel"].unique())))
    print("Account_Type     :", ", ".join(sorted(df["Account_Type"].unique())))
    print("Transaction_Type :", ", ".join(sorted(df["Transaction_Type"].unique())))
    print("Flagged          : Yes, No")
    print("Amount range     : {:,.2f} to {:,.2f}".format(df["Amount"].min(), df["Amount"].max()))
    print("Date range       : {} to {}".format(df["Date"].min().date(), df["Date"].max().date()))
    print("Amount bands     :")
    for label in BAND_LABELS:
        print("    ", label)
    print("Sort columns     :", ", ".join(SORT_COLUMNS))
    print("\nTips: separate several values with a comma, e.g.  Delhi, Mumbai")
    print("      Press Enter on any question to skip that filter.")


def custom_filter(df):
    heading("CUSTOM FILTER AND SORT  (press Enter to skip any question)")
    mask = np.ones(len(df), dtype=bool)

    cities = ask_choice("City (e.g. Delhi, Mumbai)", sorted(df["City"].unique()))
    if cities is not None:
        mask = mask & df["City"].isin(cities).to_numpy()

    channels = ask_choice("Channel (e.g. UPI, ATM)", sorted(df["Channel"].unique()))
    if channels is not None:
        mask = mask & df["Channel"].isin(channels).to_numpy()

    acc_types = ask_choice("Account type (e.g. Savings, Business)",
                           sorted(df["Account_Type"].unique()))
    if acc_types is not None:
        mask = mask & df["Account_Type"].isin(acc_types).to_numpy()

    txn_types = ask_choice("Transaction type (Credit / Debit)",
                           sorted(df["Transaction_Type"].unique()))
    if txn_types is not None:
        mask = mask & df["Transaction_Type"].isin(txn_types).to_numpy()

    flagged = ask_choice("Flagged (Yes / No)", ["Yes", "No"])
    if flagged is not None:
        mask = mask & df["Flagged"].isin(flagged).to_numpy()

    band = ask_choice("Amount band (type exact band name from option 3)",
                      BAND_LABELS, skip_text="Enter = use min/max instead")
    if band is not None:
        band_index = BAND_LABELS.index(band[0])
        low, high = BAND_BINS[band_index], BAND_BINS[band_index + 1]
        mask = mask & (df["Amount"].to_numpy() >= low) & (df["Amount"].to_numpy() < high)
        print("  Using band range: {:,.0f} to {}".format(low, "no limit" if high == np.inf else "{:,.0f}".format(high)))
    else:
        while True:
            min_amt = ask_number("Minimum amount")
            max_amt = ask_number("Maximum amount")
            if min_amt is not None and max_amt is not None and min_amt > max_amt:
                print("  Minimum cannot be greater than maximum. Try again.")
            else:
                break
        if min_amt is not None:
            mask = mask & (df["Amount"].to_numpy() >= min_amt)
        if max_amt is not None:
            mask = mask & (df["Amount"].to_numpy() <= max_amt)

    while True:
        start = ask_date("Start date")
        end = ask_date("End date")
        if start is not None and end is not None and start > end:
            print("  Start date cannot be after end date. Try again.")
        else:
            break
    if start is not None:
        mask = mask & (df["Date"] >= start).to_numpy()
    if end is not None:
        mask = mask & (df["Date"] <= end).to_numpy()

    result = df[mask].copy()

    if len(result) == 0:
        print("\nNo records match these conditions. Try relaxing some filters.")
        return

    # sorting
    print("\nSort columns:", ", ".join(SORT_COLUMNS))
    sort_col = ask_choice("Sort by column", SORT_COLUMNS, skip_text="Enter = no sorting")
    if sort_col is not None:
        order = input("Order - A for ascending, D for descending [D]: ").strip().lower()
        ascending = (order == "a")
        result = result.sort_values(sort_col[0], ascending=ascending)

    # how many rows to show
    while True:
        rows_text = input("How many rows to display? [20, or type 'all']: ").strip().lower()
        if rows_text == "":
            rows = 20
            break
        elif rows_text == "all":
            rows = len(result)
            break
        elif rows_text.isdigit() and int(rows_text) > 0:
            rows = int(rows_text)
            break
        else:
            print("  Enter a positive whole number or 'all'.")

    heading("RESULT")
    print("Matching records :", len(result))
    print("Total amount     : Rs {:,.2f}".format(result["Amount"].sum()))
    print("Average amount   : Rs {:,.2f}".format(result["Amount"].mean()))
    print("Flagged records  :", int((result["Flagged"] == "Yes").sum()))
    print("Credits / Debits : {} / {}".format(
        int((result["Transaction_Type"] == "Credit").sum()),
        int((result["Transaction_Type"] == "Debit").sum())))
    print()
    show = result.head(rows).copy()
    show["Date"] = show["Date"].dt.strftime("%Y-%m-%d")
    print(show.to_string(index=False))

    save = input("\nSave this result to a CSV file? (y/n) [n]: ").strip().lower()
    if save == "y":
        name = input("File name [filtered_result.csv]: ").strip()
        if name == "":
            name = "filtered_result.csv"
        if not name.endswith(".csv"):
            name = name + ".csv"
        result.to_csv(name, index=False)
        print("Saved", len(result), "records to", name)


# --------------------------------------------------------------------------
# main menu
# --------------------------------------------------------------------------
def main():
    raw = load_data(DATA_FILE)
    if raw is None:
        return

    inspect_data(raw)
    df = prepare(raw)

    while True:
        heading("MAIN MENU - BANKING TRANSACTION PATTERN ANALYSIS")
        print("1. Full analysis report (Tasks 142 - 153)")
        print("2. Custom filter and sort")
        print("3. Show valid input values")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            full_report(df)
        elif choice == "2":
            custom_filter(df)
        elif choice == "3":
            show_valid_values(df)
        elif choice == "4":
            print("Thank you. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
