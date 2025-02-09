# Research Day Poster Judge Assignment

## Overview
This project automates the process of assigning judges to research posters for the College of Engineering and Computer Science (ECS) Research Day. The system ensures fair and efficient matching while adhering to multiple constraints.

## Features
- **Judge-Poster Matching**: Assigns judges to posters while ensuring each poster has exactly two judges and each judge is assigned a maximum of six posters.
- **Time Slot Constraints**: Odd-numbered posters are judged in the first hour, even-numbered in the second hour. Judges' availability is taken into account.
- **Conflict Avoidance**: Judges are not assigned to posters where they are the advisor.
- **Expertise-Based Matching**: Uses NLP techniques to match judges based on research interests.
- **Automated Web Scraping**: Scrapes faculty web pages to extract research interests for better matching.
- **Output Reports**: Generates three Excel files with judge-poster assignments in different formats.

## File Structure
- `driver.py`: Main script that orchestrates the process.
- `scraper.py`: Scrapes faculty information for judge expertise evaluation.
- `matcher.py`: Assigns judges to posters based on constraints and expertise scoring.
- `matrix_creator.py`: Generates a binary matrix of judge-poster assignments.
- `requirements.txt`: List of dependencies.
- **Required Input Files**:
  - `Sample_input_abstracts.xlsx`: Contains poster abstracts and advisor names.
  - `Example_list_judges.xlsx`: Contains judge names, departments, and availability.
  - `professors.xlsx`: (Optional) If missing, the scraper will generate this file with faculty research interests.

### Example Input Data for `Sample_input_abstracts.xlsx`
The input data in `Sample_input_abstracts.xlsx` might look like this:

| Poster # | Title   | Abstract   | Advisor FirstName | Advisor LastName | Program                      |
|----------|---------|------------|------------------|-----------------|-----------------------------|
| 1        | Title 1 | Abstract 1 | Advisor 1 FirstName | Advisor 1 LastName | Computer/Information Science |
| 2        | Title 2 | Abstract 2 | Advisor 2 FirstName | Advisor 2 LastName | Electrical/Computer Engineering |
| 3        | Title 3 | Abstract 3 | Advisor 3 FirstName | Advisor 3 LastName | Civil Engineering           |
| 4        | Title 4 | Abstract 4 | Advisor 4 FirstName | Advisor 4 LastName | Electrical/Computer Engineering |
| 5        | Title 5 | Abstract 5 | Advisor 5 FirstName | Advisor 5 LastName | Bioengineering              |

---

### Example Input Data for `Example_list_judges.xlsx`
The input data in `Example_list_judges.xlsx` might look like this:

| Judge | Judge FirstName | Judge LastName | Department | Hour available |
|-------|-----------------|----------------|------------|----------------|
| 1     | Judge 1 FirstName | Judge 1 LastName | EECS       | both           |
| 2     | Judge 2 FirstName | Judge 2 LastName | EECS       | 1              |
| 3     | Judge 3 FirstName | Judge 3 LastName | EECS       | 2              |
| 4     | Judge 4 FirstName | Judge 4 LastName | EECS       | both           |
| 5     | Judge 5 FirstName | Judge 5 LastName | EECS       | 2              |

---
## Approach for Assigning Judges to Posters
The assignment of judges to posters is performed in multiple stages:

### 1. **Scraping Faculty Research Interests** (`scraper.py`)
- Web scraping is used to collect ECS faculty research interests from official webpages.
- Extracted data includes areas of expertise, research focus, and descriptions.
- This information is stored in `professors.xlsx` for later use.

### 2. **Computing Expertise Scores** (`matcher.py`)
- The system evaluates judges' expertise using research data scraped from faculty webpages (`professors.xlsx`).
- Judges' research interests, areas of expertise, and past publications are extracted and used for matching.
- NLP techniques such as TF-IDF (Term Frequency-Inverse Document Frequency) and sentence embeddings are applied to compute similarity scores.
- The scoring system consists of:
  - **BERT-based Sentence Embeddings**:
    - Uses the all-mpnet-base-v2 model from sentence-transformers to encode poster abstracts and judges' research descriptions.
    - Computes cosine similarity between embeddings to determine how closely related a judge’s expertise is to a given poster.
    - Semantic similarity score contributes 35% to the final score.
   
  - **TF-IDF Keyword Overlap**:
    - Extracts important keywords from both poster abstracts and judges' research areas.
    - Computes similarity based on common keyword presence.
    - Keyword similarity score contributes 25% to the final score.
   
  - **Field Relevance (Department-based Matching)**:
    - Uses predefined field relationships (e.g., Computer Science → AI, Algorithms, Software Engineering) to determine topic overlap.
    - Currently set to 0% weight but can be adjusted.

  - **Expertise Level Score (Lexical Matching)**:
    - Checks for domain-specific words like "expert", "professor", "PhD", "research", etc., in judge descriptions.
    - Expertise score contributes 40% to the final score.
- Judges receive an overall expertise score based on these weighted components, which helps in optimal assignment.


### 3. **Applying Constraints for Assignment** (`matcher.py`)
- Each poster is assigned exactly two judges.
- Each judge is assigned a maximum of six posters.
- Judges are assigned based on availability and expertise score.
- Advisors are excluded from reviewing their own students' posters.
- Posters are scheduled according to their number (odd/even) and judge availability.

### 4. **Generating Assignment Outputs** (`matrix_creator.py`)
- The final assignments are written to Excel files for review.
- A binary matrix is created, where rows represent posters and columns represent judges, with values indicating assignments.

This systematic approach ensures that assignments are optimized while adhering to all constraints.

## Installation
This project requires Python 3.10.

1. Ensure you have Python 3.10 installed.
2. Clone the repository.
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Program
Ensure the required input files (`Sample_input_abstracts.xlsx` and `Example_list_judges.xlsx`) are in the same directory as `driver.py`.
Execute the main script:
```sh
python driver.py
```

## Outputs
- `processed_Sample_input_abstracts.xlsx`: Poster assignments.
- `processed_Example_list_judges.xlsx`: Judge assignments.
- `judge_poster_assignment_matrix.xlsx`: Binary matrix representation of assignments.

## Assumptions
- Judges are ECS faculty members.
- At least `J > P/3` for feasible assignments.
- Research expertise is determined using faculty webpage data.
- If scraping fails, a fallback method may be needed for expertise matching.
- The input Excel files follow a specific format but may have additional columns.

## Future Enhancements
- Improve NLP-based expertise matching.
- Provide a web-based interface for input and output management.
- Implement conflict resolution for ambiguous cases.

---
