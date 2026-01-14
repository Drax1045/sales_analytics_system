from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, validate_and_filter
from utils.api_handler import fetch_product_rating

FILE_PATH = "data/sales_data.txt"

def main():
    # Step 1: Read raw file
    raw_lines = read_sales_data(FILE_PATH)

    # Step 2: Parse transactions
    transactions = parse_transactions(raw_lines)

    # Step 3: Validate & filter
    valid_records, invalid_count, summary = validate_and_filter(transactions)

    print(f"Total records parsed: {summary['total_input']}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {summary['final_count']}")

    # Step 4: API simulation (already required in Q4)
    if valid_records:
        sample_product_id = valid_records[0]["ProductID"]
        rating = fetch_product_rating(sample_product_id)
        print("\nSample API Output:", rating)

if __name__ == "__main__":
    main()
