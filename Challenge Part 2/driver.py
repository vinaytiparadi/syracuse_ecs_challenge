import os
import subprocess
import signal
import pandas as pd
import time

def check_file_exists(filepath):
    """Checks if a file exists."""
    return os.path.exists(filepath)

def run_script(script_path):
    """Runs a Python script."""
    subprocess.run(['python', script_path])

def run_flask_app(script_path):
    """Runs the Flask app and handles graceful shutdown."""
    process = subprocess.Popen(['python', script_path])

    try:
        while True:  # Keep the driver script running while the app is up
            time.sleep(1)  # Check periodically, without busy-waiting
    except KeyboardInterrupt:
        print("\nCtrl+C detected.  Shutting down gracefully...")
        # Convert reshaped_judges_data.csv to xlsx
        try:
            df = pd.read_csv("reshaped_judges_data.csv")
            df.to_excel("output_for_part3.xlsx", index=False)
            print("Converted reshaped_judges_data.csv to reshaped_judges_data.xlsx")
        except FileNotFoundError:
            print("reshaped_judges_data.csv not found, could not convert to .xlsx")
        except Exception as e:
            print(f"Error during conversion: {e}")
            
        # Terminate the Flask app process.  Send SIGINT (like Ctrl+C)
        process.send_signal(signal.SIGINT)
        try:
            process.wait(timeout=10)  # Give the app time to shut down
            print("Flask app terminated.")
        except subprocess.TimeoutExpired:
            print("Flask app did not terminate gracefully.  Forcing termination...")
            process.terminate() # More forceful termination
            process.wait() # Ensure it's terminated

        print("Driver script exiting.")
        

def main():
    """Main function to orchestrate the script execution."""

    excel_file = "judge_poster_assignment_matrix.xlsx"
    passwords_file = "judge_passwords.csv"
    reshaped_data_file = "reshaped_judges_data.csv"
    judges_data_csv = 'judge_poster_assignment_matrix.csv'

    if not check_file_exists(excel_file):
        print(f"Error: {excel_file} not found. Please make sure it exists.")
        return

    if not check_file_exists(passwords_file):
        print("Generating passwords...")
        run_script("pass_gen.py")

    if not check_file_exists(reshaped_data_file):
        print("Reshaping data...")
        run_script("data_reshaper.py")


    #check for judge_poster_assignment_matrix.csv
    if not check_file_exists(judges_data_csv):
        try:
            print("generating judge_poster_assignment_matrix.csv")
            df = pd.read_excel(excel_file)
            df.to_csv(judges_data_csv, index=False)
        except FileNotFoundError:
            print("Could not find the excel file from where the .csv has to be generated")
            return
        except Exception as e:
            print("An Exception occured while creating csv of judge_poster_assignment_matrix.xlsx : ", e)
            return


    if (check_file_exists(passwords_file) and
        check_file_exists(reshaped_data_file) and
        check_file_exists(judges_data_csv)):
        print("Starting Flask app...")
        run_flask_app("app.py")
    else:
        print("Required files are missing.  Could not start the app.")

if __name__ == "__main__":
    main()