def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    Returns list of raw data lines (excluding header and empty lines).
    """

    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as file:
                lines = file.readlines()

                # Remove header and empty lines
                data_lines = []
                for line in lines[1:]:
                    line = line.strip()
                    if line:
                        data_lines.append(line)

                return data_lines

        except FileNotFoundError:
            print("Error: File not found.")
            return []
        except UnicodeDecodeError:
            continue

    print("Error: Unable to read file with supported encodings.")
    return []
