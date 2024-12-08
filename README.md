# Ask the Doc

Ask the Doc is a basic Retrieval-Augmented Generation (RAG) pipeline with an integrated web scraper. It allows you to fetch any documentation site, store its content, and query it using an LLM (Language Model) for precise answers.

## Features
- Fetch documentation websites and store their content.
- Query the stored content using a pre-configured QA pipeline.
- Supports customizable templates for LLM responses.
- Ready-to-use FastAPI server for easy integration.

---

## Quick Start

### Prerequisites
1. Install Python 3.8+.
2. Add your (https://huggingface.co/docs/hub/security-tokens)[Hugging Face token] to the `.env` file:

   ```plaintext
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
   ```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the server
```bash
uvicorn app.main:app --reload
```

---

## API Reference

### Fetch a website

Store the content of a website for querying:
```bash
curl -X POST http://localhost:8000/fetch \
     -d '{"base_url": "https://example.com"}' \
     -H "Content-Type: application/json"
```

### Get stored documents

Retrieve all stored documents:
```bash
curl -X GET http://localhost:8000/documents
```

### Ask a question

Query the stored documents for an answer:
```bash
curl -X POST http://localhost:8000/query \
     -d '{"question": "What is wallet"}' \
     -H "Content-Type: application/json"
```

---

## Swagger Documentation

Interactive API documentation is available at:
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## How It Works

1. **Fetching:**
   - The `/fetch` endpoint scrapes a website and stores its content in the document store. It doesn't fetch external links from the site, so it's useful for fetching your technical documentation or API.
2. **Document Storage:**
   - All content is stored in an in-memory document store or can be connected to a database for persistence.
3. **Question Answering:**
   - The `/query` endpoint retrieves relevant documents and uses a Hugging Face LLM to answer the question.

---

## Contributing

I welcome contributions to improve the project! Please see the [CONTRIBUTING.md](./CONTRIBUTING.md) file for guidelines.

## Dependecies

This application uses Hugging Face's APIs and requires adherence to their [Terms of Service](https://huggingface.co/terms).

## License

This project is licensed under the **Apache 2.0 License**. See the [LICENSE](./LICENSE) file for details.