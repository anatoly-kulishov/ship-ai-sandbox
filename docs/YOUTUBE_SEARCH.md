# Что искать на YouTube (термины и запросы)

Поиски под **средний рыночный план** [LEARNING_PLAN.md](./LEARNING_PLAN.md) (GenAI / AI Application / LLM Engineer).  
Сначала **русский**, если мало — **english**.

Формат: `тема` → готовые строки для поиска.

---

## Фаза A · Фундамент LLM

| Тема | Искать RU | Искать EN |
|---|---|---|
| LLM вообще | `что такое LLM простыми словами` | `what is an LLM explained` |
| Токены | `токены нейросеть LLM` | `LLM tokens tokenization explained` |
| Контекстное окно | `контекстное окно LLM` | `context window LLM explained` |
| System prompt | `system prompt eng` / `системный промпт` | `system prompt vs user prompt` |
| Temperature | `temperature LLM что это` | `LLM temperature top_p explained` |
| Structured output | `structured output LLM JSON` | `LLM structured output JSON schema` |
| Pydantic | `Pydantic Python курс` | `Pydantic v2 tutorial` |
| Function calling | `function calling LLM` / `tool use LLM` | `OpenAI function calling tutorial` |
| Tool use / агенты intro | `AI agents tool use просто` | `LLM tool use explained` |

---

## Фаза B · Локальный инференс

| Тема | Искать RU | Искать EN |
|---|---|---|
| Ollama | `Ollama установка туториал` | `Ollama tutorial beginner` |
| Локальная LLM | `локальная LLM на ПК` | `run LLM locally` |
| Llama / Qwen / Mistral | `Llama 3 Qwen сравнение` | `Llama 3 vs Qwen vs Mistral` |
| OpenAI-compatible API | `OpenAI compatible API Ollama` | `OpenAI compatible endpoint Ollama` |
| Инференс | `инференс нейросети что это` | `what is model inference` |
| GGUF | `GGUF что это` | `GGUF format explained` |
| Квантизация | `квантизация нейросетей LLM` | `LLM quantization Q4 Q5 Q8` |
| AWQ / GPTQ | `AWQ GPTQ квантизация` | `AWQ vs GPTQ vs GGUF` |
| VRAM / RAM для моделей | `сколько VRAM нужно для LLM` | `LLM VRAM requirements 7B 14B` |
| vLLM | `vLLM туториал` | `vLLM tutorial deploy` |
| TGI (Text Generation Inference) | `Hugging Face TGI` | `Hugging Face TGI tutorial` |
| TensorRT-LLM | `TensorRT-LLM обзор` | `TensorRT-LLM getting started` |

---

## Фаза C · Backend

| Тема | Искать RU | Искать EN |
|---|---|---|
| FastAPI | `FastAPI с нуля курс` | `FastAPI tutorial full course` |
| Uvicorn | `uvicorn FastAPI` | `uvicorn ASGI explained` |
| REST API | `REST API простыми словами` | `REST API for beginners` |
| Pydantic + FastAPI | `FastAPI Pydantic модели` | `FastAPI Pydantic request body` |
| Async Python | `async await Python просто` | `Python asyncio explained` |
| httpx / async HTTP | `httpx async Python` | `httpx vs requests async` |
| PostgreSQL | `PostgreSQL для начинающих` | `PostgreSQL crash course` |
| SQLAlchemy | `SQLAlchemy 2.0 туториал` | `SQLAlchemy 2.0 tutorial` |
| Микросервисы intro | `микросервисы Python FastAPI` | `Python microservices FastAPI` |

---

## Фаза D · RAG (самое важное)

| Тема | Искать RU | Искать EN |
|---|---|---|
| RAG | `RAG Retrieval Augmented Generation простыми словами` | `RAG explained simply` |
| Зачем RAG | `зачем нужен RAG LLM галлюцинации` | `RAG vs fine-tuning` |
| Chunking | `chunking RAG текст` | `text chunking for RAG` |
| Overlap чанков | `chunk overlap RAG` | `chunk size overlap RAG` |
| Embeddings | `эмбеддинги что это` | `word embeddings vs sentence embeddings` |
| Cosine similarity | `косинусное сходство векторы` | `cosine similarity explained` |
| Векторная БД | `векторная база данных` | `vector database explained` |
| pgvector | `pgvector PostgreSQL туториал` | `pgvector tutorial` |
| Qdrant | `Qdrant туториал` | `Qdrant getting started` |
| Chroma / Milvus | `ChromaDB туториал` / `Milvus векторная БД` | `ChromaDB tutorial` / `Milvus tutorial` |
| Hybrid search | `hybrid search RAG BM25` | `hybrid search dense sparse RAG` |
| Reranking | `reranker RAG` | `reranking in RAG pipelines` |
| Citations / grounding | `RAG цитирование источников` | `RAG citations grounding` |
| LangChain | `LangChain RAG туториал` | `LangChain RAG tutorial 2024` |
| LlamaIndex | `LlamaIndex туториал` | `LlamaIndex beginner tutorial` |
| Парсинг документов | `парсинг PDF Python RAG` | `PDF parsing for RAG Unstructured` |

