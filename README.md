# ship-ai-sandbox

**AI Application Engineer / AI Product Engineer training sandbox** — учебная песочница для перехода из Full-stack разработки в инженерию AI-приложений.

Практические уроки: structured output, Pydantic-валидация, Function Calling (Tool Use), GigaChat API, Streamlit UI. Без «просто поговорить с чатом» — модель работает как предсказуемый кусок бэкенда.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![GigaChat](https://img.shields.io/badge/LLM-GigaChat-green.svg)](https://developers.sber.ru/docs/ru/gigachat/api/overview)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Pydantic](https://img.shields.io/badge/Validation-Pydantic-E92063.svg)](https://docs.pydantic.dev/)

---

## For whom / Для кого

- Full-stack / backend-разработчики, которые хотят стать **AI Application Engineer** или **AI Product Engineer**
- Тем, кто осваивает **LLM apps**, **tool calling**, **structured output**, дальше — **RAG**, **evals**, агенты
- Практикам: меньше теории, больше рабочих скриптов и UI

## What you learn / Чему учит

| Skill | Practice in this repo |
|---|---|
| System prompts as API contracts | Note classifier with strict JSON |
| Structured output + **Pydantic** | Validate LLM responses before UI/DB |
| **Function Calling / Tool Use** | Model calls `save_note` → SQLite |
| OpenAI-compatible LLM clients | GigaChat Freemium via `base_url` |
| Speech → text pipeline | Browser dictation (Web Speech API) |
| Local eval mindset | Edge-case prompts for urgency/category |

Roadmap ahead (planned lessons): **RAG** (chunking, embeddings, pgvector/Qdrant), **evals** (Ragas-style), orchestration (**LangGraph** / agents).

## Quick start

```bash
git clone https://github.com/anatoly-kulishov/ship-ai-sandbox.git
cd ship-ai-sandbox
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # paste GigaChat Authorization key
```

Get a key: [Sber Developers Studio](https://developers.sber.ru/studio) → GigaChat API (Freemium for individuals) → Authorization key.

```env
LLM_API_KEY=your-authorization-key
LLM_BASE_URL=https://api.giga.chat/v1
LLM_MODEL=GigaChat-2
LLM_OAUTH_URL=https://ngw.devices.sberbank.ru:9443/api/v2/oauth
LLM_SCOPE=GIGACHAT_API_PERS
LLM_SSL_VERIFY=false
```

### Run Lessons Hub (recommended)

```bash
./run.sh
# or: streamlit run app.py --server.port 8501
```

Open **http://localhost:8501** — switch lessons in the sidebar.

| Command | What |
|---|---|
| `./run.sh` | Hub (all lessons) |
| `./run.sh 01` | Lesson 01 only |
| `./run.sh 02` | Lesson 02 only |
| `python 01-note-sorter/categorize.py "купить хлеб сегодня"` | CLI classifier |
| `python 02-tool-use/agent.py "завтра созвон"` | CLI tool → SQLite |

## Lessons

### 01 · Note sorter (structured output)

**Skill:** turn an LLM into a typed function.

- Input: chaotic note text (or dictation)
- Output: `{ "category": "WORK|PERSONAL|SHOPPING", "urgent": bool }`
- Stack: system prompt → GigaChat → JSON → **Pydantic** → Streamlit

Formula: `prompt + JSON + Pydantic = predictable backend function`

### 02 · Tool Use (function calling)

**Skill:** model selects an action; **your code** executes the side effect.

- GigaChat `functions` API → `save_note(category, urgent, text)`
- Args validated with Pydantic
- Persisted to SQLite (`02-tool-use/notes.db`, gitignored)
- Original user text is stored (not a model rewrite)

Formula: `function calling = LLM chooses action, code runs it`

## Project layout

```
ship-ai-sandbox/
├── app.py                 # Lessons Hub (Streamlit)
├── pages/                 # Hub navigation
├── 01-note-sorter/        # Structured output + dictation
├── 02-tool-use/           # Tool calling → SQLite
├── lib/gigachat.py        # Shared OAuth + OpenAI-compatible client
├── run.sh                 # Convenient launcher
├── .env.example
└── requirements.txt
```

## Core principles (remember these)

1. **LLM ≠ chat for product** — need a contract (schema + allowed values).
2. **Prompt = business rules** — “срочно” yesterday is not urgent.
3. **Validate at the trust boundary** — Pydantic before UI/DB.
4. **`temperature=0`** for classification.
5. **STT and LLM are separate layers** — speech→text, then text→structure.
6. **Side effects only in your code** — never trust free-form model prose for writes.
7. **Provider is swappable** — `LLM_BASE_URL` + key + model (OpenAI-compatible).

## Stack

- **Python 3.12+**
- **GigaChat API** (OpenAI-compatible chat completions + functions)
- **Pydantic v2**
- **Streamlit** + `streamlit-mic-recorder`
- **SQLite** (lesson 02)
- **python-dotenv**, **requests**, **openai** SDK

## GitHub topics (suggested)

`ai-application-engineer` · `ai-product-engineer` · `llm` · `gigachat` · `structured-output` · `pydantic` · `function-calling` · `tool-use` · `streamlit` · `rag-learning` · `python` · `openai-compatible`

## License

Learning / personal sandbox. Use and fork freely for education.

---

**ship-ai-sandbox** — practice shipping AI features like an engineer, not like a chatbot demo.
