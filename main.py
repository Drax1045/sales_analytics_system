from utils.file_handler import read_sales_file
from utils.data_processor import clean_sales_data
from utils.api_handler import fetch_product_rating

FILE_PATH = "data/sales_data.txt"

def main():
    raw_lines = read_sales_file(FILE_PATH)

    valid_records, invalid_count, total_records = clean_sales_data(raw_lines)

    print(f"Total records parsed: {total_records}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    # API simulation
    if valid_records:
        sample_product_id = valid_records[0][2]
        rating = fetch_product_rating(sample_product_id)
        print("\nSample API Output:", rating)

if __name__ == "__main__":
    main()
