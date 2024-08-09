import json
import csv
import argparse
import sys
import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def remove_null_values(line, output_cols):
    return {key: (None if line.get(key) in ["", "null", None] else line.get(key)) for key in output_cols}

def validate_search_field(data, search_field):
    if search_field not in data:
        raise ValueError(f"Search field '{search_field}' does not exist in the input JSON data")

def process_json_line(line, search_field, search_term, output_cols):
    try:
        data = json.loads(line)
        validate_search_field(data, search_field)
        if search_term.lower() in str(data.get(search_field, '')).lower():
            return remove_null_values(data, output_cols)
    except json.JSONDecodeError:
        logging.warning(f"Skipping invalid JSON line: {line.strip()}")
    return None


def filter_json_data(input_json_file, search_field, search_term, output_cols):
    filtered_lines = []
    with open(input_json_file, 'r') as file:
        for line in file:
            filtered_line = process_json_line(line, search_field, search_term, output_cols)
            if filtered_line:
                filtered_lines.append(filtered_line)
    return filtered_lines


def write_csv_file(output_csv_file, filtered_lines, output_cols):
    try:
        with open(output_csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=output_cols)
            writer.writeheader()
            writer.writerows(filtered_lines)
        logging.info(f"Filtered data written to {output_csv_file}")
    except Exception as e:
        logging.error(f"An error occurred while writing to file: {e}")
        sys.exit(1)


def main(input_json_file, output_csv_file, search_field, search_term, output_cols):
    if not all([search_field, search_term, output_cols]):
        logging.error("Search field, search term, and output columns cannot be empty")
        sys.exit(1)

    try:
        filtered_lines = filter_json_data(input_json_file, search_field, search_term, output_cols)
        if filtered_lines:
            write_csv_file(output_csv_file, filtered_lines, output_cols)
        else:
            logging.warning("No matching records found")
    except FileNotFoundError:
        logging.error(f"File {input_json_file} does not exist.")
        sys.exit(1)
    except ValueError as e:
        logging.error(e)
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup_logging()
    parser = argparse.ArgumentParser(description='Filter input JSON data and output a CSV')
    parser.add_argument('--input', required=True, help='Path to input JSON file')
    parser.add_argument('--output', required=True, help='Path to output CSV file')
    parser.add_argument('--search_field', required=True, help='Field in JSON to search')
    parser.add_argument('--search_term', required=True, help='Term in search_field to filter by')
    parser.add_argument('--output_cols', required=True, help='Comma-separated list of fields from original JSON to keep')
    args = parser.parse_args()

    output_cols = [field.strip() for field in args.output_cols.split(',')]
    main(args.input, args.output, args.search_field, args.search_term, output_cols)
