"""
Sales Analytics System
Main application entry point
Executes end-to-end analytics workflow
"""
from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    region_wise_sales,
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)
from utils.report_generator import generate_sales_report


FILE_PATH = "data/sales_data.txt"


def main():
    print("=" * 45)
    print("SALES ANALYTICS SYSTEM")
    print("=" * 45)

    try:
        # [1/10] Read sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data(FILE_PATH)
        print(f"✓ Successfully read {len(raw_lines)} records")

        # [2/10] Parse transactions
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        # [3/10] Show filter options
        print("\n[3/10] Filter Options Available:")
        regions = sorted({tx["Region"] for tx in transactions})
        amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in transactions]

        print(f"Regions: {', '.join(regions)}")
        print(f"Amount Range: ₹{int(min(amounts)):,} - ₹{int(max(amounts)):,}")

        apply_filter = input("\nDo you want to filter data? (y/n): ").lower().strip()

        filtered_transactions = transactions
        if apply_filter == "y":
            region = input("Enter region (or press Enter to skip): ").strip()
            min_amt = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_amt = input("Enter maximum amount (or press Enter to skip): ").strip()

            filtered_transactions = []
            for tx in transactions:
                amount = tx["Quantity"] * tx["UnitPrice"]

                if region and tx["Region"] != region:
                    continue
                if min_amt and amount < float(min_amt):
                    continue
                if max_amt and amount > float(max_amt):
                    continue

                filtered_transactions.append(tx)

            print(f"✓ Records after filtering: {len(filtered_transactions)}")

        # [4/10] Validate transactions
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(filtered_transactions)
        print(f"✓ Valid: {summary['final_count']} | Invalid: {invalid_count}")

        # [5/10] Perform analysis
        print("\n[5/10] Analyzing sales data...")
        region_wise_sales(valid_transactions)
        print("✓ Analysis complete")

        # [6/10] Fetch API data
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # [7/10] Enrich sales data
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

        enriched_count = sum(1 for tx in enriched_transactions if tx["API_Match"])
        success_rate = (enriched_count / len(enriched_transactions)) * 100
        print(f"✓ Enriched {enriched_count}/{len(enriched_transactions)} transactions ({success_rate:.1f}%)")

        # [8/10] Save enriched data
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)
        print("✓ Saved to data/enriched_sales_data.txt")

        # [9/10] Generate report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions)
        print("✓ Report saved to output/sales_report.txt")

        # [10/10] Done
        print("\n[10/10] Process Complete!")
        print("=" * 45)

    except Exception as e:
        print("\nAn error occurred:")
        print(str(e))


if __name__ == "__main__":
    main()
