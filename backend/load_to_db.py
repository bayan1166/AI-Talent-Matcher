import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = 'postgres'
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'ai_talent_db'

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

try:
    print("Uploading data to PostgreSQL... \n")
    
    emp_df = pd.read_csv('data/employees_cleaned.csv')
    emp_df.to_sql('employees', engine, if_exists='replace', index=False)
    print("employees table uploaded")

    res_df = pd.read_csv('data/resumes_cleaned.csv')
    res_df.to_sql('candidates', engine, if_exists='replace', index=False)
    print("candidates table uploaded")

    proj_df = pd.read_csv('data/projects_catalog.csv')
    proj_df.to_sql('projects', engine, if_exists='replace', index=False)
    print("projects table uploaded")

    train_df = pd.read_csv('data/training_catalog.csv')
    train_df.to_sql('training_catalog', engine, if_exists='replace', index=False)
    print("training_catalog table uploaded")

    print("\nAll tables created and data uploaded successfully!")

except Exception as e:
    print(f"Error: {e}")