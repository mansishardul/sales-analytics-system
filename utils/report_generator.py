from datetime import datetime
from collections import defaultdict

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted sales report
    """

    # Ensure output directory exists
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    now = datetime.now()
    total_transactions = len(transactions)
    total_revenue = calculate_total_revenue(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = sorted(t["Date"] for t in transactions)
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    region_stats = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, 5)
    customers = customer_analysis(transactions)
    daily_trends = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    # API enrichment summary
    enriched_success = [t for t in enriched_transactions if t.get("API_Match")]
    failed_enriched = [t for t in enriched_transactions if not t.get("API_Match")]
    success_rate = (len(enriched_success) / len(enriched_transactions)) * 100 if enriched_transactions else 0

    with open(output_file, "w", encoding="utf-8") as f:

        # 1. HEADER
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Records Processed: {total_transactions}\n\n")

        # 2. OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_transactions}\n")
        f.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

        # 3. REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write(f"{'Region':<10}{'Sales':>15}{'% of Total':>15}{'Transactions':>15}\n")

        for region, stats in region_stats.items():
            f.write(
                f"{region:<10}"
                f"₹{stats['total_sales']:>14,.2f}"
                f"{stats['percentage']:>14.2f}%"
                f"{stats['count']:>15}\n"
            )
        f.write("\n")

        # 4. TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write(f"{'Rank':<6}{'Product':<25}{'Qty Sold':>10}{'Revenue':>15}\n")
        for i, (name, qty, rev) in enumerate(top_products, 1):
            f.write(f"{i:<6}{name:<25}{qty:>10}₹{rev:>14,.2f}\n")
        f.write("\n")

        # 5. TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write(f"{'Rank':<6}{'Customer':<15}{'Spent':>15}{'Orders':>10}\n")
        for i, (cust, stats) in enumerate(list(customers.items())[:5], 1):
            f.write(
                f"{i:<6}{cust:<15}"
                f"₹{stats['total_spent']:>14,.2f}"
                f"{stats['orders']:>10}\n"
            )
        f.write("\n")

        # 6. DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write(f"{'Date':<12}{'Revenue':>15}{'Transactions':>15}{'Customers':>15}\n")
        for date, stats in daily_trends.items():
            f.write(
                f"{date:<12}"
                f"₹{stats['revenue']:>14,.2f}"
                f"{stats['transaction_count']:>15}"
                f"{stats['unique_customers']:>15}\n"
            )
        f.write("\n")

        # 7. PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write(f"Best Selling Day: {peak_day[0]} (₹{peak_day[1]:,.2f}, {peak_day[2]} transactions)\n")

        if low_products:
            f.write("Low Performing Products:\n")
            for name, qty, rev in low_products:
                f.write(f"- {name}: Qty {qty}, Revenue ₹{rev:,.2f}\n")
        else:
            f.write("No low performing products found\n")

        f.write("\n")

        # 8. API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write(f"Total Records Enriched: {len(enriched_success)}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")

        if failed_enriched:
            f.write("Products Not Enriched:\n")
            for t in failed_enriched:
                f.write(f"- {t['ProductName']} ({t['ProductID']})\n")

    print(f"[SUCCESS] Sales report generated at {output_file}")
