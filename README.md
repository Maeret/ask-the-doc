# QueryDoc

Ask the documentation.

Basic RAG pipeline with webscrapper. Just fetch any doc site and ask the LLM any question.

## Quick start

```bash
pip install -r requirements.txt
python main.py
```

## Run server

```bash
uvicorn app.main:app --reload
```
## API

Fetch url

```bash
curl -X POST http://localhost:8000/fetch -d '{"base_url": "https://example.com"}' -H "Content-Type: application/json"
```

Ask question

```bash
curl -X POST http://localhost:8000/query -d '{"question": "What is wallet"}' -H "Content-Type: application/json"
```

## Swagger Documentation

Run the server and goto 



