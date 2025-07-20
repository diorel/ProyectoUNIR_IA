from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .rag import RAGSystem

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/query")
async def query_rag(query: Query):
    try:
        response = rag_system.query(query.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Initialize the RAG system at startup
rag_system = None

@app.on_event("startup")
async def startup_event():
    global rag_system
    try:
        rag_system = RAGSystem()
    except Exception as e:
        print(f"Error initializing RAG system: {str(e)}")
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 