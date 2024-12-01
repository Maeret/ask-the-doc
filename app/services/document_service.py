import os
import requests
import asyncio
import ssl
import aiohttp
from dotenv import load_dotenv
from typing import List
from urllib.parse import urljoin
from app.components.web_scrapper import WebScrapper
from haystack import Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from bs4 import BeautifulSoup

load_dotenv()

ssl_crt_path = os.environ.get("SSL_CRT")

if ssl_crt_path and os.path.exists(ssl_crt_path):
    print(f"Using SSL {ssl_crt_path}")
    ssl_context = ssl.create_default_context(cafile=ssl_crt_path)
else:
    print("SSL certificate not found or path is incorrect. Using default context.")
    ssl_context = ssl.create_default_context()

class DocumentService:
    def __init__(self):
        self.web_scrapper = WebScrapper()
        self.document_store = InMemoryDocumentStore()

    async def fetch_page(self, session, url):
        """Asynchronously fetch a single page."""
        try:
            async with session.get(url, ssl=False) as response:
                if response.status != 200:
                    print(f"Error {response.status} for {url}")
                    return None
                html = await response.text()
                return html
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            return None

    async def fetch_site_urls(self, base_url: str) -> List[str]:
        """Asynchronously fetch all URLs on the site."""
        visited = set()
        to_visit = [base_url]
        urls = []
        
        base_url = base_url.rstrip("/") + "/"

        async with aiohttp.ClientSession() as session:
            while to_visit:
                url = to_visit.pop()
                if url in visited:
                    continue
                visited.add(url)

                html = await self.fetch_page(session,url)
                if not html:
                    continue

                urls.append(url)
                soup = BeautifulSoup(html, "html.parser")

                # Get all links from the page
                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                     # Use urljoin to handle relative and absolute links properly
                    full_url = urljoin(base_url, href)
                    
                    # Check if the link is within the base directory
                    if full_url.startswith(base_url) and full_url not in visited:
                        to_visit.append(full_url)

        
        return urls

    async def process_host(self, base_url: str) -> List[Document]:
        """Fetch pages, transform them to documents and write them to store."""
        urls = await self.fetch_site_urls(base_url)
        print(f"Fetched URLs: {urls}")

        documents = self.web_scrapper.run(urls=urls)["documents"]
        
        # Store documents in the database
        self.document_store.write_documents(documents)
        return documents

if __name__ == "__main__":
    # Test block for local debugging
    service = DocumentService()
    test_host = "https://maeret.github.io/iframe-doc"  # Replace with your website URL

    async def main():
        print("Fetching URLs...")
        fetched_urls = await service.fetch_site_urls(test_host)
        print(f"Fetched URLs: {fetched_urls}")

        print("Processing host to generate documents...")
        documents = await service.process_host(test_host)
        print(f"Generated {len(documents)} documents.")

        # Uncomment the following lines if you want to print document contents
        for doc in documents[:3]:  # Print first 3 documents for brevity
            print(f"Document content: {doc.content[:100]}...")  # Print first 100 characters

    # Run the async main function
    asyncio.run(main())
