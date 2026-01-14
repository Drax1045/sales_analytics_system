import random

def fetch_product_rating(product_id):
    """
    Simulates fetching product rating from an external API.
    """
    return {
        "product_id": product_id,
        "rating": round(random.uniform(3.0, 5.0), 1)
    }
import requests

BASE_URL = "https://dummyjson.com/products"
def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print("API fetch successful")
        return products

    except Exception as e:
        print("API fetch failed:", e)
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    """
    mapping = {}

    for product in api_products:
        pid = product.get("id")
        if pid is None:
            continue

        mapping[pid] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return mapping

def enrich_sales_data(transactions, product_mapping):
    enriched = []

    for tx in transactions:
        enriched_tx = tx.copy()

        product_id = tx.get("ProductID", "")
        numeric_id = int("".join(filter(str.isdigit, product_id))) if product_id else None

        api_product = None
        if numeric_id:
            api_product = product_mapping.get(numeric_id)

        # OPTIONAL fallback by product name
        if not api_product:
            for p in product_mapping.values():
                if p["title"].lower() in tx["ProductName"].lower() or \
                   tx["ProductName"].lower() in p["title"].lower():
                    api_product = p
                    break

        if api_product:
            enriched_tx["API_Category"] = api_product.get("category")
            enriched_tx["API_Brand"] = api_product.get("brand")
            enriched_tx["API_Rating"] = api_product.get("rating")
            enriched_tx["API_Match"] = True
        else:
            enriched_tx["API_Category"] = None
            enriched_tx["API_Brand"] = None
            enriched_tx["API_Rating"] = None
            enriched_tx["API_Match"] = False

        enriched.append(enriched_tx)

    return enriched


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions to file
    """
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w") as f:
        f.write("|".join(headers) + "\n")

        for tx in enriched_transactions:
            row = []
            for h in headers:
                value = tx.get(h)
                if value is None:
                    value = ""
                row.append(str(value))
            f.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filename}")
