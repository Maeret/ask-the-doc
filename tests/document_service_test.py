import asyncio
from app.services.document_service import DocumentService

async def run_manual_test():
    """Manual test for DocumentService."""
    service = DocumentService()
    test_host = "https://maeret.github.io/iframe-doc/"  # Replace with your website URL
  
    await service.process_host(test_host)


if __name__ == "__main__":
    asyncio.run(run_manual_test())
