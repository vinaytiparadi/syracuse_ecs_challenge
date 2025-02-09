# Poster Judging Web Application

This project implements a simple web application for judges to evaluate posters in a competition. It utilizes Flask for the backend and basic HTML/CSS for the frontend and uses Excel file as a database for simplification.

## Project Structure

The project directory is organized as follows:

```
poster_judging_app/
├── app.py
├── dashboard.html
├── data_reshaper.py
├── driver.py
├── judge_passwords.csv       (Generated)
├── judge_poster_assignment_matrix.csv (Generated)
├── judge_poster_assignment_matrix.xlsx  (Input)
├── login.html
├── output_for_part3.xlsx     (Generated)
├── pass_gen.py
├── requirements.txt
└── img1.jpg (Optional Input - Path should be updated in the login.html file.)
```

**Explanation of Files:**

*   **`app.py`**:  The main Flask application.  Handles user login, authentication, poster score submission, and data storage.
*   **`dashboard.html`**:  The HTML template for the judge's dashboard.  Displays assigned posters and allows score input.
*   **`data_reshaper.py`**: A Python script to transform the initial poster assignment data into a format suitable for the application.
*   **`driver.py`**: A script to orchestrate the entire process: data preparation, password generation (if needed), and starting the Flask application.  Handles graceful shutdown.
*   **`judge_passwords.csv`**: (Generated Data) A CSV file storing judge IDs and their corresponding passwords. Created by `pass_gen.py`.
*    **`judge_poster_assignment_matrix.csv`**: (Generated Data) CSV file generated from the input excel file using pandas.
*   **`judge_poster_assignment_matrix.xlsx`**:  (Input Data) An Excel file containing the initial judge-poster assignments.  **You need to provide this file.**  The format should be:
    *   The first column is labeled "Poster #".
    *   Subsequent columns are labeled with Judge IDs (e.g., "1", "2", "3"...).
    *   A '1' in a cell indicates that the judge in that column is assigned to the poster in that row.  A '0' or blank indicates no assignment.
*   **`login.html`**: The HTML template for the judge login page.
*   **`output_for_part3.xlsx`**: (Generated Data) An Excel file containing the final scores, created upon graceful shutdown of the application.  This is the converted version of `reshaped_judges_data.csv`.
*   **`pass_gen.py`**:  Generates random passwords for each judge and saves them to a CSV file.
* **`reshaped_judges_data.csv`**: (Generated Data)  A CSV file storing the reshaped data, including poster number, judge number, and scores (initially 0).  Created by `data_reshaper.py`.
*   **`requirements.txt`**: Lists the required Python packages (Flask and pandas).
*   **`img1.jpg`**: (Input Data) Background Image for the login.html. **You need to add the path to your own image in the login.html, if you plan to use one**

## Setup and Execution

1.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Prepare Input Data:**

    *   Create an Excel file named `judge_poster_assignment_matrix.xlsx` with the format described above.  Place this file in the same directory as the other scripts.

3.  **Run the Driver Script:**

    ```bash
    python driver.py
    ```

    This script will:
    *   Check for the existence of `judge_poster_assignment_matrix.xlsx`.
    *   Generate `judge_passwords.csv` if it doesn't exist (using `pass_gen.py`).
    *   Generate `reshaped_judges_data.csv` if it doesn't exist (using `data_reshaper.py`).
        *   Generate `judge_poster_assignment_matrix.csv` from the input excel file.
    *   Start the Flask application (`app.py`).

4.  **Access the Application:**

    Open a web browser and go to `http://127.0.0.1:6969/`.  You should see the login page.

## Approach on How to Use the Web Application (For Judges)

1.  **Obtain Credentials:** You will be provided with a Judge ID.  The `driver.py` script automatically generates a `judge_passwords.csv` file containing the Judge ID and a randomly generated password.  The administrator of the system should securely share your Judge ID and password with you.  *Do not share these credentials.*

2.  **Login:**
    *   Open your web browser and navigate to `http://127.0.0.1:6969/`.
    *   Enter your assigned Judge ID in the "Judge ID" field.
    *   Enter your password in the "Password" field.
    *   Click the "Login" button.

3.  **Dashboard:**
    *   If your login is successful, you will be redirected to your personal dashboard.
    *   The dashboard displays a list of all posters you are assigned to judge.  Each poster entry will have:
        *   The poster number (e.g., "Poster #1").
        *   Input fields for "Innovation," "Clarity," and "Presentation."  These fields will initially show the scores (if previously submitted) or '0' if no scores have been entered yet.
        *   A "Total" score, which automatically calculates the sum of the three category scores.
        *   A "Submit Scores" button.

4.  **Scoring Posters:**
    *   For each poster, enter a score out of 10 for each of the three categories: Innovation would be scored out of 4 , Clarity would be scoredout of 3, and Presentation would be scored out of 3.
    *   As you enter scores, the "Total" will update dynamically.
    *   Once you have entered scores for a poster, click the "Submit Scores" button *for that poster*.  This saves your scores for that specific poster.  You can submit scores for each poster individually.

5.  **Reviewing and Editing Scores:**
    *   You can revisit the dashboard at any time *before the application is shut down* to review or modify your scores.  The dashboard will display your most recently submitted scores.  Simply change the scores in the input fields and click "Submit Scores" again to update them.

6.  **Logout (Optional):**
     *  There is a "Logout" button. Clicking it will end your session and return you to the login page. Logging out does *not* finalize the scores. Scores are saved each time you click "Submit Scores".

7. **Completion:** Once you are finished scoring all assigned posters and have submitted the scores, you have completed your judging duties.

## Important Considerations for Judges

*   **Submit Frequently:** It's recommended to click "Submit Scores" for each poster after you've entered the scores. This ensures your work is saved even if you accidentally close your browser or lose your internet connection.
*   **Shutdown:**  The scores are *permanently* saved only when the administrator shuts down the application using `Ctrl+C or Cmd` in the terminal where `driver.py` is running.
