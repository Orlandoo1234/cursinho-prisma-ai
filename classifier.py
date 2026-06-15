import ollama
import time
from schemas import ClassificationRequest, ClassificationResponse
from prompt_builder import build_classification_prompt
from validator import parse_ai_response

OLLAMA_MODEL = "llama3.2:3b"

MODEL_OPTIONS = {
    "temperature": 0.1,
    "num_predict": 200,
}


def classify_question(request: ClassificationRequest) -> ClassificationResponse:
    
    start_time = time.time()
    print(f"[CLASSIFIER] Iniciando classificação...")
    print(f"[CLASSIFIER] Enunciado: {request.statement[:100]}...")
    
    prompt = build_classification_prompt(
        statement=request.statement,
        disciplines=request.available_disciplines,
        subjects=request.available_subjects
    )
    
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            options=MODEL_OPTIONS
        )
        
        raw_text = response["message"]["content"]
        elapsed_time = time.time() - start_time
        
        print(f"[CLASSIFIER] Resposta recebida em {elapsed_time:.2f}s")
        print(f"[CLASSIFIER] Resposta bruta: {raw_text[:300]}")
        
        return parse_ai_response(
            raw_response=raw_text,
            disciplines=request.available_disciplines,
            subjects=request.available_subjects
        )
        
    except Exception as e:
        print(f"[CLASSIFIER] Erro: {type(e).__name__}: {e}")
        return ClassificationResponse(
            ai_available=False,
            confidence="low",
            error_message="Serviço de IA indisponível"
        )


def check_ollama_health() -> dict:
    try:
        models = ollama.list()
        model_names = [m["model"] for m in models.get("models", [])]
        model_available = any(OLLAMA_MODEL in name for name in model_names)
        return {
            "ollama_running": True,
            "model_available": model_available,
            "model_name": OLLAMA_MODEL
        }
    except Exception as e:
        return {
            "ollama_running": False,
            "model_available": False,
            "model_name": OLLAMA_MODEL,
            "error": str(e)
        }