# main.py

from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

from utils.report_generator import generate_sales_report


def main():
    """
    Main execution function as per assignment workflow
    """

    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # ---------------- STEP 1 ----------------
        print("\n[1/10] Reading sales data...")
        file_path = "sales_data.txt"
        raw_data = read_sales_data(file_path)
        print(f"✓ Successfully read {len(raw_data)} lines")

        # ---------------- STEP 2 ----------------
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_data)
        print(f"✓ Parsed {len(transactions)} records")

        # ---------------- STEP 3 ----------------
        print("\n[3/10] Filter Options Available:")
        print("Regions: North, South, East, West")
        print("Amount Range: ₹500 - ₹90,000")

        choice = input("Do you want to filter data? (y/n): ").strip().lower()

        region = min_amount = max_amount = None

        if choice == "y":
            region = input("Enter region (or press Enter to skip): ").strip() or None
            min_amount = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_amount = input("Enter maximum amount (or press Enter to skip): ").strip()

            min_amount = float(min_amount) if min_amount else None
            max_amount = float(max_amount) if max_amount else None

        # ---------------- STEP 4 ----------------
        print("\n[4/10] Validating transactions...")
        valid_data, invalid_count, summary = validate_and_filter(
            transactions,
            region=region,
            min_amount=min_amount,
            max_amount=max_amount
        )

        print(f"✓ Valid: {summary['final_count']} | Invalid: {summary['invalid']}")

        # ---------------- STEP 5 ----------------
        print("\n[5/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid_data)
        region_stats = region_wise_sales(valid_data)
        top_products = top_selling_products(valid_data)
        top_customers = customer_analysis(valid_data)
        daily_trends = daily_sales_trend(valid_data)
        peak_day = find_peak_sales_day(valid_data)
        low_products = low_performing_products(valid_data)
        print("✓ Analysis complete")

        # ---------------- STEP 6 ----------------
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # ---------------- STEP 7 ----------------
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_data = enrich_sales_data(valid_data, product_mapping)

        enriched_count = sum(1 for t in enriched_data if t["API_Match"])
        success_rate = (enriched_count / len(valid_data)) * 100 if valid_data else 0

        print(f"✓ Enriched {enriched_count}/{len(valid_data)} transactions ({success_rate:.1f}%)")

        # ---------------- STEP 8 ----------------
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_data)
        print("✓ Saved to: enriched_sales_data.txt")

        # ---------------- STEP 9 ----------------
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_data, enriched_data)
        print("✓ Report saved to: output/sales_report.txt")

        # ---------------- STEP 10 ----------------
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n[ERROR] Something went wrong!")
        print("Details:", str(e))


if __name__ == "__main__":
    main()
