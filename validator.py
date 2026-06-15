import json
import re
from schemas import ClassificationResponse


def parse_ai_response(
    raw_response: str,
    disciplines: list[str],
    subjects: dict[str, list[str]]
) -> ClassificationResponse:
    
    json_match = re.search(r'\{[^{}]*\}', raw_response, re.DOTALL)
    
    if not json_match:
        print(f"[VALIDATOR] Nenhum JSON encontrado: {raw_response[:200]}")
        return ClassificationResponse(
            confidence="low",
            error_message="IA não retornou JSON válido"
        )
    
    json_text = json_match.group()
    
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"[VALIDATOR] Erro no JSON: {e}")
        return ClassificationResponse(
            confidence="low",
            error_message="JSON malformado na resposta da IA"
        )
    
    raw_discipline = data.get("discipline")
    validated_discipline = validate_discipline(raw_discipline, disciplines)
    
    raw_subject = data.get("subject")
    validated_subject = None
    if validated_discipline:
        validated_subject = validate_subject(raw_subject, validated_discipline, subjects)
    
    raw_difficulty = data.get("difficulty")
    validated_difficulty = validate_difficulty(raw_difficulty)
    
    filled_count = sum([
        validated_discipline is not None,
        validated_subject is not None,
        validated_difficulty is not None
    ])
    
    if filled_count == 3:
        confidence = "high"
    elif filled_count >= 1:
        confidence = "medium"
    else:
        confidence = "low"
    
    print(f"[VALIDATOR] disciplina={validated_discipline}, matéria={validated_subject}, dificuldade={validated_difficulty}, confiança={confidence}")
    
    return ClassificationResponse(
        discipline=validated_discipline,
        subject=validated_subject,
        difficulty=validated_difficulty,
        confidence=confidence
    )


def validate_discipline(raw_value, disciplines):
    if not raw_value or raw_value == "null":
        return None
    if raw_value in disciplines:
        return raw_value
    raw_lower = raw_value.lower().strip()
    for discipline in disciplines:
        if discipline.lower() == raw_lower:
            return discipline
    print(f"[VALIDATOR] Disciplina '{raw_value}' não encontrada")
    return None


def validate_subject(raw_value, discipline, subjects):
    if not raw_value or raw_value == "null":
        return None
    valid_subjects = subjects.get(discipline, [])
    if raw_value in valid_subjects:
        return raw_value
    raw_lower = raw_value.lower().strip()
    for subject in valid_subjects:
        if subject.lower() == raw_lower:
            return subject
    print(f"[VALIDATOR] Matéria '{raw_value}' não encontrada")
    return None


def validate_difficulty(raw_value):
    valid = ["Fácil", "Médio", "Difícil"]
    if not raw_value or raw_value == "null":
        return None
    if raw_value in valid:
        return raw_value
    mapping = {
        "fácil": "Fácil", "facil": "Fácil", "easy": "Fácil",
        "médio": "Médio", "medio": "Médio", "medium": "Médio",
        "difícil": "Difícil", "dificil": "Difícil", "hard": "Difícil"
    }
    return mapping.get(raw_value.lower().strip(), None)