# KWIC Neo4J Graph Creator

## Overview

This Python script automates the creation of a Keyword in Context (KWIC) graph using Neo4J, a graph database management system. It extracts markdown files from a specified Git repository, parses their content, and structures them into a Neo4J graph for advanced text analysis. The script emphasizes organizing documents and their textual content into a connected graph, enabling intricate analysis of keywords in context.

Date: 2021-10-13

## Features

- Clones a Git repository containing markdown files to a local directory.
- Parses markdown files to extract text and metadata.
- Creates nodes and edges in a Neo4J graph to represent documents, their metadata, and textual content.
- Utilizes custom functions for Neo4J Cypher operations to insert data efficiently.

## Requirements

- Python 3.x
- Neo4J database (local setup)
- Python packages: `os`, `json`, `uuid`, `gitpython`, `neo4j`, `mdparser`

## Setup

1. Ensure Neo4J is installed and running on your local machine. Configure it to listen on `neo4j://localhost:7687`.

2. Install the required Python packages if you haven't already:

```bash
pip install gitpython neo4j
```

(Note: The `mdparser` package should be provided with the script or installed if available.)

3. Clone or download this script to your local machine.

4. Update the `config.json` file with your Neo4J credentials (`neo_user`, `neo_pass`), the Git repository containing your markdown files (`gitrepo`), and the name of your document set (`docset`).

## Execution

Run the script from your command line:

```bash
python minimonolith.py
```

Upon execution, the script performs the following actions:

- Clones the specified Git repository to a local directory.
- Parses each markdown file within the repository, creating nodes for documents and their textual lines.
- Inserts metadata as properties of document nodes.
- Connects document nodes to their respective text lines with edges, constructing a comprehensive graph in Neo4J.

## Neo4J Graph Structure

The script generates a graph with the following structure:

- **Docset Node**: Represents the set of documents being analyzed.
- **Article Nodes**: Represent individual documents, containing metadata such as path and summary.
- **Line Nodes**: Represent individual lines of text within documents.
- **Edges**: Connect documents to their text lines and the docset node, indicating relationships.

## Output

The script populates your Neo4J database with nodes and relationships representing the structure and content of the markdown files in the specified Git repository. This graph can then be queried using Cypher to analyze keywords in the context of their documents and the entire corpus.

# Markdown Parser Module

## Overview

This module provides a set of classes for parsing markdown files. It includes a container class (`MDPage`) for holding page data and a parsing class (`MDParser`) that processes markdown files to return structured data and HTML content.

## Features

- **MDPage**: A simple container class for holding the metadata, raw text, and HTML-converted content of a markdown file.
- **MDParser**: A comprehensive parser that:
  - Reads and stores the raw content of markdown files.
  - Splits the content into metadata and body.
  - Cleans and processes metadata into key-value pairs.
  - Converts markdown body text into HTML.

## Installation

This module requires Python 3.x and the `markdown` package. Ensure you have Python installed on your system and then install the markdown package using pip:

```bash
pip install markdown
```

The module also depends on a custom utility module (`mod_utilities`). Ensure that this module is available in your project or adjust the import statements according to your project structure.

## Usage

### MDPage Class

Instantiate an `MDPage` object to hold markdown file data:

```python
page = MDPage()
```

### MDParser Class

1. **Initialize the Parser**:
   
   ```python
   parser = MDParser()
   ```

2. **Load and Get Raw Body**:
   
   Load a markdown file and get its raw content:

   ```python
   raw_content = parser.get_raw_body("path/to/markdown.md")
   ```

3. **Process Metadata**:
   
   Extract and process metadata from the loaded markdown file:

   ```python
   metadata = parser.process_meta()
   ```

4. **Process Body**:
   
   Convert the body of the markdown file into HTML:

   ```python
   html_content = parser.process_body()
   ```

## Example

```python
from markdown_parser import MDParser

parser = MDParser()
parser.get_raw_body("example.md")
metadata = parser.process_meta()
html = parser.process_body()

print(metadata)
print(html)
```

Replace `"example.md"` with the path to your markdown file. This example demonstrates how to use the `MDParser` to extract metadata and convert the markdown body to HTML.