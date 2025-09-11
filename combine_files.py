import os

def combine_files_to_txt(source_folder, output_file_path):
    """
    Scans a source folder, reads the content of each file, and writes it
    to a single text file, prepending each file's content with its path.

    Args:
        source_folder (str): The path to the folder you want to scan.
        output_file_path (str): The path for the final combined text file.
    """
    # Ensure the source folder exists
    if not os.path.isdir(source_folder):
        print(f"Error: The source folder '{source_folder}' does not exist.")
        return

    try:
        # Open the output file in write mode with UTF-8 encoding
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            # Walk through the directory tree
            for dirpath, _, filenames in os.walk(source_folder):
                for filename in filenames:
                    # Construct the full file path
                    file_path = os.path.join(dirpath, filename)

                    # Avoid reading the output file itself if it's in the source folder
                    if os.path.abspath(file_path) == os.path.abspath(output_file_path):
                        continue

                    # Write the header for the current file
                    outfile.write("="*80 + "\n")
                    outfile.write(f"// FILE: {file_path}\n")
                    outfile.write("="*80 + "\n\n")

                    try:
                        # Open and read the content of the current file
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                            content = infile.read()
                            outfile.write(content)
                            outfile.write("\n\n")
                    except Exception as e:
                        # If reading fails, write an error message instead of content
                        outfile.write(f"Could not read file. Reason: {e}\n\n")

        print(f"Success! All files from '{source_folder}' have been combined into '{output_file_path}'")

    except IOError as e:
        print(f"Error writing to output file '{output_file_path}'. Reason: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # --- Configuration ---
    # 1. Set the folder you want to scan.
    #    Examples:
    #    - Windows: r"C:\Users\YourUser\Documents\MyProject"
    #    - macOS/Linux: "/home/youruser/documents/my_project"
    SOURCE_DIRECTORY = r"C:\Users\lab\Desktop\npp-web-proto\src"

    # 2. Set the name and location for the combined text file.
    #    It's best to place this outside the source directory.
    #    Examples:
    #    - Windows: r"C:\Users\YourUser\Desktop\combined_output.txt"
    #    - macOS/Linux: "/home/youruser/desktop/combined_output.txt"
    OUTPUT_FILE = r"C:\Users\lab\Desktop\npp-web-proto\ProjectSummary.txt"
    # --- End of Configuration ---

    # Check if the placeholder paths have been changed
    if SOURCE_DIRECTORY == "path/to/your/folder" or OUTPUT_FILE == "path/to/your/output_file.txt":
        print("Please update the SOURCE_DIRECTORY and OUTPUT_FILE variables in the script.")
    else:
        combine_files_to_txt(SOURCE_DIRECTORY, OUTPUT_FILE)
