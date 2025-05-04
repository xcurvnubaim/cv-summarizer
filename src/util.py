import os
import subprocess
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor
import csv

def download_file_from_drive(file_id, output_path):
    """
    Downloads a file from Google Drive using a public link and wget.
    """
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    try:
        subprocess.run(["wget", "-O", output_path, url], check=True)
    except subprocess.CalledProcessError as e:
        print(f"wget failed for file ID {file_id}: {e}")

def extract_file_id(url):
    """
    Extracts the file ID from a Google Drive URL.
    """
    parsed_url = urlparse(url)
    if "id" in parse_qs(parsed_url.query):
        return parse_qs(parsed_url.query)["id"][0]
    # Fallback for /file/d/FILE_ID/view format
    parts = parsed_url.path.split("/")
    if "file" in parts and "d" in parts:
        return parts[parts.index("d") + 1]
    return None

def download_all_cv(preprocessor_instance):
    """
    Downloads all CVs from the preprocessor instance in parallel.
    """
    def download_task(row):
        try:
            file_id = extract_file_id(row['CV ATS'])
            if not file_id:
                raise ValueError("No file ID found")
            os.makedirs("data/cv", exist_ok=True)
            filename = row['Nama'].replace("/", "_") + ".pdf"
            download_file_from_drive(file_id, f"data/cv/{filename}")
        except Exception as e:
            print(f"Error downloading CV for {row['Nama']}: {e}")

    with ThreadPoolExecutor() as executor:
        rows = [preprocessor_instance.get_row(i) for i in range(preprocessor_instance.size())]
        executor.map(download_task, rows)

def summarize_cv_to_csv(cv_summary_results: list, output_file: str):
    """
    Saves the CV summary results to a CSV file in tabular format.

    Args:
        cv_summary_results (list): A list of dictionaries containing CV summaries.
        output_file (str): The path to the output CSV file.
    """
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        # Define the column headers
        fieldnames = ["Nama", "Summary", "Top Skills", "Key Achievements", "Education"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header and rows
        writer.writeheader()
        for result in cv_summary_results:
            writer.writerow(result)

    print(f"CV summaries saved to {output_file}")

def extract_field(lines, field_name):
    """
    Extracts a specific field from the summarized content.

    Args:
        lines (list): The list of lines from the summarized content.
        field_name (str): The name of the field to extract.

    Returns:
        str: The extracted field value, or an empty string if not found.
    """
    for line in lines:
        if line.startswith(field_name):
            return line.replace(field_name, "").strip()
    return ""

def extract_csv(file_path):
    """
    Reads a CSV file and returns its content as a list of dictionaries.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of dictionaries where each dictionary represents a row in the CSV.
    """
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]
