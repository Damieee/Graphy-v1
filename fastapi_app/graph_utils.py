from langchain.graphs import Neo4jGraph
from langchain.vectorstores import Neo4jVector
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain.prompts import PromptTemplate
from langchain.chains.graph_qa.cypher import GraphCypherQAChain

def get_graph(url, username, password):
    try:
        return Neo4jGraph(url=url, username=username, password=password)
    except Exception as e:
        raise Exception(f"Failed to connect to Neo4j: {e}")

def clear_graph(graph):
    try:
        cypher = "MATCH (n) DETACH DELETE n;"
        graph.query(cypher)
    except Exception as e:
        raise Exception(f"Failed to clear graph: {e}")

def add_pdf_to_graph(tmp_file_path, filename, llm, graph, embeddings, neo4j_url, neo4j_username, neo4j_password):
    try:
        loader = PyPDFLoader(tmp_file_path)
        pages = loader.load_and_split()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)
        docs = text_splitter.split_documents(pages)
        lc_docs = [
            Document(page_content=doc.page_content.replace("\n", ""), metadata={'source': filename})
            for doc in docs
        ]
        allowed_nodes = [
            "Threat", "Vulnerability", "Asset", "Control", "Attack", "Actor", "Incident",
            "Mitigation", "Standard", "Organization", "System", "Domain", "Impact", "Measure",
            "Policy", "Sector"
        ]
        allowed_relationships = [
            "HAS_VULNERABILITY", "TARGETS", "PROTECTS", "MITIGATES", "CAUSES", "AFFECTS",
            "BELONGS_TO", "COMPLIES_WITH", "RESPONDS_TO", "OCCURS_IN", "APPLIES_TO",
            "IMPLEMENTS", "MONITORS", "REPORTS", "ASSOCIATED_WITH"
        ]
        transformer = LLMGraphTransformer(
            llm=llm,
            allowed_nodes=allowed_nodes,
            allowed_relationships=allowed_relationships,
            node_properties=False,
            relationship_properties=False
        )
        graph_documents = transformer.convert_to_graph_documents(lc_docs)
        graph.add_graph_documents(graph_documents, include_source=True)
        Neo4jVector.from_existing_graph(
            embedding=embeddings,
            url=neo4j_url,
            username=neo4j_username,
            password=neo4j_password,
            database="neo4j",
            node_label="Cybersecurity",
            text_node_properties=["id", "text"],
            embedding_node_property="embedding",
            index_name="vector_index",
            keyword_index_name="entity_index",
            search_type="hybrid"
        )
    except Exception as e:
        raise Exception(f"Failed to add PDF to graph: {e}")

def get_qa_chain(llm, graph):
    try:
        template = """
        Task: Generate a Cypher statement to query the graph database.

        Instructions:
        Use only relationship types and properties provided in schema.
        Do not use other relationship types or properties that are not provided.

        schema:
        {schema}

        Note: Do not include explanations or apologies in your answers.
        Do not answer questions that ask anything other than creating Cypher statements.
        Do not include any text other than generated Cypher statements.

        Question: {question}"""
        question_prompt = PromptTemplate(
            template=template,
            input_variables=["schema", "question"]
        )
        qa = GraphCypherQAChain.from_llm(
            llm=llm,
            graph=graph,
            cypher_prompt=question_prompt,
            verbose=True,
            allow_dangerous_requests=True
        )
        return qa
    except Exception as e:
        raise Exception(f"Failed to create QA chain: {e}")
