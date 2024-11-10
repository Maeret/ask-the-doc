import requests
from typing import List
from bs4 import BeautifulSoup
from haystack import component, Document, Pipeline

@component
class WebScrapper:
 
    @component.output_types(documents=List[Document])
    def run(self, urls: List[str]) -> dict:
        documents = []
        errors = []

        for url in urls:
            try:
                r = requests.get(url)
                r.raise_for_status()
                soup = BeautifulSoup(markup=r.text, features='html.parser')
                content = "\n".join([p.text for p in soup.find_all('p')])
                document = Document(content=content, meta={"source": url})
                documents.append(document)
            
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error for {url}: {http_err}")
                errors.append(f"HTTP error for {url}: {http_err}")
            
            except Exception as err:
                print(f"Error for {url}: {err}")
                errors.append(f"Error for {url}: {err}")
        
        return {"documents": documents, "errors": errors}
     
