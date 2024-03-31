# KWIC: Keyword in Context Application

## About KWIC

Keyword in Context (KWIC) is a software application designed to index and search texts by keywords. This Python implementation allows users to easily input text and retrieve all occurrences of a specific keyword, along with the words surrounding it, providing valuable context. This tool is particularly useful for researchers, students, and anyone interested in text analysis.

### History of KWIC

The concept of Keyword in Context has its roots in the early days of information retrieval. Initially developed in the 1950s and 1960s, KWIC was a groundbreaking approach to indexing and searching text. It was popularized by Hans Peter Luhn, a pioneering figure in information retrieval at IBM. KWIC indexes were originally used in library science and linguistics for cataloging and search purposes, allowing users to find a word within its original textual context. This method greatly enhanced the ability to retrieve information from large texts or databases.

Over the years, KWIC has evolved with advancements in computing, from manual systems to sophisticated digital software. The KWIC system implemented in this repository is a modern adaptation, leveraging Python to offer a user-friendly and efficient way to explore text data.

### Versions of the app

| Version | Summary |
|---------|---------|
| [KWIC v0.1 (2019)](KWIC1/readme.md) | Initial version using JSON for config and CSV for data processing; focuses on basic keyword context extraction. |
| [KWIC v1.0.0 (2022)](KWIC2/readme.md) | Advanced version with YAML config, SQLite database integration, and enhanced keyword centrality and context analysis. |
| [KWIC graph (2021.10.13)](graph/minimonolith.py) | The Graph KWIC app uses Neo4J to analyze keywords in documents, creating a detailed text analysis and visualization tool. |


## Contributing

Contributions to the KWIC project are welcome. Please refer to the CONTRIBUTING.md file for guidelines on how to contribute.

## License

This KWIC application is released under the MIT License. See the LICENSE file for more details.