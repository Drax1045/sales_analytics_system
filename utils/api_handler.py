import random

def fetch_product_rating(product_id):
    """
    Simulates fetching product rating from an external API.
    """
    return {
        "product_id": product_id,
        "rating": round(random.uniform(3.0, 5.0), 1)
    }
