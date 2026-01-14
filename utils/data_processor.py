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

def calculate_total_revenue(transactions):
    total = 0.0
    for tx in transactions:
        total += tx["Quantity"] * tx["UnitPrice"]
    return round(total, 2)

def region_wise_sales(transactions):
    region_data = {}

    total_revenue = sum(tx["Quantity"] * tx["UnitPrice"] for tx in transactions)

    for tx in transactions:
        region = tx["Region"].strip()
        if not region:
            continue

        revenue = tx["Quantity"] * tx["UnitPrice"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += revenue
        region_data[region]["transaction_count"] += 1

    for region in region_data:
        region_data[region]["percentage"] = round(
            (region_data[region]["total_sales"] / total_revenue) * 100, 2
        )

    return dict(
        sorted(
            region_data.items(),
            key=lambda x: x[1]["total_sales"],
            reverse=True
        )
    )

def top_selling_products(transactions, n=5):
    products = {}

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        if name not in products:
            products[name] = {"qty": 0, "revenue": 0.0}

        products[name]["qty"] += qty
        products[name]["revenue"] += revenue

    result = [
        (name, data["qty"], round(data["revenue"], 2))
        for name, data in products.items()
    ]

    result.sort(key=lambda x: x[1], reverse=True)
    return result[:n]


def customer_analysis(transactions):
    customers = {}

    for tx in transactions:
        customer_id = tx["CustomerID"].strip()
        if not customer_id:
            continue

        amount = tx["Quantity"] * tx["UnitPrice"]
        product = tx["ProductName"]

        if customer_id not in customers:
            customers[customer_id] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products": set()
            }

        customers[customer_id]["total_spent"] += amount
        customers[customer_id]["purchase_count"] += 1
        customers[customer_id]["products"].add(product)

    result = {}
    for cid, data in customers.items():
        result[cid] = {
            "total_spent": round(data["total_spent"], 2),
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(
                data["total_spent"] / data["purchase_count"], 2
            ),
            "products_bought": sorted(list(data["products"]))
        }

    return dict(
        sorted(result.items(), key=lambda x: x[1]["total_spent"], reverse=True)
    )

def daily_sales_trend(transactions):
    daily_data = {}

    for tx in transactions:
        date = tx["Date"]
        revenue = tx["Quantity"] * tx["UnitPrice"]
        customer = tx["CustomerID"].strip()

        if not date:
            continue

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transaction_count"] += 1

        if customer:
            daily_data[date]["customers"].add(customer)

    result = {}
    for date in sorted(daily_data):
        result[date] = {
            "revenue": round(daily_data[date]["revenue"], 2),
            "transaction_count": daily_data[date]["transaction_count"],
            "unique_customers": len(daily_data[date]["customers"])
        }

    return result

def find_peak_sales_day(transactions):
    daily = {}

    for tx in transactions:
        date = tx["Date"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if date not in daily:
            daily[date] = {"revenue": 0.0, "count": 0}

        daily[date]["revenue"] += revenue
        daily[date]["count"] += 1

    peak_date = max(daily, key=lambda d: daily[d]["revenue"])

    return (
        peak_date,
        round(daily[peak_date]["revenue"], 2),
        daily[peak_date]["count"]
    )

def low_performing_products(transactions, threshold=10):
    product_data = {}

    # Aggregate quantity and revenue per product
    for tx in transactions:
        product = tx["ProductName"]
        quantity = tx["Quantity"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += quantity
        product_data[product]["revenue"] += revenue

    # Filter products with quantity < threshold
    low_products = []
    for product, data in product_data.items():
        if data["quantity"] < threshold:
            low_products.append(
                (product, data["quantity"], round(data["revenue"], 2))
            )

    # Sort by total quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products
