# Assemble Readings from Your Zotero Library

## Overview

This script automates the process of fetching and organizing PDFs based on citations in a Markdown syllabus. It uses a Zotero Better BibTeX JSON export to map citation keys to Zotero items and either copies the PDFs from local storage or downloads them using the Zotero API. The script is designed to handle errors gracefully, providing detailed logs of missing citation keys and failed PDF downloads.

## Features

- **Automatic PDF Fetching**: Automatically fetches PDFs for each citation in your syllabus.
- **Flexible Source Handling**: Copies PDFs from local Zotero storage if available; otherwise, it downloads them from Zotero.
- **Error Reporting**: Logs missing citation keys and failed PDF downloads separately.
- **Session-Based Organization**: Organizes PDFs by session, based on the structure of your Markdown syllabus.

## Getting Started

### Prerequisites

1. **Zotero with Better BibTeX**: Ensure that you have Zotero installed and the Better BibTeX plugin configured.
2. **Python**: Make sure you have Python 3.x installed on your system.
3. **Python Packages**: You'll need the following Python packages:
   - `python-dotenv`
   - `pyzotero`

   You can install them using `pip`:

   ```bash
   pip install python-dotenv pyzotero
   ```

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/zotero-pdf-fetcher.git
   cd zotero-pdf-fetcher
   ```

2. **Create a `.env` File**

   In the root directory of the project, create a `.env` file with the following content:

   ```env
   ZOTERO_LIBRARY_ID=your_zotero_library_id
   ZOTERO_API_KEY=your_zotero_api_key
   ZOTERO_JSON_PATH=/path/to/your/zotero.json
   ```

   - **ZOTERO_LIBRARY_ID**: Your Zotero library ID. You can find this in your Zotero web library URL (e.g., `https://www.zotero.org/users/1234567/library` where `1234567` is your library ID).
   - **ZOTERO_API_KEY**: Generate an API key from Zotero by following the instructions [here](https://www.zotero.org/settings/keys/new).
   - **ZOTERO_JSON_PATH**: The path to your exported Zotero Better BibTeX JSON file.

3. **Export Your Zotero Library**

   Export your Zotero library in Better BibTeX JSON format by following these steps:

   - Open Zotero.
   - Right-click your library and select `Export Library`.
   - Choose `Better BibTeX JSON` as the export format.
   - Save the exported JSON file to a location specified in your `.env` file.

### Running the Script

Once your environment is set up, you can run the script as follows:

```bash
python script_name.py syllabus.md /path/to/output/dir --missing-keys-output=missing_keys.txt --failed-downloads-output=failed_downloads.txt
```

- **syllabus.md**: The path to your Markdown syllabus file.
- **/path/to/output/dir**: The directory where you want to save the PDFs.
- **--missing-keys-output**: Optional. Specify the file to save missing citation keys (default: `missing_citation_keys.txt`).
- **--failed-downloads-output**: Optional. Specify the file to save failed PDF downloads (default: `failed_downloads.txt`).

### Error Handling and Limitations

- **Session Labeling**: The script is designed to work with a specific format for session headers (e.g., `## Session 1 (9/24):`). If you change the session labeling, the script may not work as expected.
- **No Warranties**: This script is provided "as is" without any warranty. It may require modifications to work in different environments or with different session labeling formats.

## Contributing

Feel free to fork the repository, submit issues, or create pull requests. Contributions are always welcome!

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.



