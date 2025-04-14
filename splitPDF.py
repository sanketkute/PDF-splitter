import PyPDF2
import os
import math
import re # Import regular expressions for range parsing

def extract_page_range(pdf_path, output_dir, start_page, end_page):
    """
    Extracts a specific range of pages from a PDF file and saves it as a new PDF.

    Args:
        pdf_path (str): The path to the PDF file.
        output_dir (str): The directory where the extracted PDF will be saved.
        start_page (int): The starting page number (1-based).
        end_page (int): The ending page number (1-based).
    """
    # Check if the output directory exists, create it if it doesn't
    if not os.path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)

    # Extract the base name of the PDF file without the extension
    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    output_filename = os.path.join(
        output_dir,
        f'{base_filename}_Pages_{start_page}-{end_page}.pdf'
    )

    try:
        # Open the PDF file in read binary mode
        print(f"Attempting to open PDF: {pdf_path}")
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            total_pages = len(pdf_reader.pages)

            # --- Input Validation ---
            if not (1 <= start_page <= total_pages and 1 <= end_page <= total_pages):
                 print(f"Error: Page range ({start_page}-{end_page}) is invalid for a PDF with {total_pages} pages.")
                 return
            if start_page > end_page:
                print(f"Error: Start page ({start_page}) cannot be greater than end page ({end_page}).")
                return

            pdf_writer = PyPDF2.PdfWriter()

            print(f"Extracting pages {start_page} to {end_page}...")
            # Adjust for 0-based indexing used by PyPDF2
            for page_num in range(start_page - 1, end_page):
                try:
                    page = pdf_reader.pages[page_num]
                    pdf_writer.add_page(page)
                except Exception as page_error:
                    print(f"  Warning: Could not add page {page_num + 1}. Error: {page_error}")

            # Check if any pages were actually added
            if len(pdf_writer.pages) > 0:
                # Write the extracted range to a new PDF file
                try:
                    with open(output_filename, 'wb') as output_file:
                        pdf_writer.write(output_file)
                    print(f'Saved: {output_filename}')
                except Exception as write_error:
                    print(f"Error writing file {output_filename}: {write_error}")
            else:
                print("Could not extract any pages in the specified range.")


    except FileNotFoundError:
        print(f"Error: File not found at '{pdf_path}'. Please ensure the path is correct.")
    except PyPDF2.errors.PdfReadError as pdf_error:
         print(f"Error reading PDF file '{pdf_path}'. It might be corrupted or password-protected. Error: {pdf_error}")
    except PermissionError:
        print(f"Error: Permission denied when trying to access '{pdf_path}' or write to '{output_dir}'.")
    except OSError as os_err:
        print(f"An OS error occurred: {os_err}")
    except Exception as e:
        import traceback
        print(f"An unexpected error occurred: {e}")
        print(traceback.format_exc())

