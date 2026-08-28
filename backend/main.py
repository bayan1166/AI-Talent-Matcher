from fastapi import FastAPI, Query
from sqlalchemy import create_engine
import pandas as pd
import chromadb
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Talent Matcher API")

DB_USER = 'postgres'
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'ai_talent_db'

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

chroma_client = chromadb.PersistentClient(path="./chroma_data")
collection = chroma_client.get_collection(name="resumes_collection")

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Talent Matcher API!", "status": "Running perfectly"}

@app.get("/employees")
def get_employees():
    try:
        df = pd.read_sql("SELECT * FROM employees LIMIT 5", engine)
        return {"status": "success", "data": df.to_dict(orient="records")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/match")
def match_candidates(skills: str = Query(..., description="Skills required for the project")):
    try:
        results = collection.query(
            query_texts=[skills],
            n_results=1
        )
        
        best_candidate_id = results['metadatas'][0][0]['candidate_id']
        best_major = results['metadatas'][0][0]['major'] if 'major' in results['metadatas'][0][0] else "Not Specified"
        
        ai_reasoning = f"Candidate {best_candidate_id} demonstrates exceptional alignment with the required competencies in {skills}. Their background and technical proficiency make them an optimal fit for project execution."
            
        return {
            "status": "success", 
            "query": skills, 
            "top_candidate": best_candidate_id,
            "major": best_major,
            "ai_reasoning": ai_reasoning
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}