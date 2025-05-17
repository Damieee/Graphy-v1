from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from schemas import QuestionRequest, QuestionResponse
from services import process_pdf_service, answer_question_service
from config import settings

app = FastAPI(
    title="Graphy v1 - FastAPI",
    description="A modular FastAPI backend for PDF-to-Neo4j GraphRAG with OpenAI and LangChain.",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Graphy v1 FastAPI backend."}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

@app.post("/upload_pdf/")
async def upload_pdf(
    file: UploadFile = File(...),
    neo4j_url: str = Form(...),
    neo4j_username: str = Form(...),
    neo4j_password: str = Form(...),
    openai_api_key: str = Form(...)
):
    try:
        file_bytes = await file.read()
        result = process_pdf_service(file_bytes, neo4j_url, neo4j_username, neo4j_password, openai_api_key)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(
    req: QuestionRequest,
):
    try:
        answer = answer_question_service(
            req.question,
            req.neo4j_url,
            req.neo4j_username,
            req.neo4j_password,
            req.openai_api_key
        )
        return QuestionResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', reload=True, host="0.0.0.0", port=8000)