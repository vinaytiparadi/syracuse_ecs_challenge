import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
from typing import Dict, List, Tuple, Optional
import time
import sys

class ExpertiseScorer:
    def __init__(self):
        nltk.download('stopwords', quiet=True)
        self.model = SentenceTransformer('all-mpnet-base-v2')
        self.tfidf = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000
        )
        self.field_relations = {
            'computer': ['software', 'programming', 'algorithms', 'data', 'ai', 'machine learning'],
            'electrical': ['circuits', 'electronics', 'signals', 'power', 'communications'],
            'mechanical': ['mechanics', 'dynamics', 'thermodynamics', 'materials'],
            'civil': ['structures', 'construction', 'environmental', 'geotechnical'],
            'chemical': ['chemistry', 'process', 'materials', 'biochemical'],
            'biomedical': ['medical', 'biology', 'health', 'tissue', 'biomechanics'],
            'physics': ['quantum', 'optics', 'mechanics', 'electronics', 'materials'],
            'mathematics': ['statistics', 'analysis', 'algorithms', 'computation']
        }

    def preprocess_text(self, text: str) -> str:
        if pd.isna(text): return ""
        text = re.sub(r'[^a-zA-Z\s]', ' ', str(text).lower())
        return ' '.join(text.split())

    def get_field_keywords(self, field: str) -> set:
        keywords = set()
        field = field.lower()
        for key, values in self.field_relations.items():
            if key in field: keywords.update(values)
        return keywords

    def calculate_keyword_overlap(self, text1: str, text2: str) -> float:
        if not text1.strip() or not text2.strip(): return 0.0
        try:
            tfidf_matrix = self.tfidf.fit_transform([text1, text2])
            return float((tfidf_matrix * tfidf_matrix.T).toarray()[0, 1])
        except Exception as e:
            print(f"Warning: TF-IDF calculation failed: {e}"); return 0.0

    def calculate_field_similarity(self, field1: str, field2: str) -> float:
        try:
            field1, field2 = str(field1).lower(), str(field2).lower()
            if field1 == field2: return 1.0
            keywords1, keywords2 = self.get_field_keywords(field1), self.get_field_keywords(field2)
            if not keywords1 or not keywords2: return 0.0
            return float(len(keywords1 & keywords2) / len(keywords1 | keywords2))
        except Exception as e:
            print(f"Warning: Field similarity calculation failed: {e}"); return 0.0

    def calculate_expertise_score(self, text: str) -> float:
        try:
            if pd.isna(text) or not str(text).strip(): return 0.0
            text = str(text).lower()
            expertise_terms = {'expert': 0.8, 'specialist': 0.8, 'research': 0.6, 'published': 0.7,
                               'experience': 0.6, 'developed': 0.5, 'phd': 0.7, 'professor': 0.7, 'advanced': 0.6}
            score, matches = 0.0, 0
            for term, weight in expertise_terms.items():
                if term in text: score += weight; matches += 1
            return float(score / (matches if matches > 0 else 1))
        except Exception as e:
            print(f"Warning: Expertise score calculation failed: {e}"); return 0.0

    def calculate_match_score(self, poster_data: Dict, judge_data: Dict, professor_data: Optional[Dict]) -> Tuple[float, Dict[str, float]]:
        try:
            if not professor_data:
                return 0.0, {'semantic_similarity': 0.0, 'keyword_overlap': 0.0, 'field_relevance': 0.0, 'expertise_level': 0.0}

            poster_abstract = self.preprocess_text(str(poster_data.get('Abstract', '')))
            judge_text = self.preprocess_text(' '.join([
                str(professor_data.get('Current Research', '')),
                str(professor_data.get('Areas of Interest / Research Interests', '')),
                str(professor_data.get('Description', ''))
            ]))

            semantic_score = 0.0
            if poster_abstract and judge_text:
                try:
                    poster_embedding = self.model.encode([poster_abstract])[0]
                    judge_embedding = self.model.encode([judge_text])[0]
                    semantic_score = float(np.dot(poster_embedding, judge_embedding) /
                                        (np.linalg.norm(poster_embedding) * np.linalg.norm(judge_embedding)))
                except Exception as e:
                    print(f"Warning: Semantic similarity calculation failed: {e}")

            keyword_score = float(self.calculate_keyword_overlap(poster_abstract, judge_text))
            field_score = float(self.calculate_field_similarity(poster_data.get('Program', ''), judge_data.get('Department', '')))
            expertise_score = float(self.calculate_expertise_score(judge_text))
            weights = {'semantic': 0.35, 'keyword': 0.25, 'field': 0.0, 'expertise': 0.40}
            final_score = (semantic_score * weights['semantic'] + keyword_score * weights['keyword'] +
                           field_score * weights['field'] + expertise_score * weights['expertise'])
            component_scores = {'semantic_similarity': semantic_score, 'keyword_overlap': keyword_score,
                                'field_relevance': field_score, 'expertise_level': expertise_score}
            return float(final_score), component_scores

        except Exception as e:
            print(f"Warning: Match score calculation failed: {e}")
            return 0.0, {'semantic_similarity': 0.0, 'keyword_overlap': 0.0, 'field_relevance': 0.0, 'expertise_level': 0.0}


