from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str
    neo4j_url: str
    neo4j_username: str
    neo4j_password: str
    openai_api_key: str

class QuestionResponse(BaseModel):
    answer: str
