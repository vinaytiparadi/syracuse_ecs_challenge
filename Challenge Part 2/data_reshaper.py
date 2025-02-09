import pandas as pd

# Load the original Excel file
input_file = "judge_poster_assignment_matrix.xlsx"  # Change this to your actual file path
df = pd.read_excel(input_file)

# Initialize an empty list to store the reshaped data
reshaped_data = []

# Iterate through each row in the original DataFrame
for _, row in df.iterrows():
    poster_number = int(row.iloc[0])  # First column is the Poster Number (ensure it's an integer)
    judge_columns = row.iloc[1:]  # The remaining columns are judge columns
    judges_with_1 = judge_columns[judge_columns == 1].index  # Find columns where value is 1

    for judge in judges_with_1:
        reshaped_data.append([poster_number, int(judge), 0, 0, 0, 0])  # Ensure Judge # is an integer

# Create a new DataFrame with the specified columns
reshaped_df = pd.DataFrame(reshaped_data, columns=["Poster Number", "Judge #", "Clarity", "Innovation", "Presentation", "Total"])

# --- Save the reshaped data to a CSV file ---
output_file = "reshaped_judges_data.csv"  # Specify your desired output file name (CSV)
reshaped_df.to_csv(output_file, index=False)

print(f"Reshaped data has been saved to {output_file}")