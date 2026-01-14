from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, validate_and_filter
from utils.api_handler import (
    fetch_product_rating,
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)
from utils.report_generator import generate_sales_report

FILE_PATH = "data/sales_data.txt"


def main():
    # =========================
    # STEP 1: Read raw sales file
    # =========================
    raw_lines = read_sales_data(FILE_PATH)

    # =========================
    # STEP 2: Parse transactions
    # =========================
    transactions = parse_transactions(raw_lines)

    # =========================
    # STEP 3: Validate & clean data
    # =========================
    valid_transactions, invalid_count, summary = validate_and_filter(transactions)

    print(f"Total records parsed: {summary['total_input']}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {summary['final_count']}")

    # =========================
    # STEP 4: API Simulation (Q4 requirement)
    # =========================
    if valid_transactions:
        sample_product_id = valid_transactions[0]["ProductID"]
        rating = fetch_product_rating(sample_product_id)
        print("\nSample API Output:", rating)

    # =========================
    # STEP 5: Fetch API products
    # =========================
    api_products = fetch_all_products()

    # =========================
    # STEP 6: Create product mapping
    # =========================
    product_mapping = create_product_mapping(api_products)

    # =========================
    # STEP 7: Enrich sales data
    # =========================
    enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

    # =========================
    # STEP 8: Generate sales report (Q5)
    # =========================
    generate_sales_report(valid_transactions, enriched_transactions)
    print("\nSales report generated at output/sales_report.txt")


if __name__ == "__main__":
    main()
