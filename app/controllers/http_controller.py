#import uvicorn
#from fastapi import FastAPI, APIRouter, HTTPException, Request
#from pydantic import BaseModel
#from typing import List, Optional
##from app.pipelines.qa_pipeline import QAPipeline
##from app.pipelines.embedding_pipeline import EmbeddingPipeline
#from app.services.document_service import DocumentService
#
#router = APIRouter()
#
##qa_pipeline = QAPipeline()
##embedding_pipeline = EmbeddingPipeline()
#document_service = DocumentService()
#
#class HostToScrape(BaseModel):
#    host: str
#
#class QuestionRequest(BaseModel):
#    question: str
#    top_k: Optional[int] = 5
#
#class AnswerResponse(BaseModel):
#    question: str
#    answers: List[str]
#    source_links: List[str]
#
#@router.get("/")
#async def root():
#    return {"message": "It works!"}
#
#@router.post("/host")
#async def scrape(request: HostToScrape):
#    """Create url list to fetch from host url, transform found HTML to documents and write found documents to database"""
#    try:
#        documents = document_service.process_host(request.host)
#        
#        return {"status": "ok", "document_count": len(documents)}
#    except Exception as e:
#        raise HTTPException(status_code=500, detail=str(e))
#
#
#
#
##@router.post("/api/v1/ask", response_model=AnswerResponse)
##async def ask_question(request: QuestionRequest):
##    """
##    Get aswer from documentation
##    """
##    question = request.question
##    top_k = request.top_k
##
##    # Run pipeline
##    try:
##        response = qa_pipeline.run(question=question, top_k=top_k)
##        if not response["answers"]:
##            raise HTTPException(status_code=404, detail="No answer")
##        
##        answers = [ans["answer"] for ans in response["answers"]]
##        source_links = [ans["document"]["meta"]["url"] for ans in response["answers"] if "url" in ans["document"]["meta"]]
##
##        return AnswerResponse(
##            question=question,
##            answers=answers,
##            source_links=source_links
##        )
##    except Exception as e:
##        raise HTTPException(status_code=500, detail=str(e))
##
##
##
##@router.post("/api/v1/update_documents")
##async def update_documents():
##    """
##    
##    """
##    try:
##        embedding_pipeline.run()
##        return {"message": "Success"}
##    except Exception as e:
##        raise HTTPException(status_code=500, detail=str(e))
##
##
##
##@router.get("/api/v1/documents")
##async def get_documents():
##    """
##    Get all documents from database
##    """
##    try:
##        documents = document_service.get_all_documents()
##        return {"documents": documents}
##    except Exception as e:
##        raise HTTPException(status_code=500, detail=str(e))
#
#app = FastAPI()
#
#app.include_router(router)
#
#def start_server():
#    """Start server function"""
#    uvicorn.run(app, host="127.0.0.1", port=8000)
