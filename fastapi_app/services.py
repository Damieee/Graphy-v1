from openai_utils import get_llm_and_embeddings
from graph_utils import get_graph, clear_graph, add_pdf_to_graph, get_qa_chain

import tempfile

def process_pdf_service(file, neo4j_url, neo4j_username, neo4j_password, openai_api_key):
    try:
        llm, embeddings = get_llm_and_embeddings(openai_api_key)
        graph = get_graph(neo4j_url, neo4j_username, neo4j_password)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file)
            tmp_file_path = tmp_file.name
        clear_graph(graph)
        add_pdf_to_graph(tmp_file_path, "uploaded.pdf", llm, graph, embeddings, neo4j_url, neo4j_username, neo4j_password)
        return {"status": "success", "message": "PDF processed and graph updated."}
    except Exception as e:
        raise Exception(f"PDF processing failed: {e}")

def answer_question_service(question, neo4j_url, neo4j_username, neo4j_password, openai_api_key):
    try:
        llm, embeddings = get_llm_and_embeddings(openai_api_key)
        graph = get_graph(neo4j_url, neo4j_username, neo4j_password)
        qa = get_qa_chain(llm, graph)
        res = qa.invoke({"query": question})
        return res['result']
    except Exception as e:
        raise Exception(f"Question answering failed: {e}")
