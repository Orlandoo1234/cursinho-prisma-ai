from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from dotenv import load_dotenv

from schemas import ClassificationRequest, ClassificationResponse
from classifier import classify_question, check_ollama_health

load_dotenv()

app = FastAPI(
    title="Cursinho Prisma — Serviço de IA",
    description="API para classificação automática de questões de vestibular",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"[API] {request.method} {request.url.path} — {process_time:.3f}s")
    return response


@app.get("/")
def root():
    return {
        "service": "Cursinho Prisma AI Service",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    ollama_status = check_ollama_health()
    status = "ok" if ollama_status["ollama_running"] and ollama_status["model_available"] else "degraded"
    return {"status": status, **ollama_status}


@app.post("/classify", response_model=ClassificationResponse)
def classify(request: ClassificationRequest):
    if not request.statement or len(request.statement.strip()) < 15:
        raise HTTPException(
            status_code=400,
            detail="O enunciado deve ter pelo menos 15 caracteres"
        )
    if not request.available_disciplines:
        raise HTTPException(
            status_code=400,
            detail="A lista de disciplinas não pode estar vazia"
        )
    return classify_question(request)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"[ERROR] Erro não tratado: {type(exc).__name__}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "discipline": None,
            "subject": None,
            "difficulty": None,
            "confidence": "low",
            "ai_available": False,
            "error_message": "Erro interno no serviço"
        }
    )


if __name__ == "__main__":
    import uvicorn
    print("=" * 50)
    print("  Cursinho Prisma — Serviço de IA")
    print("=" * 50)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)