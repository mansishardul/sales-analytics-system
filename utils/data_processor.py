# utils/data_processor.py
from collections import defaultdict

def calculate_total_revenue(transactions):
    total = 0.0
    for txn in transactions:
        total += txn['Quantity'] * txn['UnitPrice']
    return round(total, 2)


def region_wise_sales(transactions):
    region_data = {}
    total_sales = 0.0

    for txn in transactions:
        region = txn['Region']
        amount = txn['Quantity'] * txn['UnitPrice']
        total_sales += amount

        if region not in region_data:
            region_data[region] = {'total_sales': 0.0, 'count': 0}

        region_data[region]['total_sales'] += amount
        region_data[region]['count'] += 1

    for r in region_data:
        region_data[r]['percentage'] = round(
            (region_data[r]['total_sales'] / total_sales) * 100, 2
        )

    return dict(sorted(
        region_data.items(),
        key=lambda x: x[1]['total_sales'],
        reverse=True
    ))


def top_selling_products(transactions, n=5):
    product_data = {}

    for txn in transactions:
        p = txn['ProductName']
        if p not in product_data:
            product_data[p] = {'qty': 0, 'revenue': 0.0}

        product_data[p]['qty'] += txn['Quantity']
        product_data[p]['revenue'] += txn['Quantity'] * txn['UnitPrice']

    result = [
        (p, v['qty'], round(v['revenue'], 2))
        for p, v in product_data.items()
    ]

    result.sort(key=lambda x: x[1], reverse=True)
    return result[:n]


def customer_analysis(transactions):
    customer_data = {}

    for txn in transactions:
        c = txn['CustomerID']
        amount = txn['Quantity'] * txn['UnitPrice']

        if c not in customer_data:
            customer_data[c] = {
                'total_spent': 0.0,
                'orders': 0,
                'products': set()
            }

        customer_data[c]['total_spent'] += amount
        customer_data[c]['orders'] += 1
        customer_data[c]['products'].add(txn['ProductName'])

    for c in customer_data:
        customer_data[c]['avg_order_value'] = round(
            customer_data[c]['total_spent'] / customer_data[c]['orders'], 2
        )
        customer_data[c]['total_spent'] = round(customer_data[c]['total_spent'], 2)
        customer_data[c]['products'] = list(customer_data[c]['products'])

    return dict(sorted(
        customer_data.items(),
        key=lambda x: x[1]['total_spent'],
        reverse=True
    ))



def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date.
    Returns dictionary sorted by date.
    """
    daily_data = defaultdict(lambda: {
        "revenue": 0.0,
        "transaction_count": 0,
        "customers": set()
    })

    for txn in transactions:
        date = txn["Date"]
        amount = txn["Quantity"] * txn["UnitPrice"]
        customer = txn["CustomerID"]

        daily_data[date]["revenue"] += amount
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(customer)

    # Final formatting
    result = {}
    for date in sorted(daily_data.keys()):
        result[date] = {
            "revenue": round(daily_data[date]["revenue"], 2),
            "transaction_count": daily_data[date]["transaction_count"],
            "unique_customers": len(daily_data[date]["customers"])
        }

    return result

def find_peak_sales_day(transactions):
    """
    Identifies the date with the highest revenue.
    Returns: (date, revenue, transaction_count)
    """
    daily_totals = {}

    for txn in transactions:
        date = txn["Date"]
        amount = txn["Quantity"] * txn["UnitPrice"]

        if date not in daily_totals:
            daily_totals[date] = {
                "revenue": 0.0,
                "transaction_count": 0
            }

        daily_totals[date]["revenue"] += amount
        daily_totals[date]["transaction_count"] += 1

    peak_date = max(
        daily_totals.items(),
        key=lambda x: x[1]["revenue"]
    )

    return (
        peak_date[0],
        round(peak_date[1]["revenue"], 2),
        peak_date[1]["transaction_count"]
    )

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with total quantity sold below threshold.
    Returns list of tuples sorted by quantity ascending.
    """
    product_data = {}

    for txn in transactions:
        product = txn["ProductName"]
        quantity = txn["Quantity"]
        revenue = txn["Quantity"] * txn["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "total_quantity": 0,
                "total_revenue": 0.0
            }

        product_data[product]["total_quantity"] += quantity
        product_data[product]["total_revenue"] += revenue

    low_products = [
        (
            product,
            data["total_quantity"],
            round(data["total_revenue"], 2)
        )
        for product, data in product_data.items()
        if data["total_quantity"] < threshold
    ]

    # Sort by total quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products


