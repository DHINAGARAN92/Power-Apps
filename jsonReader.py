import os
import json

# Correct directory path using raw string
json_directory = r"C:\Users\Admin\Desktop\Power Fx\New folder\DhinaTestSolution_1_0_0_8_managed\Workflows"

# Text to search for
search_text = "218ad2e3-1b07-44b8-a8ab-80a5171788d3"

# List to store files where the text is found
files_with_text = []

# Loop through all JSON files in the directory
for filename in os.listdir(json_directory):
    if filename.endswith(".json"):  # Ensure we only check JSON files
        file_path = os.path.join(json_directory, filename)  # Correctly indented
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = json.load(file)  # Load JSON content
                json_str = json.dumps(content)  # Convert JSON to string for searching
                if search_text in json_str:
                    files_with_text.append(filename)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

# Output results
if files_with_text:
    print("Text found in the following JSON files:")
    for file in files_with_text:
        print(file)
else:
    print("Text not found in any JSON file.")
