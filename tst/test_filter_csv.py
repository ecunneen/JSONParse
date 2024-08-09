import unittest
import json
import os
import csv
from unittest.mock import patch, mock_open
import filter_csv  # Assuming this is the correct module name

class TestMainFunction(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = "test_files"
        os.makedirs(self.test_dir, exist_ok=True)

        # Create input and output file paths
        self.input_json_file = os.path.join(self.test_dir, "input.json")
        self.output_csv_file = os.path.join(self.test_dir, "output.csv")

    def tearDown(self):
        # Remove all files within the temporary directory
        for filename in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, filename)
            os.remove(file_path)

        # Remove the temporary directory
        os.rmdir(self.test_dir)

    def test_main_function_with_valid_input(self):
        # Create sample input JSON data
        input_data = [
            {"externalId": 10001, "firstName": "Homer", "lastName": "Simpson", "middleName": "Jay", "graduationYear": 2020, "languages": ["Python", "C++", "R"], "locationCity": "Phoenix", "locationCountry": "United States", "locationState": "Arizona", "preferredLanguage": "English", "personalWebsite": False, "yearsExperience" : 5},
            {"externalId": 10002, "firstName": "John", "lastName": "Smith", "middleName": "Jingleheimer", "graduationYear": 2021, "languages": ["Java"], "locationCity": "Atlanta", "locationCountry": "United States", "locationState": "Georgia", "preferredLanguage": "Spanish", "personalWebsite": True, "yearsExperience": 4},
            {"externalId": 10003, "firstName": "Dave", "lastName": "Grohl", "middleName": None, "graduationYear": 2000, "languages": ["MATLAB", "Maleboge"], "locationCity": "Seattle", "locationCountry": "United States", "locationState": "Washington", "preferredLanguage": "English", "personalWebsite": True, "yearsExperience" : 20}
        ]

        # Write the input JSON data to a file
        with open(self.input_json_file, 'w') as f:
            for entry in input_data:
                json.dump(entry, f)
                f.write('\n')

        # Call the main function with the input and output file paths
        filter_csv.main(self.input_json_file, self.output_csv_file, "languages", "Python",
                        ["externalId","firstName","lastName","middleName"])

        # Read the output CSV file
        output_data = []
        with open(self.output_csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                output_data.append(row)

        # Expected output data after filtering
        expected_output_data = [
            {"externalId": "10001", "firstName": "Homer", "lastName": "Simpson", "middleName": "Jay"},
        ]

        # Assert that the output data matches the expected output data
        self.assertEqual(output_data, expected_output_data)

    def test_main_function_with_empty_inputs(self):
        # Create sample input JSON data
        input_data = [
            {"externalId": "", "firstName": "", "lastName": "", "middleName": "", "graduationYear": "", "languages": ["Python"],
             "city": "", "country": "", "state": "", "preferredLanguage": "",
             "personalWebsite": "", "yearsExperience" : ""}
        ]

        # Write the input JSON data to a file
        with open(self.input_json_file, 'w') as f:
            for entry in input_data:
                json.dump(entry, f)
                f.write('\n')

        # Call the main function with the input and output file paths
        filter_csv.main(self.input_json_file, self.output_csv_file, "languages", "Python",
                        ["externalId", "firstName", "lastName", "middleName", "graduationYear", "languages",
             "city", "country", "state", "preferredLanguage",
             "personalWebsite", "yearsExperience"])

        # Read the output CSV file
        output_data = []
        with open(self.output_csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                output_data.append(row)

        # Expected output data after filtering
        expected_output_data = [
            {"externalId": "", "firstName": "", "lastName": "", "middleName": "", "graduationYear": "", "languages": "['Python']",
             "city": "", "country": "", "state": "", "preferredLanguage": "",
             "personalWebsite": "", "yearsExperience": ""}
        ]


            # Assert that the output data matches the expected output data
        self.assertEqual(output_data, expected_output_data)

    def test_case_insensitivity_of_search_term(self):
        # Create sample input JSON data
        input_data = [
            {"externalId": 10001, "firstName": "Homer", "lastName": "Simpson", "middleName": "Jay", "languages": ["python", "C++", "R"]}
        ]

        # Write the input JSON data to a file
        with open(self.input_json_file, 'w') as f:
            for entry in input_data:
                json.dump(entry, f)
                f.write('\n')

        # Call the main function with a different case search term
        filter_csv.main(self.input_json_file, self.output_csv_file, "languages", "Python",
                        ["externalId", "firstName", "lastName", "middleName"])

        # Read the output CSV file
        output_data = []
        with open(self.output_csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                output_data.append(row)

        # Expected output data after filtering
        expected_output_data = [
            {"externalId": "10001", "firstName": "Homer", "lastName": "Simpson", "middleName": "Jay"},
        ]

        # Assert that the output data matches the expected output data
        self.assertEqual(output_data, expected_output_data)

    def test_partial_match_in_search_term(self):
        # Create sample input JSON data
        input_data = [
            {"externalId": 10001, "firstName": "Homer", "lastName": "Simpson", "middleName": "Jay", "languages": ["Pythony", "C++", "R"]}
        ]

        # Write the input JSON data to a file
        with open(self.input_json_file, 'w') as f:
            for entry in input_data:
                json.dump(entry, f)
                f.write('\n')

        # Call the main function with a partial search term
        filter_csv.main(self.input_json_file, self.output_csv_file, "languages", "Python",
                        ["externalId", "firstName", "lastName", "middleName"])

        # Read the output CSV file
        output_data = []
        with open(self.output_csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                output_data.append(row)

        # Expected output data after filtering
        expected_output_data = [
            {"externalId": "10001", "firstName": "Homer", "lastName": "Simpson", "middleName": "Jay"},
        ]

        # Assert that the output data matches the expected output data
        self.assertEqual(output_data, expected_output_data)

    def test_special_characters_in_search_term(self):
        # Create sample input JSON data
        input_data = [
            {"externalId": 10001, "firstName": "Special", "lastName": "Character", "middleName": "@#", "languages": ["@Python@", "C++", "R"]}
        ]

        # Write the input JSON data to a file
        with open(self.input_json_file, 'w') as f:
            for entry in input_data:
                json.dump(entry, f)
                f.write('\n')

        # Call the main function with special characters in the search term
        filter_csv.main(self.input_json_file, self.output_csv_file, "languages", "@Python@",
                        ["externalId", "firstName", "lastName", "middleName"])

        # Read the output CSV file
        output_data = []
        with open(self.output_csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                output_data.append(row)

        # Expected output data after filtering
        expected_output_data = [
            {"externalId": "10001", "firstName": "Special", "lastName": "Character", "middleName": "@#"},
        ]

        # Assert that the output data matches the expected output data
        self.assertEqual(output_data, expected_output_data)

    def test_multiple_matching_records(self):
        # Create sample input JSON data
        input_data = [
            {"externalId": 10001, "firstName": "Homer", "lastName": "Simpson", "middleName": "Jay", "languages": ["Python", "C++", "R"]},
            {"externalId": 10002, "firstName": "John", "lastName": "Doe", "middleName": "A", "languages": ["Python", "Java"]},
        ]

        # Write the input JSON data to a file
        with open(self.input_json_file, 'w') as f:
            for entry in input_data:
                json.dump(entry, f)
                f.write('\n')

        # Call the main function with the input and output file paths
        filter_csv.main(self.input_json_file, self.output_csv_file, "languages", "Python",
                        ["externalId", "firstName", "lastName", "middleName"])

        # Read the output CSV file
        output_data = []
        with open(self.output_csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                output_data.append(row)

        # Expected output data after filtering
        expected_output_data = [
            {"externalId": "10001", "firstName": "Homer", "lastName": "Simpson", "middleName": "Jay"},
            {"externalId": "10002", "firstName": "John", "lastName": "Doe", "middleName": "A"},
        ]

        # Assert that the output data matches the expected output data
        self.assertEqual(output_data, expected_output_data)

    def test_missing_fields_in_output_columns(self):
        # Create sample input JSON data
        input_data = [
            {"externalId": 10001, "firstName": "Homer", "languages": ["Python", "C++", "R"]}
        ]

        # Write the input JSON data to a file
        with open(self.input_json_file, 'w') as f:
            for entry in input_data:
                json.dump(entry, f)
                f.write('\n')

        # Call the main function with an output column that doesn't exist in the JSON
        filter_csv.main(self.input_json_file, self.output_csv_file, "languages", "Python",
                        ["externalId", "firstName", "lastName", "middleName"])

        # Read the output CSV file
        output_data = []
        with open(self.output_csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                output_data.append(row)

        # Expected output data after filtering
        expected_output_data = [
            {"externalId": "10001", "firstName": "Homer", "lastName": "", "middleName": ""},
        ]

        # Assert that the output data matches the expected output data
        self.assertEqual(output_data, expected_output_data)

    def test_null_value_handling(self):
        # Create sample input JSON data
        input_data = [
            {"externalId": 10001, "firstName": "Homer", "lastName": "Simpson", "middleName": None, "languages": ["Python", "C++", "R"]}
        ]

        # Write the input JSON data to a file
        with open(self.input_json_file, 'w') as f:
            for entry in input_data:
                json.dump(entry, f)
                f.write('\n')

        # Call the main function with the input and output file paths
        filter_csv.main(self.input_json_file, self.output_csv_file, "languages", "Python",
                        ["externalId", "firstName", "lastName", "middleName"])

        # Read the output CSV file
        output_data = []
        with open(self.output_csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                output_data.append(row)

        # Expected output data after filtering
        expected_output_data = [
            {"externalId": "10001", "firstName": "Homer", "lastName": "Simpson", "middleName": ""},
        ]

        # Assert that the output data matches the expected output data
        self.assertEqual(output_data, expected_output_data)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_main_function_with_missing_input_file(self, mock_open):
        with self.assertRaises(SystemExit) as cm:
            filter_csv.main("nonexistent_file.json", self.output_csv_file, "languages",
                            "Python", ["externalID"])
        self.assertEqual(cm.exception.code, 1)

    @patch("builtins.open", side_effect=Exception("Error reading file"))
    def test_main_function_with_error_reading_input_file(self, mock_open):
        with self.assertRaises(SystemExit) as cm:
            filter_csv.main(self.input_json_file, self.output_csv_file, "languages",
                            "Python", ["externalID"])
        self.assertEqual(cm.exception.code, 1)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_main_function_with_empty_search_field(self, mock_open):
        with self.assertRaises(SystemExit) as cm:
            filter_csv.main("nonexistent_file.json", self.output_csv_file, "",
                            "Python", ["externalID"])
        self.assertEqual(cm.exception.code, 1)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_main_function_with_empty_search_term(self, mock_open):
        with self.assertRaises(SystemExit) as cm:
            filter_csv.main("nonexistent_file.json", self.output_csv_file, "languages",
                            "", ["externalID"])
        self.assertEqual(cm.exception.code, 1)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_main_function_with_invalid_output_cols(self, mock_open):
        with self.assertRaises(SystemExit) as cm:
            filter_csv.main("nonexistent_file.json", self.output_csv_file, "languages",
                            "Python", "")
        self.assertEqual(cm.exception.code, 1)

if __name__ == "__main__":
    unittest.main()
