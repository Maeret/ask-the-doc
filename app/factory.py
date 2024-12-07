from haystack.document_stores.in_memory import InMemoryDocumentStore
from app.pipelines.qa_pipeline import create_qa_pipeline
from app.services.document_service import DocumentService

def create_services():
    """
    Create and return the document service and QA pipeline.
    """
    # Shared document store
    document_store = InMemoryDocumentStore()

    # Document Service
    document_service = DocumentService(document_store=document_store)

    # QA Pipeline
    qa_pipeline = create_qa_pipeline(document_store=document_store)

    return qa_pipeline, document_service
