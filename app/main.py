from fastapi import FastAPI, HTTPException
from app.factory import create_services
from pydantic import BaseModel

app = FastAPI()

qa_pipeline, document_service = create_services()

class FetchRequest(BaseModel):
    base_url: str

@app.post("/fetch")
async def fetch_site(request: FetchRequest):
    """
    Fetch site documents and store them.
    """
    try:
        documents = await document_service.process_host(request.base_url)
        return {"status": "success", "fetched": len(documents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
def get_documents():
    """
    Retrieve all stored documents.
    """
    documents = document_service.get_all_documents()
    return {"documents": [doc.to_dict() for doc in documents]}

class QueryRequest(BaseModel):
    question: str
    
@app.post("/query")
def query_pipeline(request: QueryRequest):
    """
    Answer a question using the QA pipeline.
    """
    try:
        answer = qa_pipeline.run({"text_embedder": {"text": request.question}, "prompt_builder": {"question": request.question}})
        return {"question": request.question, "answer": answer["llm"]["replies"][0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
