import requests
import json
import time

BASE_URL = "http://localhost:8000"

DISCIPLINES = [
    "Matemática", "Física", "Química", "Biologia",
    "História", "Geografia", "Língua Portuguesa"
]

SUBJECTS = {
    "Matemática": ["Álgebra", "Geometria", "Trigonometria", "Funções", "Probabilidade e Estatística"],
    "Física": ["Mecânica", "Termodinâmica", "Óptica", "Eletrostática", "Eletrodinâmica"],
    "Química": ["Química Orgânica", "Reações Químicas", "Soluções", "Eletroquímica"],
    "Biologia": ["Citologia", "Genética", "Ecologia", "Evolução", "Fisiologia Humana"],
    "História": ["Brasil Colônia", "Brasil Império", "Segunda Guerra Mundial", "Guerra Fria"],
    "Geografia": ["Geopolítica", "Climatologia", "Hidrografia", "Urbanização"],
    "Língua Portuguesa": ["Gramática", "Interpretação de Texto", "Redação"]
}

TEST_CASES = [
    {
        "name": "Física - Segunda Lei de Newton",
        "statement": "Um corpo de 2kg é submetido a uma força de 10N. Qual é a aceleração?",
        "expected_discipline": "Física",
        "expected_subject": "Mecânica"
    },
    {
        "name": "Matemática - Equação do 2° grau",
        "statement": "Resolva a equação x² - 5x + 6 = 0 e encontre as raízes.",
        "expected_discipline": "Matemática",
        "expected_subject": "Álgebra"
    },
    {
        "name": "Química - Reação de combustão",
        "statement": "Na reação de combustão completa do metano CH4, quais são os produtos formados?",
        "expected_discipline": "Química",
        "expected_subject": "Reações Químicas"
    },
    {
        "name": "Biologia - Mitose",
        "statement": "Durante a divisão celular por mitose, em qual fase ocorre a separação dos cromátides-irmãs?",
        "expected_discipline": "Biologia",
        "expected_subject": "Citologia"
    },
    {
        "name": "História - Segunda Guerra",
        "statement": "O bombardeio atômico de Hiroshima e Nagasaki em 1945 foi determinante para o fim da Segunda Guerra Mundial. Quais foram as consequências geopolíticas?",
        "expected_discipline": "História",
        "expected_subject": "Segunda Guerra Mundial"
    }
]


def run_test(test_case):
    payload = {
        "statement": test_case["statement"],
        "available_disciplines": DISCIPLINES,
        "available_subjects": SUBJECTS
    }
    start = time.time()
    try:
        response = requests.post(f"{BASE_URL}/classify", json=payload, timeout=60)
        elapsed = time.time() - start
        if response.status_code == 200:
            result = response.json()
            discipline_ok = result["discipline"] == test_case["expected_discipline"]
            subject_ok = result["subject"] == test_case.get("expected_subject")
            return {
                "name": test_case["name"],
                "status": "PASSOU" if discipline_ok else "FALHOU",
                "elapsed": f"{elapsed:.2f}s",
                "got_discipline": result["discipline"],
                "expected_discipline": test_case["expected_discipline"],
                "got_subject": result["subject"],
                "expected_subject": test_case.get("expected_subject"),
                "difficulty": result["difficulty"],
                "confidence": result["confidence"],
                "discipline_correct": discipline_ok,
                "subject_correct": subject_ok
            }
    except Exception as e:
        return {"name": test_case["name"], "status": "ERRO", "elapsed": "N/A", "error": str(e)}


def main():
    print("\n" + "="*60)
    print("  TESTES DO SERVIÇO DE IA — CURSINHO PRISMA")
    print("="*60)

    try:
        health = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"\n✓ Servidor online")
    except:
        print("\n✗ Servidor não está rodando! Execute: python main.py")
        return

    print(f"\nExecutando {len(TEST_CASES)} testes...\n")

    results = []
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"[{i}/{len(TEST_CASES)}] {test_case['name']}...", end=" ", flush=True)
        result = run_test(test_case)
        results.append(result)
        print(f"{result['status']} ({result.get('elapsed', 'N/A')})")

    print("\n" + "="*60)
    print("  RESUMO DOS RESULTADOS")
    print("="*60)

    passed = sum(1 for r in results if r["status"] == "PASSOU")
    total = len(results)

    for result in results:
        symbol = "✓" if result["status"] == "PASSOU" else "✗"
        print(f"\n{symbol} {result['name']}")
        print(f"   Status:      {result['status']}")
        print(f"   Tempo:       {result.get('elapsed', 'N/A')}")
        if "got_discipline" in result:
            cd = "✓" if result["discipline_correct"] else "✗"
            cs = "✓" if result.get("subject_correct") else "✗"
            print(f"   Disciplina:  {cd} Esperado={result['expected_discipline']}, Obtido={result['got_discipline']}")
            print(f"   Matéria:     {cs} Esperado={result['expected_subject']}, Obtido={result['got_subject']}")
            print(f"   Dificuldade: {result.get('difficulty')} (confiança: {result.get('confidence')})")

    print("\n" + "="*60)
    accuracy = (passed/total*100) if total > 0 else 0
    print(f"  APROVEITAMENTO: {passed}/{total} ({accuracy:.0f}%)")
    if accuracy >= 70:
        print("  ✓ Meta atingida!")
    else:
        print("  ✗ Meta não atingida — ajuste o prompt")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()