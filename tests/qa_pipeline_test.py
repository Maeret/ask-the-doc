from app.pipelines.qa_pipeline import run_qa_pipeline


def run_test():
    """Manual test for QA pipeline."""
    question = "What is wallet?"  
  
    run_qa_pipeline(question)


if __name__ == "__main__":
    run_test()