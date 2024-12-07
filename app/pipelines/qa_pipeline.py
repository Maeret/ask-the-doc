import os
from dotenv import load_dotenv
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack.components.generators import HuggingFaceAPIGenerator
from haystack.utils import Secret

load_dotenv()

def create_qa_pipeline(document_store):
    """
    Factory function to create a QA pipeline.
    """
    text_embedder = SentenceTransformersTextEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
    text_embedder.warm_up()

    retriever = InMemoryEmbeddingRetriever(document_store)

    template = """
        You are provided with some documents from the site.
        Use **only** the information from these documents to answer the question.
        If the information is not in the documents, respond with "I don't know."
        
        Document Content:
        {% for document in documents %}
            Content: {{ document.content }}
            Source URL: {{ document.meta.url }}
        {% endfor %}
        
        Question: {{ question }}
        Answer: Include the source URL in your response.
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

    pipeline = Pipeline()
    pipeline.add_component("text_embedder", text_embedder)
    pipeline.add_component("retriever", retriever)
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.add_component("llm", hf_generator)

    pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
    pipeline.connect("retriever", "prompt_builder.documents")
    pipeline.connect("prompt_builder", "llm")

    return pipeline