---

## Фаза E · Docker и «для сотрудников»

| Тема | Искать RU | Искать EN |
|---|---|---|
| Docker | `Docker с нуля` | `Docker tutorial for beginners` |
| Dockerfile | `Dockerfile пример Python` | `Dockerfile Python FastAPI` |
| docker-compose | `docker-compose туториал` | `docker compose tutorial` |
| Volumes / networks | `docker volumes networks` | `docker volumes explained` |
| GPU в Docker | `nvidia docker GPU` | `NVIDIA Container Toolkit tutorial` |
| nvidia-smi | `nvidia-smi как пользоваться` | `nvidia-smi explained` |
| Open WebUI | `Open WebUI Ollama` | `Open WebUI Ollama setup` |
| Dify | `Dify AI туториал` | `Dify AI tutorial self host` |
| AnythingLLM | `AnythingLLM установка` | `AnythingLLM tutorial` |

---

## Фаза F · Evals, ИБ, роль инженера

| Тема | Искать RU | Искать EN |
|---|---|---|
| LLM evals | `оценка качества LLM` | `LLM evaluation benchmarks` |
| RAG evaluation | `оценка RAG пайплайна` | `RAG evaluation faithfulness` |
| Ragas | `Ragas LLM evaluation` | `Ragas RAGAS tutorial` |
| Галлюцинации | `галлюцинации нейросетей` | `LLM hallucinations explained` |
| Prompt injection | `prompt injection атака` | `prompt injection explained` |
| On-prem AI | `on-premise LLM` | `on-prem LLM enterprise` |
| Data privacy LLM | `безопасность LLM персональные данные` | `LLM data privacy enterprise` |
| RBAC | `RBAC простыми словами` | `RBAC explained` |
| AI Application Engineer | `AI engineer чем занимается` | `AI application engineer role` |
| MLOps vs LLMOps | `LLMOps что это` | `LLMOps vs MLOps` |
| Langfuse / tracing | `Langfuse туториал` | `Langfuse tutorial LLM` |
| LLM-as-a-Judge | `LLM as a judge` | `LLM-as-a-judge evaluation` |

---

## Фаза · Agents и промпт-паттерны

| Тема | Искать RU | Искать EN |
|---|---|---|
| Few-shot | `few shot prompting` | `few-shot prompting explained` |
| Chain of Thought | `chain of thought prompting` | `chain of thought CoT explained` |
| ReAct | `ReAct agent LLM` | `ReAct prompting agents` |
| AI agents | `AI агенты LangChain` | `LangChain agents tutorial` |
| Multi-agent (обзор) | `multi agent LLM обзор` | `multi agent systems LLM overview` |

---

## Модели и экосистема (фоном)

| Тема | Искать |
|---|---|
| Hugging Face | `Hugging Face Hub tutorial` / `Hugging Face что это` |
| Transformers library | `Hugging Face transformers tutorial` |
| Open-source LLMs 2025/2026 | `best open source LLM 2026` |
| Fine-tuning (позже, не раньше RAG) | `LoRA fine-tuning explained` / `LoRA дообучение` |
| LoRA / QLoRA | `QLoRA explained simply` |

---

## Порядок просмотра (не прыгай)

1. LLM + tokens + context + temperature + structured output  
2. function calling → Ollama + local LLM  
3. FastAPI + asyncio + Postgres  
4. RAG explained → chunking → embeddings → Qdrant/pgvector  
5. LangChain/LlamaIndex **после** своего RAG  
6. ReAct / agents  
7. Docker compose + Open WebUI/Dify  
8. Evals + Langfuse + security  
9. LoRA / QLoRA (только после RAG)

---

## Каналы (ориентиры, не реклама)

Ищи по авторам/каналам: **Andrej Karpathy** (основы), **freeCodeCamp** (длинные туториалы), **NetworkChuck / TechWorld with Nana** (Docker), русскоязычные разборы RAG/Ollama по свежим роликам с датой 2024–2026.

Критерий хорошего ролика: есть **схема на доске** + **демо в терминале**, а не только слайды.
