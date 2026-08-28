import pandas as pd

resumes_df = pd.read_csv('data/resume_data.csv')

columns_to_keep = [
    'skills', 
    'major_field_of_studies', 
    'positions', 
    'responsibilities'
]

resumes_clean = resumes_df[columns_to_keep].copy()

resumes_clean.insert(0, 'CandidateID', ['C' + str(i).zfill(4) for i in range(1, len(resumes_clean) + 1)])

resumes_clean.fillna('', inplace=True)

resumes_sampled = resumes_clean.sample(n=500, random_state=42)

resumes_sampled.to_csv('data/resumes_cleaned.csv', index=False)

print(resumes_sampled.head(3))