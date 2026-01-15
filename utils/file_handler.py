# utils/file_handler.py

def read_sales_data(filename):
    """
    Reads sales data file safely with multiple encodings.
    Returns list of raw data lines (excluding header).
    """
    encodings_to_try = ["utf-8", "latin-1", "cp1252"]

    for encoding in encodings_to_try:
        try:
            with open(filename, "r", encoding=encoding) as file:
                lines = file.readlines()

                cleaned_lines = []
                for line in lines[1:]:  # skip header
                    line = line.strip()
                    if line:
                        cleaned_lines.append(line)

                return cleaned_lines

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return []

    print("Unable to read file with supported encodings.")
    return []


def parse_transactions(raw_lines):
    """
    Parses raw pipe-delimited lines into clean transaction dictionaries.
    """
    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # Skip malformed rows
        if len(parts) != 8:
            continue

        try:
            transaction = {
                "TransactionID": parts[0].strip(),
                "Date": parts[1].strip(),
                "ProductID": parts[2].strip(),
                "ProductName": parts[3].replace(",", "").strip(),
                "Quantity": int(parts[4].replace(",", "").strip()),
                "UnitPrice": float(parts[5].replace(",", "").strip()),
                "CustomerID": parts[6].strip(),
                "Region": parts[7].strip()
            }

            transactions.append(transaction)

        except ValueError:
            # Skip rows with invalid numeric data
            continue

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    Returns:
    (valid_transactions, invalid_count, summary_dict)
    """
    valid_transactions = []
    invalid_count = 0

    for txn in transactions:
        try:
            # Validation rules
            if (
                txn["Quantity"] <= 0 or
                txn["UnitPrice"] <= 0 or
                not txn["TransactionID"].startswith("T") or
                not txn["ProductID"].startswith("P") or
                not txn["CustomerID"].startswith("C") or
                not txn["Region"].strip()
            ):
                invalid_count += 1
                continue

            valid_transactions.append(txn)

        except Exception:
            invalid_count += 1

    # Apply region filter
    if region:
        valid_transactions = [
            t for t in valid_transactions
            if t["Region"] == region
        ]

    # Apply minimum amount filter
    if min_amount is not None:
        valid_transactions = [
            t for t in valid_transactions
            if t["Quantity"] * t["UnitPrice"] >= min_amount
        ]

    # Apply maximum amount filter
    if max_amount is not None:
        valid_transactions = [
            t for t in valid_transactions
            if t["Quantity"] * t["UnitPrice"] <= max_amount
        ]

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "final_count": len(valid_transactions)
    }

    return valid_transactions, invalid_count, summary
