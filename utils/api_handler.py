import requests


# --------------------------------------------------
# Task 3.1(a): Fetch All Products
# --------------------------------------------------
def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get("products", [])

    except Exception as e:
        print(f"[ERROR] API fetch failed: {e}")
        return []


# --------------------------------------------------
# Task 3.1(b): Create Product Mapping
# --------------------------------------------------
def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    """
    product_mapping = {}

    for product in api_products:
        product_mapping[product["id"]] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return product_mapping


# --------------------------------------------------
# Task 3.2: Enrich Sales Data
# --------------------------------------------------
def enrich_sales_data(transactions, product_mapping):
    """
    Enrich transactions using ProductName ↔ API title
    """
    enriched = []

    for txn in transactions:
        enriched_txn = txn.copy()
        match_found = False

        for api_product in product_mapping.values():
            if txn["ProductName"].lower() == api_product["title"].lower():
                enriched_txn["API_Category"] = api_product["category"]
                enriched_txn["API_Brand"] = api_product["brand"]
                enriched_txn["API_Rating"] = api_product["rating"]
                enriched_txn["API_Match"] = True
                match_found = True
                break

        if not match_found:
            enriched_txn["API_Category"] = None
            enriched_txn["API_Brand"] = None
            enriched_txn["API_Rating"] = None
            enriched_txn["API_Match"] = False

        enriched.append(enriched_txn)

    return enriched


# --------------------------------------------------
# Save Enriched Data
# --------------------------------------------------
def save_enriched_data(enriched_transactions, filename="enriched_sales_data.txt"):
    """
    Saves enriched data to file
    """

    header = (
        "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
        "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(header)

        for txn in enriched_transactions:
            f.write(
                f"{txn.get('TransactionID')}|"
                f"{txn.get('Date')}|"
                f"{txn.get('ProductID')}|"
                f"{txn.get('ProductName')}|"
                f"{txn.get('Quantity')}|"
                f"{txn.get('UnitPrice')}|"
                f"{txn.get('CustomerID')}|"
                f"{txn.get('Region')}|"
                f"{txn.get('API_Category') or ''}|"
                f"{txn.get('API_Brand') or ''}|"
                f"{txn.get('API_Rating') or ''}|"
                f"{txn.get('API_Match')}\n"
            )

    print(f"[SUCCESS] Enriched data saved to {filename}")
