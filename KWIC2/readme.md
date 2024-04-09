# KWIC (Keyword in Context) Application

## Overview

The KWIC (Keyword in Context) application, developed by Matt Briggs and marked version 1.0.0 as of June 11, 2022, is designed to process text corpora to identify and analyze the context in which keywords appear. It utilizes a series of Python modules and a SQLite database to organize, search, and analyze text data for insights into keyword centrality and context.

### Key Features

- Parses and analyzes a specified corpus of text documents.
- Creates a SQLite database to store corpus, document details, and keyword contexts.
- Calculates keyword centrality within the corpus and across documents.
- Generates views for easy retrieval of keyword contexts and entity networks.

## Installation

### Prerequisites

- Python 3.8 or higher
- `yaml` package for Python
- `SQLite3` for database creation and management

### Setup

1. Ensure all prerequisites are installed on your system.
2. Clone the repository or download the source code to your local machine.
3. Install required Python packages:

```bash
pip install pyyaml
```

python -m nltk.downloader all

Note: If `createdatabase`, `loaddatabase`, and `loadcentrality` modules are not standard Python packages, ensure they are included in your project directory or installed accordingly.

## Configuration

Before running the KWIC application, you must configure it via the `config.yaml` file. This file should specify paths for the corpus to assess and the directory to store the database:

```yaml
Corpustoassess: <path_to_corpus_directory>
Databasefolder: <path_to_database_storage_directory>
```

## Database Schema

The application relies on a SQLite database with the following schema:

- **corpus**: Stores details about the entire corpus.
- **document**: Details of individual documents within the corpus.
- **textline**: Records of each line in the documents, including sentiment analysis.
- **entity**: Identifies unique entities within the corpus and their centrality.
- **context**: Connects entities to their occurrences in text lines.
- **similarity**: Captures similarity measures between documents.
- **entity_network_view**: A view for analyzing entity networks.
- **kwic_view**: A view for easily accessing keyword in context information.

Ensure to execute the provided SQL commands to set up the database schema before running the application.

## Running the Application

To start the KWIC application, run the main script from your terminal:

```bash
python createKWIC.py
```

This script will:

1. Read configurations from `config.yaml`.
2. Create and populate the database based on the corpus specified.
3. Print progress and summaries of the data processed, including keyword centrality and document similarities.

## Output

The primary output will be:

- A SQLite database named as per the `Databasefolder` configuration, containing the processed text data, keyword contexts, and analysis results.
- Console output detailing the progress and summaries of the analysis, including keyword centrality measures.
