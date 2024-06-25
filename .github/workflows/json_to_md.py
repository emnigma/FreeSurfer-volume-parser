import argparse
import json

def json_to_markdown(json_file, md_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    md_table = "| Name | Volume (mm^3) |\n"
    md_table += "|------|--------------|\n"

    for entry in data:
        name = entry['name']
        volume = entry['volume']
        md_table += f"| {name} | {volume:.1f} |\n"

    with open(md_file, 'w') as f:
        f.write(md_table)

def main():
    parser = argparse.ArgumentParser(description='Convert JSON to Markdown table.')
    parser.add_argument('--json', required=True, help='Path to the JSON file')
    parser.add_argument('--md', required=True, help='Path to the output Markdown file')

    args = parser.parse_args()
    
    json_to_markdown(args.json, args.md)

if __name__ == "__main__":
    main()
