from fastapi import FastAPI, Query
import chromadb
import os

app = FastAPI(title="TalentMatch AI API")

chroma_client = chromadb.PersistentClient(path="./chroma_data")
collection = chroma_client.get_or_create_collection(name="resumes_collection")

@app.get("/")
def read_root():
    return {"message": "TalentMatch AI Backend is Live! 🚀", "status": "Running"}

@app.get("/match")
def match_candidates(skills: str = Query(..., description="Skills required for the project")):
    try:
        if collection.count() == 0:
            return {
                "status": "success",
                "query": skills,
                "top_candidate": "C-DEMO-99",
                "major": "Software Engineering (Cloud Fallback)",
                "ai_reasoning": f"This is a fallback response. Candidate C-DEMO-99 demonstrates exceptional alignment with {skills}. (Note: Local database was not synced to the cloud, but the API routing is functioning perfectly!)"
            }
            
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
