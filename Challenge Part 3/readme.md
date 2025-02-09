# Poster Score Ranking – Hackathon Part 3

## Overview
This part ranks posters based on judges' scores, ensuring fairness and balancing multiple evaluation criteria. Each poster is judged by two judges, and the algorithm combines their scores to produce an overall ranking. The ranking considers **Innovation (0-4 scale)**, **Clarity (0-3 scale)**, and **Presentation (0-3 scale)**, along with the **Total** score.

The final output is a ranked list of posters saved in a new Excel file.

---

## Features
- **Multi-Criteria Ranking**: Posters are ranked based on the following criteria (in order of priority):
  1. **Total Score**: Sum of the scores across both judges for all categories.
  2. **Innovation (0-4 scale)**: Average score across both judges.
  3. **Clarity (0-3 scale)**: Average score across both judges.
  4. **Presentation (0-3 scale)**: Average score across both judges.
  
- **Fair Tie-Breaking**: Ties are resolved by considering `Innovation`, followed by `Clarity`, and finally `Presentation`.
- **Dense Ranking**: Posters with identical scores receive the same rank, and subsequent ranks adjust without skipping.
- **Handles Missing Scores**: Missing scores are recorded as `0` and ignored when calculating averages to ensure fairness.

---

## Assumptions and Input File Structure
1. **Input File Requirements**:
   - Must be an Excel file (`.xlsx`).
   - Each row represents a score given by a specific judge for a specific poster.
   - Required columns:
     - **Poster #**: Unique identifier for each poster (integer).
     - **Judge #**: Identifier for the judge (integer).
     - **Innovation**: Score for innovation (0-4 scale).
     - **Clarity**: Score for clarity (0-3 scale).
     - **Presentation**: Score for presentation (0-3 scale).
     - **Total**: Sum of the scores for `Innovation`, `Clarity`, and `Presentation`.

2. **Input File Structure**:  
   Since each poster is judged by two judges, there are two rows for each poster with the corresponding scores from each judge.

### Example Input File:
| Poster # | Judge # | Innovation | Clarity | Presentation | Total |
|----------|---------|------------|---------|--------------|-------|
| 1        | 101     | 4.0        | 3.0     | 3.0          | 10.0  |
| 1        | 102     | 3.5        | 2.5     | 2.5          | 8.5   |
| 2        | 103     | 4.0        | 3.0     | 2.5          | 9.5   |
| 2        | 104     | 3.0        | 2.5     | 2.0          | 7.5   |
| 3        | 105     | 3.5        | 2.0     | 2.5          | 8.0   |
| 3        | 106     | 3.0        | 2.5     | 3.0          | 8.5   |

---

## How the Ranking Works
1. **Data Processing**:
   - The script reads the input Excel file and groups rows by `Poster #`.
   - For each poster, it calculates the following:
     - **Total Score**: Sum of all judges’ `Total` scores.
     - **Average Scores** for `Innovation`, `Clarity`, and `Presentation`.

2. **Sorting and Ranking**:
   Posters are ranked in descending order based on the following priority:
   1. **Total Score**: Higher total scores are ranked first.
   2. **Innovation (0-4 scale)**: If two posters have the same total score, the one with the higher average innovation score is ranked higher.
   3. **Clarity (0-3 scale)**: If a tie persists, the one with the higher average clarity score is ranked higher.
   4. **Presentation (0-3 scale)**: Finally, the average presentation score is used to break remaining ties.

3. **Dense Ranking**:
   - Posters with identical scores across all criteria receive the same rank.
   - For example, if two posters are tied at rank 1, the next poster will be ranked 2, not 3.

4. **Output Generation**:
   - A `Rank` column is added to the original DataFrame.
   - The ranked data is saved as a new Excel file (`poster_scores_test_data_ranked_v1.xlsx`).

---

## Installation

### Prerequisites
- Python 3.x
- Required Python libraries:
  - `pandas`
  - `openpyxl`

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Execution Steps
```bash
python rank_poster_score.py
