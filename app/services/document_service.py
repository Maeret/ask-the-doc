import os
import requests
from typing import List
from app.components.web_scrapper import WebScrapper
from haystack import Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from bs4 import BeautifulSoup

class DocumentService:
    def __init__(self):
        self.web_scrapper = WebScrapper()
        self.document_store = InMemoryDocumentStore()

    def fetch_site_urls(self, base_url: str) -> List[str]:
        """Get all the site pages recursively and get their urls"""
        visited = set()
        to_visit = [base_url]
        urls = []

        while to_visit:
            url = to_visit.pop()
            if url in visited:
                continue
            try:
                response = requests.get(url)
                response.raise_for_status()
                visited.add(url)
                urls.append(url)
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Get all links from the page
                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    if href.startswith('/') or href.startswith(base_url):
                        full_url = href if href.startswith('http') else f"{base_url}{href}"
                        if full_url not in visited:
                            to_visit.append(full_url)
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch {url}: {e}")
                continue
        return urls

    def process_host(self, base_url: str) -> List[Document]:
        """Fetch pages, transform them to documents and write them to store"""
        urls = self.fetch_site_urls(base_url)
        print(f"Fetched URLs: {urls}")

        documents = self.web_scrapper.run(urls=urls)["documents"]
        
        # InMemoryDocumentStore
        self.document_store.write_documents(documents)
        return documents

    #def get_all_documents(self) -> List[Document]:
    #    """Get all documents from database"""
    #    return self.document_store.get_all_documents()

if __name__ == "__main__":
    # Test block for local debugging
    service = DocumentService()
    test_host = "https://docusaurus.io"  # Replace with your website URL

    print("Fetching URLs...")
    fetched_urls = service.fetch_site_urls(test_host)
    print(f"Fetched URLs: {fetched_urls}")

    print("Processing host to generate documents...")
    documents = service.process_host(test_host)
    print(f"Generated {len(documents)} documents.")

    # Uncomment the following lines if you want to print document contents
    for doc in documents[:3]:  # Print first 3 documents for brevity
        print(f"Document content: {doc.content[:100]}...")  # Print first 100 characters
