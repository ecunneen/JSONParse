import json
import csv
import argparse
import sys
import logging


def setup_logging():
    # Configure logging to display timestamp, log level, and message
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def remove_null_values(line, output_cols):
    # Replace null, empty string, or "null" string values with None in the specified columns
    return {key: (None if line.get(key) in ["", "null", None] else line.get(key)) for key in output_cols}


def validate_search_field(data, search_field):
    # Ensure the search field exists in the JSON data; raise an error if it does not
    if search_field not in data:
        raise ValueError(f"Search field '{search_field}' does not exist in the input JSON data")


def process_json_line(line, search_field, search_term, output_cols):
    try:
        # Parse the JSON line
        data = json.loads(line)
        # Validate the presence of the search field
        validate_search_field(data, search_field)
        # Check if the search term is present in the specified search field (case-insensitive)
        if search_term.lower() in str(data.get(search_field, '')).lower():
            # Filter the JSON line based on the output columns and return it
            return remove_null_values(data, output_cols)
    except json.JSONDecodeError:
        # Log a warning and skip the line if it's not valid JSON
        logging.warning(f"Skipping invalid JSON line: {line.strip()}")
    return None


def filter_json_data(input_json_file, search_field, search_term, output_cols):
    # Initialize a list to store filtered JSON lines
    filtered_lines = []
    # Open the input JSON file and process it line by line
    with open(input_json_file, 'r') as file:
        for line in file:
            # Process each line to see if it matches the search criteria
            filtered_line = process_json_line(line, search_field, search_term, output_cols)
            if filtered_line:
                # Append matching and filtered lines to the list
                filtered_lines.append(filtered_line)
    return filtered_lines


def write_csv_file(output_csv_file, filtered_lines, output_cols):
    try:
        # Open the output CSV file and write the filtered data to it
        with open(output_csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=output_cols)
            writer.writeheader()  # Write the header row
            writer.writerows(filtered_lines)  # Write the filtered rows
        logging.info(f"Filtered data written to {output_csv_file}")
    except Exception as e:
        # Log an error and exit if there is an issue writing to the file
        logging.error(f"An error occurred while writing to file: {e}")
        sys.exit(1)


def main(input_json_file, output_csv_file, search_field, search_term, output_cols):
    # Ensure that the search field, search term, and output columns are not empty
    if not all([search_field, search_term, output_cols]):
        logging.error("Search field, search term, and output columns cannot be empty")
        sys.exit(1)

    try:
        # Filter the JSON data based on the search criteria
        filtered_lines = filter_json_data(input_json_file, search_field, search_term, output_cols)
        if filtered_lines:
            # If matching records are found, write them to the CSV file
            write_csv_file(output_csv_file, filtered_lines, output_cols)
        else:
            # Log a warning if no matching records were found
            logging.warning("No matching records found")
    except FileNotFoundError:
        # Log an error and exit if the input JSON file does not exist
        logging.error(f"File {input_json_file} does not exist.")
        sys.exit(1)
    except ValueError as e:
        # Log an error and exit if a ValueError occurs (e.g., missing search field)
        logging.error(e)
        sys.exit(1)
    except Exception as e:
        # Log any other unexpected errors and exit
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Set up logging
    setup_logging()

    # Set up argument parsing for command-line inputs
    parser = argparse.ArgumentParser(description='Filter input JSON data and output a CSV')
    parser.add_argument('--input', required=True, help='Path to input JSON file')
    parser.add_argument('--output', required=True, help='Path to output CSV file')
    parser.add_argument('--search_field', required=True, help='Field in JSON to search')
    parser.add_argument('--search_term', required=True, help='Term in search_field to filter by')
    parser.add_argument('--output_cols', required=True,
                        help='Comma-separated list of fields from original JSON to keep')

    # Parse the arguments provided by the user
    args = parser.parse_args()

    # Convert the comma-separated output columns string into a list
    output_cols = [field.strip() for field in args.output_cols.split(',')]

    # Call the main function with the parsed arguments
    main(args.input, args.output, args.search_field, args.search_term, output_cols)
