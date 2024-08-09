markdown

# JSON Filter to CSV Converter

This Python application filters JSON data based on specified search criteria and outputs the filtered data as a CSV file. The application is designed to handle large JSON files by processing each line individually, making it efficient for a variety of use cases.

## Features

- **Search Filtering**: Filters JSON lines based on a search term in a specified field.
- **Null Value Handling**: Removes or retains null values based on user-specified columns.
- **Error Handling**: Handles common errors such as invalid JSON lines, missing files, and incorrect search fields gracefully.
- **Logging**: Provides informative logging to help with debugging and tracking the application's progress.

## Prerequisites

- Python 3.x
- No additional packages required beyond the Python standard library.

## Installation

Clone the repository or download the script:

```bash
git clone https://github.com/yourusername/json-filter-csv.git
cd json-filter-csv

Ensure you have Python 3 installed on your system. You can verify this by running:

bash

python --version

Usage

The application is run from the command line. Below is the general syntax:

bash

python json_filter.py --input <input_json_file> --output <output_csv_file> --search_field <search_field> --search_term <search_term> --output_cols <output_columns>

Arguments

    --input: Path to the input JSON file (required).
    --output: Path to the output CSV file (required).
    --search_field: The JSON field to search within (required).
    --search_term: The term to search for in the specified field (required).
    --output_cols: Comma-separated list of fields from the JSON to include in the CSV output (required).

Example

Suppose you have a JSON file data.json containing data records, and you want to filter records that have "Python" in their languages field and output their externalId, firstName, and lastName to filtered_data.csv.

You would run:

bash

python json_filter.py --input data.json --output filtered_data.csv --search_field languages --search_term Python --output_cols externalId,firstName,lastName

Logging

The application logs its operations to the console. You will see information about the number of filtered records and any errors that occur during processing.
Error Handling

    FileNotFoundError: The application will exit with an error message if the input file is not found.
    ValueError: If the specified search field is not present in the JSON data, the application will exit with a message indicating the issue.
    Invalid JSON: Lines with invalid JSON will be skipped, and a warning will be logged.

License

This project is licensed under the MIT License - see the LICENSE file for details.
Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Contact

For any issues or questions, please feel free to contact Edward Cunneen.
Code Overview
Python Script

The core functionality is implemented in json_filter.py. Below is a summary of the key functions and their responsibilities:

    setup_logging(): Configures logging for the application.

    remove_null_values(line, output_cols): Filters out null, empty, or "null" string values from the specified columns.

    validate_search_field(data, search_field): Ensures the specified search field exists in the JSON data.

    process_json_line(line, search_field, search_term, output_cols): Processes each JSON line to check if it matches the search criteria and filters it based on the output columns.

    filter_json_data(input_json_file, search_field, search_term, output_cols): Reads the input JSON file line by line and applies the filtering logic.

    write_csv_file(output_csv_file, filtered_lines, output_cols): Writes the filtered data to the specified CSV file.

    main(input_json_file, output_csv_file, search_field, search_term, output_cols): Orchestrates the overall filtering process, handling errors and managing the flow of data.

How to Run

You can run the script directly from the command line with the necessary arguments. For example:

```bash

python json_filter.py --input data.json --output filtered_data.csv --search_field languages --search_term Python --output_cols externalId,firstName,lastName

The application will process the JSON file, filter the data based on your criteria, and output the results in the specified CSV file.