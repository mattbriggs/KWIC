# KWIC (Keyword in Context) Script

## Overview

This Python script, developed by Matt Briggs, is designed to generate a Keyword in Context (KWIC) report from a specified text repository. It identifies unique keywords within entity extraction data and maps their occurrences across different text files, providing their context within the text. The script outputs a CSV file containing keywords, the URL/path of the text file they were found in, the line number, and the actual text line providing the context.

Version: 0.1  
Date: 2019-05-09

## Features

- Reads configuration from a JSON file to set input and output paths.
- Processes entity extraction data to identify unique keywords.
- Searches through files in the specified repository for occurrences of these keywords.
- Generates a KWIC report in CSV format detailing each occurrence's context.

## Requirements

- Python 3.6 or higher
- `common_utilities` module (Assuming this is a custom module that provides functionalities like file reading and CSV writing. Ensure this is accessible in your environment.)

## Setup

1. Ensure Python 3.6 or higher is installed on your system.
2. Place the `common_utilities.py` module in the same directory as the KWIC script, or ensure it's otherwise accessible in your Python environment.
3. Prepare a `config.json` file in the script's directory with the following structure:

```json
{
  "repoinput": "<path_to_text_repository>",
  "reportoutput": "<path_to_output_directory>/"
}
```

- `repoinput`: Directory path where your text files are located.
- `reportoutput`: Directory path where the output CSV report will be saved.

4. Ensure you have an `entity_extraction.csv` file in the output directory specified in your `config.json`, structured with at least four columns, where the fourth column contains the keywords.

## Running the Script

Execute the script from the command line:

```bash
python kwic.py
```

Upon successful execution, the script will generate a `kwic_new.csv` file in the specified output directory, containing the KWIC report.

## Output Format

The output CSV file will have the following columns:

- `word`: The keyword found in the text.
- `URL`: The path or URL of the file containing the keyword.
- `lineno`: The line number where the keyword was found.
- `line`: The text line providing context for the keyword occurrence.

## Note

This script is designed for educational and research purposes. Performance and capabilities may vary depending on the size of the text repository and the computing environment.