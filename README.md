# Cursinho Prisma — Serviço de IA

API de classificação automática de questões de vestibular usando inteligência artificial local (Ollama).

---

## O que este serviço faz

Recebe o enunciado de uma questão de vestibular e retorna automaticamente:
- **Disciplina** (ex: Física, Matemática, Química)
- **Matéria** (ex: Mecânica, Álgebra, Reações Químicas)
- **Nível de dificuldade** (Fácil, Médio ou Difícil)

As sugestões são geradas por IA e revisadas pelo professor antes de salvar no banco de dados.

---

## Tecnologias utilizadas

- **Python 3.12**
- **FastAPI** — framework para criação da API
- **Ollama** — execução local do modelo de IA
- **Modelo:** `llama3.2:3b`
- **Ngrok** — exposição pública da API
- **Docker** — containerização (opcional)

---

## Pré-requisitos

Antes de rodar o projeto, você precisa ter instalado:

- [Python 3.12+](https://www.python.org/downloads/)
- [Ollama](https://ollama.com/download)
- [Ngrok](https://ngrok.com/download) (conta gratuita necessária)
- [Git](https://git-scm.com/downloads)

---

## Instalação e configuração

### 1. Clone o repositório

```bash
git clone https://github.com/Orlandoo1234/cursinho-prisma-ai.git
cd cursinho-prisma-ai
```

### 2. Crie e ative o ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
HOST=0.0.0.0
PORT=8000
OLLAMA_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434
```

> ⚠️ O arquivo `.env` não está no repositório por segurança. Você precisa criá-lo manualmente.

### 5. Baixe o modelo de IA

```bash
ollama pull llama3.2:3b
```

> O download tem aproximadamente 2 GB. Aguarde a conclusão.

---

## Como rodar

Você precisará de **dois terminais abertos simultaneamente.**

### Terminal 1 — Servidor FastAPI

Com o ambiente virtual ativado:

```bash
python main.py
```

O servidor vai iniciar em `http://localhost:8000`.

### Terminal 2 — Ngrok (exposição pública)

```bash
ngrok http 127.0.0.1:8000
```

O Ngrok vai gerar uma URL pública como:
```
https://xxxx-xxxx.ngrok-free.dev
```

> ⚠️ Essa URL muda toda vez que o Ngrok é reiniciado. Comunique a nova URL ao time do ASP.NET sempre que reiniciar.

---

## Endpoints disponíveis

### `GET /`
Confirma que a API está online.

**Resposta:**
```json
{
    "service": "Cursinho Prisma AI Service",
    "status": "online",
    "version": "1.0.0"
}
```

---

### `GET /health`
Verifica se o Ollama está rodando e o modelo está disponível.

**Resposta:**
```json
{
    "status": "ok",
    "ollama_running": true,
    "model_available": true,
    "model_name": "llama3.2:3b"
}
```

---

### `POST /classify`
Classifica uma questão de vestibular.

**Body:**
```json
{
    "statement": "Um corpo de massa 5kg é submetido a uma força de 20N. Qual é a aceleração?",
    "available_disciplines": ["Matemática", "Física", "Química"],
    "available_subjects": {
        "Matemática": ["Álgebra", "Geometria", "Trigonometria"],
        "Física": ["Mecânica", "Termodinâmica", "Óptica"],
        "Química": ["Química Orgânica", "Reações Químicas"]
    }
}
```

**Resposta:**
```json
{
    "discipline": "Física",
    "subject": "Mecânica",
    "difficulty": "Fácil",
    "confidence": "high",
    "ai_available": true,
    "error_message": null
}
```

**Campos da resposta:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `discipline` | string ou null | Disciplina sugerida pela IA |
| `subject` | string ou null | Matéria sugerida pela IA |
| `difficulty` | string ou null | "Fácil", "Médio" ou "Difícil" |
| `confidence` | string | "high", "medium" ou "low" |
| `ai_available` | boolean | `false` se o Ollama estiver offline |
| `error_message` | string ou null | Mensagem de erro, se houver |

---

## Testando a API

### Pelo navegador (documentação interativa)

Acesse `http://localhost:8000/docs` para testar os endpoints diretamente pelo navegador.

### Pelos testes automatizados

Com o servidor rodando, execute em outro terminal:

```bash
python test_classifier.py
```

O script testa 5 questões de disciplinas diferentes e exibe o aproveitamento. A meta é **≥ 70% de acerto**.

---

## Comportamento quando a IA está offline

Se o Ollama não estiver disponível, a API **não trava** — ela retorna:

```json
{
    "discipline": null,
    "subject": null,
    "difficulty": null,
    "confidence": "low",
    "ai_available": false,
    "error_message": "Serviço de IA indisponível"
}
```

O front-end deve tratar esse caso deixando os campos em branco para o professor preencher manualmente.

---

## Integração com ASP.NET

O ASP.NET deve:

1. Buscar as disciplinas e matérias do banco de dados
2. Enviar `POST /classify` com o enunciado e as listas
3. Verificar o campo `ai_available` antes de usar a resposta
4. Preencher os campos do formulário com os valores retornados
5. Deixar o professor revisar antes de salvar

**Timeout recomendado:** 30 segundos (o modelo pode demorar em hardware limitado).

---

## Estrutura do projeto

```
cursinho-prisma-ai/
├── main.py             # Ponto de entrada da API
├── classifier.py       # Comunicação com o Ollama
├── prompt_builder.py   # Monta o prompt enviado para a IA
├── validator.py        # Valida e limpa a resposta da IA
├── schemas.py          # Formatos de entrada e saída
├── test_classifier.py  # Script de testes automatizados
├── Dockerfile          # Configuração Docker
├── docker-compose.yml  # Configuração Docker Compose
├── requirements.txt    # Dependências Python
└── .gitignore
```

---

## Docker (opcional)

### Build e execução

```bash
docker build -t cursinho-prisma-ai .
docker-compose up -d
```

> ⚠️ **Pendência:** a comunicação entre o container e o Ollama no Windows requer configuração adicional. Será resolvido na Entrega 3 junto com o servidor de produção Linux.

---

## Resultados dos testes

| Teste | Disciplina | Acerto |
|-------|-----------|--------|
| Segunda Lei de Newton | Física | ✅ |
| Equação do 2° grau | Matemática | ✅ |
| Reação de combustão | Química | ✅ |
| Mitose | Biologia | ✅ |
| Segunda Guerra Mundial | História | ✅ |

**Aproveitamento: 5/5 (100%)**  
**Tempo médio de resposta: ~3s**

---

## Limitações conhecidas

- A IA não garante 100% de acerto — revisão humana é obrigatória antes de salvar
- O tempo de resposta pode variar de 1 a 15 segundos dependendo do hardware
- A URL do Ngrok muda ao reiniciar (plano gratuito)
- Docker com Ollama pendente de configuração no Windows

---

## Autores

Projeto desenvolvido para a disciplina **Oficina de Integração 1 — ES46F-ES61**  
UTFPR — Cornélio Procópio, 2026

- Gustavo Pukanski Schatzmann
- Igor Busquim de Moraes
- Luiz Fernando Moreira Domenico
- Orlando Cardoso Neto
- Rafael Spitzer Cardoso da Silva