def split_pdf_into_chunks(pdf_path, output_dir, chunk_size=1000):
    """
    Splits a PDF file into chunks of a specified number of pages and saves
    each chunk as a separate PDF. (Function remains largely the same as before)

    Args:
        pdf_path (str): The path to the PDF file to be split.
        output_dir (str): The directory where the chunked PDFs will be saved.
        chunk_size (int): The maximum number of pages per output PDF file.
    """
    # Check if the output directory exists, create it if it doesn't
    if not os.path.exists(output_dir):
        print(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)

    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]

    try:
        print(f"Attempting to open PDF: {pdf_path}")
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            total_pages = len(pdf_reader.pages)

            if total_pages == 0:
                print(f"Warning: The PDF file '{pdf_path}' has 0 pages.")
                return
            if chunk_size <= 0:
                print("Error: Chunk size must be a positive integer.")
                return

            num_chunks = math.ceil(total_pages / chunk_size)
            print(f"Total pages: {total_pages}")
            print(f"Chunk size: {chunk_size}")
            print(f"Number of chunks: {num_chunks}")

            for i in range(num_chunks):
                start_page_idx = i * chunk_size
                end_page_idx = min((i + 1) * chunk_size, total_pages)
                pdf_writer = PyPDF2.PdfWriter()

                print(f"Processing chunk {i+1}/{num_chunks} (Pages {start_page_idx + 1} to {end_page_idx})...")
                for page_num in range(start_page_idx, end_page_idx):
                    try:
                        page = pdf_reader.pages[page_num]
                        pdf_writer.add_page(page)
                    except Exception as page_error:
                        print(f"  Warning: Could not add page {page_num + 1}. Error: {page_error}")

                if len(pdf_writer.pages) > 0:
                    output_filename = os.path.join(
                        output_dir,
                        f'{base_filename}_{start_page_idx + 1}-{end_page_idx}.pdf'
                    )
                    try:
                        with open(output_filename, 'wb') as output_file:
                            pdf_writer.write(output_file)
                        print(f'Saved: {output_filename}')
                    except Exception as write_error:
                        print(f"Error writing file {output_filename}: {write_error}")
                else:
                     print(f"Skipping chunk {i+1} as no pages could be added.")

    except FileNotFoundError:
        print(f"Error: File not found at '{pdf_path}'.")
    except PyPDF2.errors.PdfReadError as pdf_error:
         print(f"Error reading PDF file '{pdf_path}'. Error: {pdf_error}")
    except PermissionError:
        print(f"Error: Permission denied accessing '{pdf_path}' or writing to '{output_dir}'.")
    except OSError as os_err:
        print(f"An OS error occurred: {os_err}")
    except Exception as e:
        import traceback
        print(f"An unexpected error occurred: {e}")
        print(traceback.format_exc())


if __name__ == "__main__":
    # --- Get PDF Path ---
    default_pdf_path = r"C:\Users\kute\Downloads\Plant Simulation Documentation\Plant Simulation Help.pdf"
    pdf_file_path_input = input(f"Enter the path to the PDF file (e.g., {default_pdf_path}): ") or default_pdf_path
    pdf_file_path = pdf_file_path_input.strip().strip('"\'')

    # --- Get Output Directory ---
    default_output_dir = os.path.join(os.path.dirname(pdf_file_path) if os.path.dirname(pdf_file_path) else '.', "output_split")
    output_directory_input = input(f"Enter the path for the output directory (e.g., {default_output_dir}): ") or default_output_dir
    output_directory = output_directory_input.strip().strip('"\'')

    # --- Choose Mode ---
    while True:
        mode = input("Choose splitting mode ('chunks' or 'range'): ").lower().strip()
        if mode in ['chunks', 'range']:
            break
        else:
            print("Invalid mode. Please enter 'chunks' or 'range'.")

    # --- Execute Based on Mode ---
    if mode == 'chunks':
        # Get chunk size
        while True:
            try:
                chunk_input = input("Enter the number of pages per chunk file (e.g., 1000): ")
                chunk_size = int(chunk_input) if chunk_input else 1000 # Default to 1000
                if chunk_size > 0:
                    break
                else:
                    print("Chunk size must be a positive integer.")
            except ValueError:
                print("Invalid input. Please enter an integer.")
        # Call chunk splitting function
        split_pdf_into_chunks(pdf_file_path, output_directory, chunk_size)

    elif mode == 'range':
        # Get page range
        while True:
            try:
                range_input = input("Enter the page range to extract (e.g., 1232-2421): ").strip()
                # Use regex to find numbers separated by a hyphen
                match = re.match(r'^\s*(\d+)\s*-\s*(\d+)\s*$', range_input)
                if match:
                    start_page = int(match.group(1))
                    end_page = int(match.group(2))
                    if start_page > 0 and end_page > 0: # Basic check, more validation in function
                         break
                    else:
                         print("Page numbers must be positive.")
                else:
                    print("Invalid format. Please use 'start-end' (e.g., 10-25).")
            except ValueError:
                print("Invalid input. Please enter numbers for the range.")
            except Exception as e:
                 print(f"An error occurred parsing range: {e}")

        # Call range extraction function
        extract_page_range(pdf_file_path, output_directory, start_page, end_page)

    print("\nPDF processing finished.")
