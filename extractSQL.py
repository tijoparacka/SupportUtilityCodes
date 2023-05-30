import json
import argparse

def extract_sql_queries(input_file, output_file):
    # Open the log file
    with open(input_file, 'r') as file, open(output_file, 'w') as outfile:
        # Read each line in the file
        for line in file:
            # Split the line by tab characters and get the last two parts
            json_parts = line.split("\t")[-2:]

            for json_part in json_parts:
                # Parse the JSON
                try:
                    log_json = json.loads(json_part)
                    # Check for the 'query' key in the JSON
                    if 'query' in log_json:
                        # Replace newline characters in the SQL query with a space
                        single_line_query = log_json['query'].replace('\n', ' ')
                        # Write the single line SQL query to the output file
                        # if "INFORMATION_SCHEMA" and "sys" are not in the query
                        if "INFORMATION_SCHEMA" not in single_line_query and "sys" not in single_line_query:
                            outfile.write(single_line_query + '\n')
                except json.JSONDecodeError:
                    continue

def main():
    parser = argparse.ArgumentParser(description='Extract SQL queries from a Druid broker log.')
    parser.add_argument('input_file', type=str, help='The input log file.')
    parser.add_argument('output_file', type=str, help='The output file where extracted queries will be written.')
    args = parser.parse_args()

    extract_sql_queries(args.input_file, args.output_file)

if __name__ == '__main__':
    main()

