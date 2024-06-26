import argparse
import json

import pandas as pd


def json_to_markdown(json_file, md_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    # Extract regions data
    regions_data = data["regions"]

    # Convert regions data to DataFrame
    df = pd.DataFrame(regions_data)

    # Convert DataFrame to MD table
    md_table = df.to_markdown(index=False)

    with open(md_file, "w") as f:
        f.write(md_table)


def main():
    parser = argparse.ArgumentParser(description="Convert JSON to Markdown table.")
    parser.add_argument("--json", required=True, help="Path to the JSON file")
    parser.add_argument("--md", required=True, help="Path to the output Markdown file")

    args = parser.parse_args()

    json_to_markdown(args.json, args.md)


if __name__ == "__main__":
    main()
