def read_sales_file(file_path):
    """
    Reads the sales data file and returns all non-empty lines.
    Handles non-UTF encoding.
    """
    records = []

    try:
        with open(file_path, "r", encoding="latin-1") as file:
            for line in file:
                line = line.strip()
                if line:
                    records.append(line)
    except FileNotFoundError:
        print("Sales data file not found.")
    except Exception as e:
        print("Error reading file:", e)

    return records
