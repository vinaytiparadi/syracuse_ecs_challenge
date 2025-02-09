from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

PASSWORD_FILE = 'judge_passwords.csv'
JUDGES_DATA_FILE = 'judge_poster_assignment_matrix.csv'
RESHAPED_DATA_FILE = 'reshaped_judges_data.csv'

def load_passwords():
    """Loads judge passwords from CSV."""
    try:
        df = pd.read_csv(PASSWORD_FILE)
        return {str(row['Judge #']): str(row['Password']) for _, row in df.iterrows()}
    except FileNotFoundError:
        return {}

def load_judges_data():
    """Loads judges data from CSV."""
    try:
        return pd.read_csv(JUDGES_DATA_FILE)
    except FileNotFoundError:
        return None

def load_reshaped_data():
    """Loads reshaped judges data from CSV."""
    try:
        return pd.read_csv(RESHAPED_DATA_FILE)
    except FileNotFoundError:
        return None

def save_reshaped_data(df):
    """Saves the reshaped data back to the CSV."""
    df.to_csv(RESHAPED_DATA_FILE, index=False)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        judge_id = request.form['judge_id']
        password = request.form['password']
        passwords = load_passwords()
        if judge_id in passwords and passwords[judge_id] == password:
            session['judge_id'] = judge_id
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid Judge ID or Password')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'judge_id' in session:
        judge_id = session['judge_id']
        judges_df = load_judges_data()
        reshaped_df = load_reshaped_data()

        if judges_df is not None and reshaped_df is not None:
            judge_id_str = str(judge_id)  # Ensure it's a string
            if judge_id_str not in judges_df.columns:
                return "Judge ID not found in judges data.", 404

            assigned_posters = judges_df[judges_df[judge_id_str] == 1]['Poster #'].tolist()

            if request.method == 'POST':
                for poster in assigned_posters:
                    poster_str = str(poster)
                    innovation_key = f'innovation_{poster_str}'
                    clarity_key = f'clarity_{poster_str}'
                    presentation_key = f'presentation_{poster_str}'

                    try:
                        innovation = int(request.form[innovation_key])
                        clarity = int(request.form[clarity_key])
                        presentation = int(request.form[presentation_key])

                        if not (0 <= innovation <= 10 and 0 <= clarity <= 10 and 0 <= presentation <= 10):
                            raise ValueError("Scores must be between 0 and 10")
                        
                        total = innovation + clarity + presentation
                    except (KeyError, ValueError) as e:
                        return f"Invalid score input for poster {poster}: {e}", 400

                    row_index = reshaped_df[
                        (reshaped_df['Poster Number'] == poster) & (reshaped_df['Judge #'] == int(judge_id))
                    ].index
                    if not row_index.empty:
                        reshaped_df.loc[row_index[0], 'Innovation'] = innovation
                        reshaped_df.loc[row_index[0], 'Clarity'] = clarity
                        reshaped_df.loc[row_index[0], 'Presentation'] = presentation
                        reshaped_df.loc[row_index[0], 'Total'] = total
                    else:
                        return f"Data not found for Judge {judge_id} and Poster {poster}.", 404

                save_reshaped_data(reshaped_df)
                reshaped_df = load_reshaped_data()

            poster_data = []
            for poster in assigned_posters:
                score_row = reshaped_df[
                    (reshaped_df['Poster Number'] == poster) & (reshaped_df['Judge #'] == int(judge_id))
                ]
                score_row = score_row.iloc[0] if not score_row.empty else None

                if score_row is not None:
                    poster_data.append({
                        'number': poster,
                        'innovation': score_row['Innovation'],
                        'clarity': score_row['Clarity'],
                        'presentation': score_row['Presentation'],
                        'total': score_row['Total']
                    })
                else:
                    poster_data.append({
                        'number': poster,
                        'innovation': 0,
                        'clarity': 0,
                        'presentation': 0,
                        'total': 0
                    })

            return render_template('dashboard.html', judge_id=judge_id, poster_data=poster_data)
        else:
            return "Error loading data.", 500
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('judge_id', None)
    return redirect(url_for('login'))

def home():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
