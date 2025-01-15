# Power BI Snippet Library

A Streamlit application for managing and injecting Power BI (PBI) snippets into Power BI Template (.PBIT) files.

## Overview

This application allows users to:

- Add, browse, and manage Power BI snippets (e.g., DAX, Power Query).
- Search for snippets by name or description.
- Inject selected snippets into a Power BI template file (.PBIT).

## Features

- **Snippet Management**: Add new snippets with type, name, description, and content.
- **Search Functionality**: Search for snippets by name or description.
- **Snippet Injection**: Inject selected snippets into a Power BI template file.
- **User-Friendly Interface**: Built with Streamlit for an intuitive web-based experience.

## Technologies Used

- **Python**: Backend logic and data handling.
- **Streamlit**: For building the web application.
- **Pandas**: Data manipulation for managing snippets.
- **Zipfile and OS Libraries**: For handling ZIP files and file operations.

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/powerbi-snippet-library.git
cd powerbi-snippet-library
```

### Install Dependencies

```bash
pip install streamlit pandas
```

### Run the Application

```bash
streamlit run app.py
```

## Usage

### Add a New Snippet

1. Use the sidebar to add a new snippet.
2. Select the snippet type (e.g., DAX, Power Query).
3. Enter the snippet name, description, and content.
4. Click "Add Snippet" to save it to the library.

### Browse and Search Snippets

- In the main area, search for snippets by name or description.
- Use the search bar to filter snippets.

### Inject Snippets into a PBIT File

1. Upload a Power BI template file (.PBIT).
2. Select the snippets you want to inject.
3. Click "Inject Snippets into PBIT" to modify the template.
4. Download the modified PBIT file.

## Snippet Storage

- Snippets are stored in a CSV file located at `snippets/snippets.csv`.
- The application reads from and writes to this file to manage the snippet library.

## PBIT Injection Process

1. The application extracts the contents of the uploaded PBIT file into a temporary directory.
2. It modifies the `DataModelSchema` file to inject the selected snippets.
3. The modified files are repackaged into a new PBIT file for download.

## Acknowledgments

- Built with Streamlit for rapid web application development.