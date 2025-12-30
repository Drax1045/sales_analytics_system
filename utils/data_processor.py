def clean_sales_data(raw_lines):
    """
    Cleans raw sales data based on given criteria.
    Returns valid records, invalid count, total records.
    """

    header = raw_lines[0]
    data_lines = raw_lines[1:]

    valid_records = []
    invalid_count = 0

    for line in data_lines:
        parts = line.split("|")

        # Must have exactly 8 fields
        if len(parts) != 8:
            invalid_count += 1
            continue

        transaction_id = parts[0]
        date = parts[1]
        product_id = parts[2]
        product_name = parts[3]
        quantity = parts[4]
        unit_price = parts[5]
        customer_id = parts[6]
        region = parts[7]

        # TransactionID validation
        if not transaction_id.startswith("T"):
            invalid_count += 1
            continue

        # Missing customer or region
        if not customer_id.strip() or not region.strip():
            invalid_count += 1
            continue

        # Clean commas
        product_name = product_name.replace(",", "")
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            invalid_count += 1
            continue

        # Quantity and price validation
        if quantity <= 0 or unit_price <= 0:
            invalid_count += 1
            continue

        valid_records.append([
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ])

    return valid_records, invalid_count, len(data_lines)
