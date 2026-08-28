import pandas as pd
import random

df = pd.read_csv('data/Employee Sample Data.csv')

tech_skills = ['Python', 'SQL', 'AWS', 'NLP', 'React', 'Machine Learning', 'Data Analysis', 'DevOps', 'FastAPI', 'Docker']
availability_status = ['Available', 'In Project (1 month left)', 'In Project (3 months left)', 'Unavailable']

random.seed(42) 
df['Skills'] = [', '.join(random.sample(tech_skills, k=random.randint(2, 5))) for _ in range(len(df))]
df['Availability'] = [random.choice(availability_status) for _ in range(len(df))]
df['PastProjects'] = [f"Project_{random.randint(100, 999)}" for _ in range(len(df))]

final_cols = ['EEID', 'Full Name', 'Department', 'Job Title', 'Skills', 'Availability', 'PastProjects']
employees_clean = df[final_cols]


employees_clean.to_csv('data/employees_cleaned.csv', index=False)

print(employees_clean.head())