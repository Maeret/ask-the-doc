import os
from dotenv import load_dotenv
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack.components.generators import HuggingFaceAPIGenerator
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.utils import Secret

load_dotenv()

document_store = InMemoryDocumentStore()

def run_qa_pipeline(question: str):
    """
    Execute the QA pipeline for a given question.
    """
    # Настройка компонентов пайплайна
    text_embedder = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
    text_embedder.warm_up()

    retriever = InMemoryEmbeddingRetriever(document_store)

    template = """
    You are provided with a document containing a list of error codes and their descriptions.
    Use only the information from this document to answer questions about specific error codes.
    If an error code is not in the document, respond with "I don't know."

    Document Content:
    {% for document in documents %}
        {{ document.content }}
    {% endfor %}

    Question: {{ question }}
    Answer:
    """

    prompt_builder = PromptBuilder(template=template)

    hf_generator = HuggingFaceAPIGenerator(
        api_type="serverless_inference_api",
        api_params={"model": "HuggingFaceH4/zephyr-7b-beta"},
        token=Secret.from_token(os.getenv("HUGGINGFACEHUB_API_TOKEN")),
        generation_kwargs={
            'temperature': 0.1,
            'top_k': 5,
            'max_new_tokens': 50
        }
    )

    rag_pipeline = Pipeline()
    rag_pipeline.add_component("text_embedder", text_embedder)
    rag_pipeline.add_component("retriever", retriever)
    rag_pipeline.add_component("prompt_builder", prompt_builder)
    rag_pipeline.add_component("llm", hf_generator)

    rag_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
    rag_pipeline.connect("retriever", "prompt_builder.documents")
    rag_pipeline.connect("prompt_builder", "llm")

    response = rag_pipeline.run({
        "text_embedder": {"text": question},
        "prompt_builder": {"question": question}
    })

    if not response["llm"]["replies"][0].strip():
        return "I don't know"
    return response["llm"]["replies"][0]
