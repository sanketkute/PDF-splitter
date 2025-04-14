# PDF Splitter Script

A Python script to split PDF files either into chunks of a specified page size or by extracting a specific page range.

## Features

* Split large PDF files into smaller, more manageable chunks (e.g., every 1000 pages).
* Extract a specific range of pages (e.g., pages 50-150) into a new PDF file.
* Command-line interface for specifying input file, output directory, and splitting mode.
* Automatically creates the output directory if it doesn't exist.
* Handles file paths with or without quotes.

## Requirements

* Python 3.x
* PyPDF2 library

## Installation

1.  **Clone the repository (or download the script):**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```
2.  **Create a virtual environment (recommended):**
    * Using `venv`:
        ```bash
        python -m venv venv
        # On Windows
        .\venv\Scripts\activate
        # On macOS/Linux
        source venv/bin/activate
        ```
    * Using Anaconda (replace `split_PDF` with your desired name):
        ```bash
        conda create --name split_PDF python=3.x # Specify your Python version
        conda activate split_PDF
        ```
3.  **Install the required package:**
    ```bash
    pip install -r requirements.txt
    # or if using conda and pip within it
    # conda install pip # if pip is not already available
    # pip install -r requirements.txt
    # Alternatively, if PyPDF2 is available via conda channels:
    # conda install pypdf2 # Check conda channels for availability
    ```

## Usage

Run the script from your terminal (make sure your environment is activated):

```bash
python pdf_splitter_script.py # Replace with your script's filename if different
The script will prompt you for:Path to the input PDF file: Enter the full path to the PDF you want to split.Path for the output directory: Specify where the resulting PDF files should be saved. A default suggestion will be provided.Splitting mode: Choose either chunks or range.If chunks: Enter the desired number of pages per chunk file (e.g., 1000).If range: Enter the page range in the format start-end (e.g., 1232-2421).Output files will be named based on the original filename and the chunk/page range.Example(split_PDF) C:\Users\YourUser\Desktop\Projects\SplitPDF> python pdf_splitter_script.py
Enter the path to the PDF file (e.g., C:\Docs\report.pdf): C:\Docs\report.pdf
Enter the path for the output directory (e.g., C:\Docs\output_split): C:\Docs\split_output
Choose splitting mode ('chunks' or 'range'): range
Enter the page range to extract (e.g., 1232-2421): 10-25
Attempting to open PDF: C:\Docs\report.pdf
Extracting pages 10 to 25...
Saved: C:\Docs\split_output\report_Pages_10-25.pdf

PDF processing finished.
ContributingFeel free to open issues or submit pull requests if you have suggestions for