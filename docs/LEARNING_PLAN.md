# План обучения: AI Application / LLM Engineer (средний по рынку)

Цель: закрыть **пересечение большинства вакансий** вроде:
- AI/LLM Engineer (on-prem, RAG, FastAPI, Docker)
- Python GenAI Developer (LangChain, agents, vector DB, cloud + open-source)
- не полный Senior MLE с Spark/Kubeflow (это отдельный трек «после»)

Роль, на которую целимся:

> **AI Application Engineer** — встраивает LLM в продукт: API, RAG, tools/agents, качество, деплой.

Принцип: один навык за урок, простой язык, пример в `ship-ai-sandbox`. Темп любой.

Видео-запросы: [YOUTUBE_SEARCH.md](./YOUTUBE_SEARCH.md) · конспекты: [01](./01-note-sorter.md), [02](./02-tool-use.md), [03](./03-ollama.md), [04](./04-gym-plan.md), [05](./05-rag.md), [06](./06-gguf.md)

**Новый чат:** снимок прогресса и прод-моста - [CONTINUE.md](./CONTINUE.md).

---

## Что требует «средний рынок» (ядро)

Почти везде просят комбинацию:

| Блок | Технологии | Вес |
|---|---|---|
| LLM-основы | prompts, tokens, temperature, structured output | must |
| Tools / agents | function calling → потом ReAct/agents | must |
| Backend | **Python, FastAPI, asyncio, Pydantic** | must |
| RAG | chunking, embeddings, vector DB, citations | must |
| Оркестрация | **LangChain или LlamaIndex** (после своего RAG) | must |
| Модели | облако (OpenAI-совместимое) **и** local (Ollama) | must |
| Данные | **PostgreSQL**, часто Redis | must |
| Delivery | **Docker**, compose; K8s — база | must / plus |
| Качество | evals, анти-галлюцинации, tracing (Langfuse) | must |
| Fine-tune | LoRA/QLoRA — обзор + один мини-опыт | plus → часто must на Middle+ |
| Heavy MLOps | Airflow, Kafka, Spark, Triton | **не в среднем плане** (фаза «После рынка») |

### Покрытие вакансий

| Тип вакансии | Насколько закрывает этот план |
|---|---|
| GenAI / Python LLM (Neuro.net и аналоги) | **высокий** |
| AI/LLM Engineer on-prem (РЖД и аналоги) | **высокий** |
| Product AI / AI Application Engineer | **высокий** |
| ML/AI Engineer fintech (WB-like) | **средний** → нужна фаза «После» |
| Research / Core LLM training | низкий (другая профессия) |

---

## Уже закрыто в sandbox

| Урок | Навык | Рынок |
|---|---|---|
| 01 | Structured output + Pydantic | must |
| 02 | Tool use → SQLite | must |
| 03 | Ollama local LLM (см. `03-ollama/`) | must |
| 04 | Gym plan structured + catalog whitelist (`04-gym-plan/`) | must (Repdraft bridge) |
| 05 | RAG embeddings + cosine по каталогу (`05-rag/`) | must (фаза D урок 11) |
| 06 | GGUF / квантизация, модель под RAM (`06-gguf/`) | must (фаза B урок 04) |

---

## Карта цели

```
        ┌─ cloud LLM (GigaChat / OpenAI-compatible)
User ──► FastAPI (async) ──┤
        └─ local LLM (Ollama → позже vLLM)
                 │
         tools / agents
                 │
              RAG layer
         chunk → embed → Qdrant/pgvector
                 │
         Postgres (+ Redis)
                 │
         Docker compose
                 │
         evals + tracing
```

Формула среднего рынка:

> **FastAPI + RAG + tools/agents + (cloud ∪ local LLM) + Docker + evals**

---

## Фаза 0 · Уже есть (Full-stack → AI)

Повтори коротко, если нужно: Python, Git, HTTP, SQL-база идейно.

---

## Фаза A · Фундамент LLM-продукта ✅ почти

| # | Тема | Готово, когда |
|---|---|---|
| A1 | Tokens, context window | объясняешь «почему обрезало» |
| A2 | Temperature / top_p | для классификации ставишь 0 |
| A3 | System vs user prompt | пишешь контракт API |
| A4 | Structured output + Pydantic | урок 01 |
| A5 | Function calling / tools | урок 02 |
| A6 | Prompt-паттерны: few-shot, CoT, ReAct (теория) | узнаёшь по названию и применяешь few-shot |

**Срок:** 1–2 недели (с учётом 01–02).

---

## Фаза B · Провайдеры моделей (облако + локально)

Рынок хочет **оба** навыка: уметь облако и уметь local.

### Урок 03 · Local LLM (Ollama) ✅ в репо

- Папка `03-ollama/`, Hub-страница **03 Ollama**
- Переключение через `.env` (`LLM_BASE_URL`)
- См. [03-ollama.md](./03-ollama.md)

### Урок 04 · GGUF / квантизация (обзор) ✅ в репо

- Папка `06-gguf/` (номер 04 в sandbox занят gym-plan), Hub **06 GGUF**
- Q4/Q5/Q8, 7B vs 14B, RAM/VRAM trade-off, калькулятор без pull
- См. [06-gguf.md](./06-gguf.md)

**Готово:** выбираешь модель под свой Mac/ПК осознанно.

#### Кандидаты на локальный прогон (позже)