def perform_matching(posters_file, judges_file, professors_file, output_posters_file, output_judges_file):
    """Performs the judge-poster matching and saves the results."""
    try:
        print("Loading data files... ", end="", flush=True)
        posters = pd.read_excel(posters_file, engine='openpyxl')
        judges = pd.read_excel(judges_file, engine='openpyxl')
        professors = pd.read_excel(professors_file, engine='openpyxl')
        print("Data files loaded successfully!")

        scorer = ExpertiseScorer()
        judge_professor_matches = {}

        print("Matching judges with professors... ", end="", flush=True)
        for _, judge in judges.iterrows():
            for _, prof in professors.iterrows():
                prof_name = str(prof['Professor Name']).lower()
                if (str(judge['Judge FirstName']).lower() in prof_name and
                    str(judge['Judge LastName']).lower() in prof_name):
                    judge_professor_matches[judge['Judge']] = prof.to_dict()
                    break
        print("Judge-professor matching complete.")

        assignments = []
        print("Calculating match scores... This might take a while, brewing some coffee... ☕", end="", flush=True)
        start_time = time.time()
        dot_count = 0
        for i, poster in posters.iterrows():
            pid = poster['Poster #']
            time_slot = 1 if pid % 2 == 1 else 2
            for j, judge in judges.iterrows():
                jid = judge['Judge']
                if str(judge['Hour available']).lower() == 'both' or int(judge['Hour available']) == time_slot:
                    try:
                        score, components = scorer.calculate_match_score(poster.to_dict(), judge.to_dict(), judge_professor_matches.get(jid))
                        assignments.append({'poster_id': pid, 'judge_id': jid, 'score': score, 'components': components, 'time_slot': time_slot})
                    except Exception as e:
                        print(f"Warning: Assignment calculation failed for poster {pid} and judge {jid}: {e}")

                    # Fun progress indicator
                    if time.time() - start_time > 1:  # Print a dot every second
                        print("." * (dot_count % 4), end="\r", flush=True)  # Cycle through 0-3 dots
                        dot_count += 1
                        start_time = time.time()
        print("\nMatch scores calculated!  Phew, that was intense!")

        assignments.sort(key=lambda x: float(x['score']), reverse=True)
        poster_assignments, judge_assignments = {pid: [] for pid in posters['Poster #']}, {jid: [] for jid in judges['Judge']}
        MAX_POSTERS_PER_JUDGE = 6

        print("Assigning judges to posters... ", end="", flush=True)
        for assignment in assignments:
            pid, jid = assignment['poster_id'], assignment['judge_id']
            if len(poster_assignments[pid]) < 2 and len(judge_assignments[jid]) < MAX_POSTERS_PER_JUDGE:
                poster_assignments[pid].append(jid)
                judge_assignments[jid].append(pid)
        print("Assignments complete.")

        print("Preparing output data... ", end="", flush=True)
        output_posters = [{**poster.to_dict(), 'Assigned Judge 1 ID': assigned[0] if len(assigned) > 0 else None,
                           'Assigned Judge 2 ID': assigned[1] if len(assigned) > 1 else None}
                          for _, poster in posters.iterrows() for assigned in [poster_assignments[poster['Poster #']]]]
        output_judges = [{'Judge No. #': jid, 'Judge FirstName': judge['Judge FirstName'], 'Judge LastName': judge['Judge LastName'],
                          'Department': judge['Department'], 'Hour available': judge['Hour available'],
                          **{f'Assigned Poster {i+1} ID': p for i, p in enumerate(assigned[:MAX_POSTERS_PER_JUDGE])}}
                         for _, judge in judges.iterrows() for jid, assigned in [(judge['Judge'], judge_assignments[judge['Judge']])]]
        for judge_data in output_judges:
            for i in range(len(judge_data)-5,MAX_POSTERS_PER_JUDGE+1):
                if f'Assigned Poster {i} ID' not in judge_data:
                   judge_data[f'Assigned Poster {i} ID']=None
        print("Output data prepared.")

        print("Saving results to Excel files... ", end="", flush=True)
        pd.DataFrame(output_posters).to_excel(output_posters_file, index=False, engine='openpyxl')
        pd.DataFrame(output_judges).to_excel(output_judges_file, index=False, engine='openpyxl')
        print(f"\nMatching completed! Output files saved to {output_posters_file} and {output_judges_file}")

    except Exception as e:
        print(f"Error in matching/assignment: {e}")
        raise

if __name__ == '__main__':
    print("Starting the matching process... ✨")
    perform_matching('Sample_input_abstracts.xlsx', 'Example_list_judges.xlsx',
                     'professors.xlsx', 'new_sample_input_abstracts.xlsx', 'new_example_list_judges.xlsx')
    print("Matching process finished! 🎉")