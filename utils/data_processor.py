def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries.
    """

    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # Skip incorrect rows
        if len(parts) != 8:
            continue

        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

        # Clean commas
        product_name = product_name.replace(",", "")
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            continue

        transaction = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        transactions.append(transaction)

    return transactions
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid_transactions = []
    invalid_count = 0
    region_filtered = 0
    amount_filtered = 0

    for tx in transactions:
        try:
            if tx["Quantity"] <= 0 or tx["UnitPrice"] <= 0:
                invalid_count += 1
                continue

            if not (
                tx["TransactionID"].startswith("T") and
                tx["ProductID"].startswith("P") and
                tx["CustomerID"].startswith("C")
            ):
                invalid_count += 1
                continue

            amount = tx["Quantity"] * tx["UnitPrice"]

            if region and tx["Region"] != region:
                region_filtered += 1
                continue

            if min_amount and amount < min_amount:
                amount_filtered += 1
                continue

            if max_amount and amount > max_amount:
                amount_filtered += 1
                continue

            valid_transactions.append(tx)

        except KeyError:
            invalid_count += 1

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "filtered_by_region": region_filtered,
        "filtered_by_amount": amount_filtered,
        "final_count": len(valid_transactions)
    }

    return valid_transactions, invalid_count, summary
