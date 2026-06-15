def build_classification_prompt(
    statement: str,
    disciplines: list[str],
    subjects: dict[str, list[str]]
) -> str:
    
    disciplines_str = ", ".join(disciplines)
    
    subjects_lines = []
    for discipline, subject_list in subjects.items():
        subjects_str = ", ".join(subject_list)
        subjects_lines.append(f"  - {discipline}: {subjects_str}")
    subjects_formatted = "\n".join(subjects_lines)
    
    prompt = f"""Você é um classificador de questões de vestibular brasileiro.
Retorne APENAS um JSON válido, sem texto adicional.

DISCIPLINAS: {disciplines_str}

MATÉRIAS POR DISCIPLINA:
{subjects_formatted}

DIFICULDADE: Fácil, Médio ou Difícil

EXEMPLOS:
Enunciado: "Resolva x² - 5x + 6 = 0"
JSON: {{"discipline": "Matemática", "subject": "Álgebra", "difficulty": "Fácil"}}

Enunciado: "Um corpo de 2kg recebe força de 10N. Calcule a aceleração."
JSON: {{"discipline": "Física", "subject": "Mecânica", "difficulty": "Fácil"}}

Enunciado: "Qual produto se forma na combustão completa do metano?"
JSON: {{"discipline": "Química", "subject": "Reações Químicas", "difficulty": "Fácil"}}

Enunciado: "Em qual fase da mitose ocorre a separação dos cromátides-irmãs?"
JSON: {{"discipline": "Biologia", "subject": "Citologia", "difficulty": "Médio"}}

Enunciado: "Quais foram as consequências geopolíticas do bombardeio de Hiroshima em 1945?"
JSON: {{"discipline": "História", "subject": "Segunda Guerra Mundial", "difficulty": "Médio"}}

AGORA CLASSIFIQUE:
Enunciado: "{statement}"
JSON:"""
    
    return prompt