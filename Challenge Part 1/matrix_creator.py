# matrix_creator.py
import pandas as pd
import sys

def create_poster_judge_matrix(posters_excel_path, judges_excel_path, output_excel_path):
    """Creates a binary matrix of poster-judge assignments."""
    try:
        posters_df = pd.read_excel(posters_excel_path, dtype={'Poster #': int, 'Assigned Judge 1 ID': str, 'Assigned Judge 2 ID': str}, engine='openpyxl')
        judges_df = pd.read_excel(judges_excel_path, dtype={'Judge No. #': str}, engine='openpyxl')

        required_poster_columns = ['Poster #', 'Assigned Judge 1 ID', 'Assigned Judge 2 ID']
        required_judge_columns = ['Judge No. #']
        for col in required_poster_columns:
            if col not in posters_df.columns: raise ValueError(f"Missing required column in posters file: {col}")
        for col in required_judge_columns:
            if col not in judges_df.columns: raise ValueError(f"Missing required column in judges file: {col}")

        judge_ids = sorted(judges_df['Judge No. #'].astype(str).unique(), key=lambda x: x.zfill(4))
        poster_ids = sorted(posters_df['Poster #'].unique())
        matrix = pd.DataFrame(0, index=poster_ids, columns=judge_ids, dtype=int)

        for _, row in posters_df.iterrows():
            poster_id = row['Poster #']
            judges = [str(row['Assigned Judge 1 ID']).strip(), str(row['Assigned Judge 2 ID']).strip()]
            for judge in judges:
                if judge in matrix.columns:
                    matrix.at[poster_id, judge] = 1
                else:
                    print(f"Warning: Judge {judge} not found in judges list (Poster {poster_id})")

        matrix.to_excel(output_excel_path, index_label='Poster #', engine='openpyxl')
        print(f"Successfully created matrix at {output_excel_path}")

    except Exception as e:
        print(f"Error creating matrix: {e}")
        raise # Re-raise to be caught in driver

if __name__ == '__main__':
    #Example Usage for testing
    # Replace these with your actual file paths if you want to test this script independently
    create_poster_judge_matrix("new_sample_input_abstracts.xlsx",
                             "new_example_list_judges.xlsx",
                             "judge_poster_assignment_matrix.xlsx")