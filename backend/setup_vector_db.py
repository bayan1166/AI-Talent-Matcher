import pandas as pd
import chromadb
import os

os.makedirs('chroma_data', exist_ok=True)

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="resumes_collection")

resumes_df = pd.read_csv('data/resumes_cleaned.csv')

documents = []
metadatas = []
ids = []

for index, row in resumes_df.iterrows():
    text = f"Skills: {row['skills']} | Responsibilities: {row['responsibilities']}"
    documents.append(text)
    
    metadatas.append({
        "candidate_id": str(row['CandidateID']), 
        "major": str(row['major_field_of_studies'])
    })
    
    ids.append(str(row['CandidateID']))

try:
    print("Uploading data to ChromaDB...\n")
    
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print("Vector database setup complete! ")

except Exception as e:
    print(f"Error: {e}")