# LibraryApp

## Personal Library Catalogue and OPAC Web Application

LibraryApp is a Python-based web application designed to manage and explore a personal library catalogue.

The project transforms a structured Excel bibliographic database into an interactive OPAC-style (Online Public Access Catalogue) web interface, allowing users to:

* search books by title, author, ISBN and metadata;
* browse the complete catalogue;
* apply dynamic filters;
* inspect detailed bibliographic records;
* analyse catalogue quality through metadata reports.

The application has been designed with a modular architecture that separates:

* data loading;
* catalogue normalization;
* search engine logic;
* user interface;
* metadata analysis.

The result is a lightweight personal library management system built with Python, Pandas and Streamlit.

---

# Web Application

The deployed version of LibraryApp is available at:

[https://libraryapp-lp.streamlit.app/](https://libraryapp-lp.streamlit.app/)

---

# Project Overview

The application uses an Excel file containing bibliographic information about the books owned by a private library as its main data source.

The workflow is:

```
Excel Catalogue
        |
        ↓
Pandas Data Import
        |
        ↓
Data Cleaning and Normalization
        |
        ↓
Search Index Creation
        |
        ↓
Streamlit Web Interface
        |
        ↓
Interactive Catalogue
```

The Excel file acts as the main database of the application.

No external database server is required.

The catalogue can therefore be updated simply by modifying the Excel file and restarting the application.

---

# Main Features

## Bibliographic Search Engine

The search system allows users to find books through:

* title;
* author;
* ISBN;
* publisher;
* keywords;
* bibliographic metadata.

The search engine uses a fuzzy matching algorithm based on the RapidFuzz library.

The following methods are used:

* `partial_ratio`
* `token_set_ratio`

These allow the system to identify matches even with incomplete queries.

Example:

```
tolst
```

finds:

```
Lev Tolstoy
```

or:

```
galactic hitchhiker
```

finds:

```
The Hitchhiker's Guide to the Galaxy
```

---

# OPAC Catalogue Interface

The catalogue section allows users to browse all books stored in the library.

Available features:

* complete catalogue visualization;
* catalogue statistics;
* CSV export.

Each record represents a physical copy owned by the library.

---

# Dynamic Filters

The search interface includes OPAC-style filters:

* original language;
* copy language;
* author;
* publisher;
* series/collection;
* availability status.

Filters are dynamically generated from the catalogue content.

Unavailable options are automatically removed.

Each option displays the number of matching records.

Example:

```
Italian (45)
English (12)
French (7)
```

---

# Metadata Dashboard

The metadata section analyses the quality of the bibliographic catalogue.

It provides information about:

* number of records;
* number of fields;
* missing values;
* data types;
* unique values;
* completeness statistics.

This section allows monitoring of the structure and quality of the bibliographic database.

---

# Project Structure

```
LibraryApp/
│
├── .devcontainer/
│   └── devcontainer.json
│
├── requirements.txt
├── README.md
├── LICENSE_GPLv3
│
├── data/
│   └── book_catalogue.xlsx
│
├── app.py
│
└── modules/
    ├── __init__.py
    ├── config.py
    ├── loader.py
    ├── search.py
    ├── catalogue.py
    ├── metadata.py
    └── ui.py
```

---

# Application Architecture

The project follows a modular architecture.

Each module has a specific responsibility.

```
app.py
 |
 ├── loader.py
 |
 ├── search.py
 |
 ├── catalogue.py
 |
 ├── metadata.py
 |
 └── ui.py
```

The modules communicate mainly through Pandas DataFrames.

---

# File Description

## app.py

### Main application entry point

`app.py` starts the Streamlit application.

Responsibilities:

* configure the web page;
* load the catalogue;
* create the search index;
* manage navigation;
* display the main application sections.

The application contains three main sections:

```
Search

Catalogue

Metadata
```

The catalogue loading process uses Streamlit caching:

```python
@st.cache_data
def load_catalogue():
```

This prevents the Excel file from being read again every time the user interacts with the interface.

---

# modules/config.py

## Central configuration module

This file contains the mapping between:

* internal Python names;
* Excel column names.

Example:

```python
"author": "Author"
```

The application uses:

```python
COLUMNS["author"]
```

instead of directly referencing:

```python
"Author"
```

Advantages:

* avoids duplicated column names throughout the code;
* simplifies Excel structure modifications;
* keeps all modules synchronized.

The file also contains:

```python
COLUMN_DESCRIPTIONS
```

which provides descriptions of catalogue fields used by the metadata dashboard.

---

# modules/loader.py

## Catalogue Import and Normalization Engine

This module manages the transformation:

```
Excel File
     ↓
Pandas DataFrame
     ↓
Normalized Catalogue
```

Main function:

```python
load_books()
```

Operations performed:

1. Verify that the Excel file exists.
2. Import the `data` worksheet.
3. Remove empty rows.
4. Normalize column names.
5. Convert Excel values.
6. Sort catalogue records.

---

## Date Normalization

Excel stores dates internally as serial numbers.

Example:

```
46228
```

is converted into:

```
29/07/2026
```

Conversion is applied only to:

* Birth Date;
* Death Date;
* Loan Date.

Bibliographic years such as:

```
1884
1979
2020
```

remain unchanged.

---

## Cell Normalization

Multi-value fields are converted into Python lists.

Example:

```
Italian; English
```

becomes:

```python
[
 "Italian",
 "English"
]
```

This allows more accurate filtering and searching.

---

# modules/search.py

## Search Engine

This module implements the OPAC search system.

Main functions:

```python
build_search_index()
```

and:

```python
search_books()
```

---

## Search Index

For each record, the application creates:

```
_search_text
```

which contains the complete textual representation of the book:

```
title + author + keywords + publisher + notes
```

This enables searches across all metadata fields.

---

## Ranking System

Each result receives a relevance score.

Weights:

| Field            | Weight |
| ---------------- | -----: |
| Exact ISBN       |    150 |
| Partial ISBN     |    100 |
| Title            |   x1.8 |
| Author           |   x1.5 |
| Publisher        |   x0.8 |
| General metadata |   x0.5 |

Results are sorted from the highest relevance score to the lowest.

---

# modules/catalogue.py

## Catalogue Display Module

Responsible for displaying the complete catalogue.

Main functions:

```python
prepare_catalogue_view()
```

and:

```python
show_catalogue()
```

Responsibilities:

* remove internal search fields;
* convert Python lists into readable text;
* display catalogue tables;
* export CSV files.

---

# modules/metadata.py

## Metadata Analysis Module

Generates catalogue quality statistics.

Main functions:

```python
generate_metadata_report()
```

and:

```python
show_metadata()
```

The module analyses:

* missing values;
* field types;
* unique values;
* data completeness.

---

# modules/ui.py

## User Interface Module

Contains the Streamlit interface components.

Responsibilities:

* filters;
* search result display;
* book detail popup.

The detailed bibliographic record displays:

* title;
* author;
* availability;
* ISBN;
* publisher;
* edition information;
* translator;
* illustrator;
* additional contributions.

---

# modules/__init__.py

This file identifies the `modules` directory as a Python package.

It can remain empty.

Its purpose is to allow imports such as:

```python
from modules.loader import load_books
```

It does not contain application logic.

---

# data/book_catalogue.xlsx

## Bibliographic Database

The Excel file is the main data source of the application.

The worksheet used by the application is:

```
data
```

Each row represents a physical copy owned by the library.

The fields describe:

* work information;
* author information;
* edition data;
* physical characteristics;
* personal notes;
* loan management.

---

# requirements.txt

Contains all Python dependencies required by the application.

Main libraries:

| Library   | Purpose              |
| --------- | -------------------- |
| Streamlit | Web interface        |
| Pandas    | Data processing      |
| OpenPyXL  | Excel reading        |
| RapidFuzz | Fuzzy search         |
| NumPy     | Numerical operations |

Installation:

```bash
pip install -r requirements.txt
```

---

# Running Locally

Requirements:

```
Python 3.11+
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

# Development Environment

## Dev Container

The project includes:

```
.devcontainer/devcontainer.json
```

which defines a reproducible development environment.

It uses:

```
mcr.microsoft.com/devcontainers/python:1-3.11-bookworm
```

The environment automatically configures:

* Python 3.11;
* VS Code Python extension;
* Pylance;
* project dependencies;
* Streamlit.

---

# Web Deployment

The application has been deployed as a Streamlit-compatible web application.

The deployment process follows this architecture:

```
GitHub Repository
        |
        ↓
Cloud Environment
        |
        ↓
Install requirements.txt
        |
        ↓
Execute app.py
        |
        ↓
Public Web Application
```

During deployment:

1. A Python environment is created.
2. Dependencies listed in `requirements.txt` are installed.
3. `app.py` is executed.
4. The file:

```
data/book_catalogue.xlsx
```

is automatically loaded.
5. The application becomes available through a public browser URL.

The deployed application is hosted on Streamlit Community Cloud:

https://streamlit.io/cloud

---

# License

This project is distributed under:

```

GNU General Public License v3.0

```

For complete information about the project license, see:

```

LICENSE_GPLv3

```

The Python libraries, frameworks and external components used by this application are distributed under their own respective licenses.

For information about the licensing terms of each dependency, refer to the official documentation and license files provided by the individual projects.

This includes, but is not limited to:

* Streamlit
* Pandas
* RapidFuzz
* OpenPyXL
* NumPy
* all other packages listed in `requirements.txt`

The use of these external components within LibraryApp does not modify or replace their original licenses.

---

# Author

LibraryApp was developed as a personal digital library management project.

The goal is to provide a lightweight and independent OPAC-style system for private collections using open-source Python technologies.
