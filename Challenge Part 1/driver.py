# driver.py

import os
import sys
from scraper import scrape_and_save_professors  # Import the scraping function
from matcher import perform_matching  # Import the matching function
from matrix_creator import create_poster_judge_matrix  # Import matrix creation

def main():
    """Main driver function."""

    # --- File Paths ---
    professors_file = 'professors.xlsx'
    input_posters_file = 'Sample_input_abstracts.xlsx'
    input_judges_file = 'Example_list_judges.xlsx'
    output_posters_file = 'processed_Sample_input_abstracts.xlsx'
    output_judges_file = 'processed_Example_list_judges.xlsx'
    output_matrix_file = 'judge_poster_assignment_matrix.xlsx'

    # --- Step 1: Scrape if professors.xlsx is missing ---
    if not os.path.exists(professors_file):
        print("professors.xlsx not found. Starting web scraping...")
        try:
            scrape_and_save_professors(professors_file)
        except Exception as e:
            print(f"Error during scraping: {e}")
            sys.exit(1)  # Exit on scraping failure
    else:
        print("professors.xlsx found. Skipping scraping.")

    # --- Step 2: Perform Matching ---
    try:
        perform_matching(input_posters_file, input_judges_file, professors_file, output_posters_file, output_judges_file)
    except Exception as e:
        print(f"Error during matching: {e}")
        sys.exit(1)

    # --- Step 3: Create Matrix ---
    try:
        create_poster_judge_matrix(output_posters_file, output_judges_file, output_matrix_file)
    except Exception as e:
        print(f"Error during matrix creation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()