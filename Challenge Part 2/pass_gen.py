import pandas as pd
import random
import shutil  # Import the shutil module for file copying

# Load the original Excel file
input_file = "judge_poster_assignment_matrix.xlsx"  # Change this to your actual file path
df = pd.read_excel(input_file)

# --- Create a CSV copy of judges_data.xlsx ---
csv_input_file = "judges_data.csv"
df.to_csv(csv_input_file, index=False)  # Save as CSV, without the index
print(f"Created a CSV copy of the input file: {csv_input_file}")


# Get the list of all judge numbers (columns from the 2nd column onward)
judge_columns = df.columns[1:]

# Generate unique 4-digit numeric passwords for each judge
judge_passwords = []
for judge in judge_columns:
    password = random.randint(1000, 9999)  # Generate a random 4-digit password
    judge_passwords.append([int(judge), password])

# Create a new DataFrame with "Judge #" and "Password"
password_df = pd.DataFrame(judge_passwords, columns=["Judge #", "Password"])

# --- Save the judge passwords to a CSV file ---
output_file = "judge_passwords.csv"  # Specify your desired output file name (CSV)
password_df.to_csv(output_file, index=False)

print(f"Judge passwords have been saved to {output_file}")