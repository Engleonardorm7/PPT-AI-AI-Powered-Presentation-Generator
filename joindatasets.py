import json
import os

def merge_json_datasets(file_paths, output_file="dataset.json"):
    """
    Merges multiple JSON datasets with the same "conversations" structure 
    into a single JSON file.

    Args:
        file_paths: A list of file paths to the JSON datasets.
        output_file: The name of the output JSON file.
    """

    all_conversations = []

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:  # Specify UTF-8 encoding
                data = json.load(f)
                if "conversations" in data and isinstance(data["conversations"], list):
                    all_conversations.extend(data["conversations"])
                else:
                  print(f"Warning: File {file_path} does not have the expected 'conversations' key or it's not a list. Skipping.")
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
            return
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in file {file_path}: {e}")
            return
        except Exception as e:
            print(f"An unexpected error occurred while reading {file_path}: {e}")
            return

    merged_data = {"conversations": all_conversations}

    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:  # Specify UTF-8 encoding
            json.dump(merged_data, outfile, indent=4, ensure_ascii=False) # indent for pretty printing, ensure_ascii for special characters
        print(f"Successfully merged datasets into {output_file}")
    except Exception as e:
        print(f"An error occurred while writing to the output file: {e}")

# Example usage:
file_paths = [
    "formatted_data_new.json",
    "formatted_data_new-2.json",
    "formatted_new_FULLex.json"
]

merge_json_datasets(file_paths)