- **PrismML Ternary Bonsai 2 27B** — сверхсжатый Qwen3.8-27B (~5.9 ГБ vs ~54 ГБ FP16), заявленный retention ~98% overall / ~99% coding; multimodal, context до 262K. Сравнить с текущим `qwen2.5:3b` на уроках 03/04 (JSON plan + RU brief). Не default, пока не прогнали smoke на своём железе.

### Урок 05 · Мульти-провайдер в коде

- Один клиент: `LLM_BASE_URL` → GigaChat **или** Ollama
- В README: как переключать

**Готово:** одна команда/env меняет провайдера.

**Срок фазы B:** 2–4 недели.

---

## Фаза C · Backend LLM-gateway (must везде)

### Урок 06 · FastAPI + Pydantic

`POST /classify`, `POST /chat` → Swagger / curl

### Урок 07 · asyncio + async OpenAI client

Почему LLM-gateway должен быть async

### Урок 08 · PostgreSQL

Заметки/диалоги/логи в Postgres (не только SQLite)

### Урок 09 · Redis (коротко)

Кэш эмбеддингов / rate limit / session — один простой use-case

**Срок фазы C:** 4–7 недель.

---

## Фаза D · RAG (ядро рынка)

Делай **сначала руками**, потом фреймворк.

| Урок | Тема | Готово |
|---|---|---|
| 10 | Chunking + overlap | видишь чанки с `source` |
| 11 | Embeddings + cosine | **05-rag/** top-k по brief зала |
| 12 | Vector DB: **Qdrant или pgvector** (один!) | top-k по вопросу |
| 13 | Full RAG + citations + «не знаю» | чат по docs |
| 14 | LangChain **или** LlamaIndex | тот же RAG на фреймворке |

**Срок фазы D:** 6–10 недель.

---

## Фаза E · Agents (после tools + RAG)

### Урок 15 · Agent loop

- ReAct: мысль → tool → наблюдение → ответ
- 2–3 tools: поиск по базе, сохранить заметку, калькулятор/HTTP

### Урок 16 · Multi-step assistant

- Один сценарий «помощник по документам + запись задачи»
- Без фанатизма multi-agent frameworks

**Срок:** 3–5 недель.

---

## Фаза F · Delivery

| Урок | Тема | Готово |
|---|---|---|
| 17 | Dockerfile + docker-compose | API + Postgres (+ vector) одной командой |
| 18 | Open WebUI или Dify | UI для «сотрудника» на твоём стеке |
| 19 | K8s basics (теория + мини-деплой по желанию) | знаешь pod/service/deploy |

**Срок:** 4–6 недель.

---

## Фаза G · Качество и наблюдаемость

| Урок | Тема | Готово |
|---|---|---|
| 20 | Evals: 30 вопросов, pass/fail, faithfulness | регрессия при смене chunk size |
| 21 | Tracing: Langfuse (или аналог) | видишь prompt/completion/latency |
| 22 | Security basics | API key, маскирование, «данные не утекают» в README |

**Срок:** 3–5 недель.

---

## Фаза H · Fine-tuning light (Middle+ рынок)

Не Deep Learning PhD — практический минимум:

| Урок | Тема | Готово |
|---|---|---|
| 23 | Hugging Face Transformers (load + generate) | прогнал модель локально/в колабе |
| 24 | LoRA / QLoRA: один маленький датасет | дообучил tiny-модель, сравнил до/после |
| 25 | Когда fine-tune, а когда RAG/prompt | чёткое правило в конспекте |

**Срок:** 3–6 недель.

---

## Портфолио (то, что показывают на собесе)

Один репо (`ship-ai-sandbox` или отдельный demo):

1. FastAPI LLM gateway (async)  
2. RAG + vector DB + citations  
3. Tools / простой agent  
4. Переключение cloud ↔ Ollama  
5. docker-compose  
6. 20–30 eval-кейсов  
7. Короткое демо 2–3 мин  

Этого хватает на **большинство** GenAI/LLM Application вакансий.

---

## Календарь (5–8 ч/нед)

| Фаза | Ориентир |
|---|---|
| A Фундамент | ✅ / 1–2 нед |
| B Cloud + Local | 2–4 нед |
| C FastAPI / Postgres / Redis | 4–7 нед |
| D RAG + LC/LI | 6–10 нед |
| E Agents | 3–5 нед |
| F Docker / UI | 4–6 нед |
| G Evals / tracing | 3–5 нед |
| H LoRA light | 3–6 нед |

**Итого среднего плана: ~6–11 месяцев** спокойно.  
При 15+ ч/нед реально ужать до **4–6 месяцев**.

---

## Что сознательно НЕ входит в средний план

Откладываем, пока не будет офферов/интереса к MLE:

- Spark, тяжёлый Airflow/Kubeflow
- ClickHouse как must
- Triton / TensorRT на старте
- Обучение LLM с нуля, RLHF «с нуля»
- Multi-agent зоопарк из 5 фреймворков

Это фаза **«После рынка / путь в ML Platform»**.

---

## Правила

1. Сначала руками (RAG, tools), потом LangChain.  
2. Один вертикальный продукт лучше десяти курсов.  
3. Каждый урок = папка + конспект `docs/NN-*.md` простым языком (зачем / как сделали / как работает) + коммит.  
4. После урока: блок «что запомнить» в том же md.  
5. Не прыгай в LoRA, пока нет RAG и FastAPI.

---

## Следующий шаг

**Урок 05 · Мульти-провайдер** — один клиент `LLM_PROVIDER` → GigaChat или Ollama (частично уже `lib/llm.py`).

Или закрепи 06: `python 06-gguf/check.py` и Hub → **06 GGUF**.
