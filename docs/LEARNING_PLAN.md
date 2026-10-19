# План обучения: AI Application / LLM Engineer (средний по рынку)

Цель: закрыть **пересечение большинства вакансий** вроде:
- AI/LLM Engineer (on-prem, RAG, FastAPI, Docker)
- Python GenAI Developer (LangChain, agents, vector DB, cloud + open-source)
- не полный Senior MLE с Spark/Kubeflow (это отдельный трек «после»)

Роль, на которую целимся:

> **AI Application Engineer** — встраивает LLM в продукт: API, RAG, tools/agents, качество, деплой.

Принцип: один навык за урок, простой язык, пример в `ship-ai-sandbox`. Темп любой.

Видео-запросы: [YOUTUBE_SEARCH.md](./YOUTUBE_SEARCH.md) · конспекты: [01](./01-note-sorter.md) … [11](./11-langchain-rag.md)  
Теория: [theory/](./theory/README.md) · карта курса Ed Donner: [sources/ed-donner.md](./sources/ed-donner.md)

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
| Качество | golden set, faithfulness, LLM-as-Judge, DeepEval, Langfuse, regression | must (вакансии GenAI Evaluation) |
| Fine-tune | LoRA/QLoRA — обзор + один мини-опыт | plus → часто must на Middle+ |
| Heavy MLOps | Airflow, Kafka, Spark, Triton | **не в среднем плане** (фаза «После рынка») |

### Покрытие вакансий

| Тип вакансии | Насколько закрывает этот план |
|---|---|
| GenAI / Python LLM (Neuro.net и аналоги) | **высокий** |
| AI/LLM Engineer on-prem (РЖД и аналоги) | **высокий** |
| Product AI / AI Application Engineer | **высокий** |
| GenAI Evaluation (hh и аналоги: бенчмарки, judge, observability) | **высокий**, если закрыта фаза G |
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
| 07 | FastAPI gateway (`07-fastapi/`) | must (фаза C урок 06) |
| 08 | asyncio + AsyncOpenAI (`08-asyncio/`) | must (фаза C урок 07) |
| 09 | Chunking + overlap (`09-chunking/`) | must (фаза D урок 10) |
| 10 | Chroma docs-RAG (`10-chroma-rag/`) | must (фаза D 12–13) |
| 11 | LangChain RAG thin (`11-langchain-rag/`) | must (фаза D урок 14) |
| 12 | PostgreSQL event log (`12-postgres/`) | must (фаза C урок 08) |

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
| A1 | Tokens, context window | [theory/01](./theory/01-tokens-context.md) |
| A2 | Temperature / top_p | [theory/02](./theory/02-prompts-temperature.md) |
| A3 | System vs user prompt | theory/02 + урок 01 |
| A4 | Structured output + Pydantic | урок 01 |
| A5 | Function calling / tools | урок 02 |
| A6 | Prompt-паттерны: few-shot, CoT, ReAct (теория) | theory/02 · [agents](./theory/06-agents-react.md) |

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

### Урок 07 · asyncio + async OpenAI client ✅ в репо

- Папка `08-asyncio/`, Hub **08 Asyncio**, порт `:8601`
- `AsyncOpenAI`, `asyncio.gather`, sync-код через `asyncio.to_thread`
- См. [08-asyncio.md](./08-asyncio.md)

**Готово:** объясняешь, почему gateway async, и `check:08` зелёный.

### Урок 08 · PostgreSQL ✅ в репо

- Папка `12-postgres/`, Hub **12 Postgres**, API `:8602`
- Таблица `events` (JSONB), `POST /classify` + `POST /plan` пишут лог
- См. [12-postgres.md](./12-postgres.md)

### Урок 09 · Redis (коротко)

Кэш эмбеддингов / rate limit / session — один простой use-case

**Срок фазы C:** 4–7 недель.

---

## Фаза D · RAG (ядро рынка)

Делай **сначала руками**, потом фреймворк.

| Урок | Тема | Готово |
|---|---|---|
| 10 | Chunking + overlap | **09-chunking/** + [theory/04](./theory/04-chunking.md) |
| 11 | Embeddings + cosine | **05-rag/** top-k по brief зала |
| 12 | Vector DB: **Chroma** (старт) | **10-chroma-rag/** |
| 12b | Второй store из вакансий: **pgvector или Qdrant** (один) | тот же retrieve, умеешь назвать отличие от Chroma |
| 13 | Full RAG + citations + «не знаю» | **10** ask по Fitllm KB |
| 14 | LangChain **или** LlamaIndex | **11-langchain-rag/** |

**Срок фазы D:** 6–10 недель.

---

## Фаза E · Agents (после tools + RAG)

### Урок 15 · Agent loop

- ReAct: мысль → tool → наблюдение → ответ
- 2–3 tools: поиск по базе, сохранить заметку, калькулятор/HTTP

### Урок 16 · Multi-step assistant + LangGraph

- Один сценарий «помощник по документам + запись задачи»
- Тот же сценарий как граф **LangGraph** (2-3 узла: retrieve → tools → answer)
- Без зоопарка из пяти agent-фреймворков. LangGraph нужен, потому что его прямо пишут в вакансиях рядом с LangChain

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

## Фаза G · GenAI Evaluation (приоритет сразу после RAG)

Ориентир: [AI/LLM Engineer в GenAI Evaluation, HeadHunter](https://spb.hh.ru/vacancy/138480763) (Москва, октябрь 2026). Роль ставит **evaluation-driven** процесс: бенчмарки, метрики, LLM-as-Judge, observability. Чат и RAG здесь уже предполагаются готовыми.

База для упражнений: Fitllm RAG из уроков 10–11. Один golden set гоняется снова при смене chunk size, модели или промпта.

| Урок | Тема | Готово, когда |
|---|---|---|
| 20 | Golden set | 20-30 вопросов по базе Fitllm: вопрос, ожидаемый факт, `source`. Версии датасета в git |
| 21 | Offline-метрики | faithfulness, попадание retrieve, pass/fail. Смена `chunk_size` двигает отчёт |
| 22 | LLM-as-Judge | рубрика отдельно от генератора. На 5 кейсах judge сравнивается с твоей ручной пометкой |
| 23 | Human eval (мини) | таблица: верно / частично / выдумка. Понимаешь, зачем человек, если judge уже есть |
| 24 | DeepEval | один тест-сьют на RAG, запускается как `check`, а не только ноутбук |
| 25 | Langfuse | в трейсе видны prompt, retrieved chunks, completion, latency |
| 26 | Сравнение моделей | один golden set на двух провайдерах (Ollama и облако), короткий diff-отчёт |
| 27 | Agent eval | после фазы E: оцениваешь траекторию tool calls, не только финальный текст |
| 28 | Security basics | API key, маскирование, «данные не утекают» в конспекте |

Плюсы той же вакансии, не блокер среднего плана: Java, обучение LLM с нуля, онлайн A/B на живом трафике. A/B на промптах достаточно понять на уровне идеи (см. YouTube-запросы).

**Срок:** 3-5 недель на уроки 20-26. Agent eval (27) после фазы E.

---

## Фаза H · Fine-tuning light (Middle+ рынок)

Не Deep Learning PhD — практический минимум:

| Урок | Тема | Готово |
|---|---|---|
| 29 | Hugging Face Transformers (load + generate) | прогнал модель локально/в колабе |
| 30 | LoRA / QLoRA: один маленький датасет | дообучил tiny-модель, сравнил до/после |
| 31 | Когда fine-tune, а когда RAG/prompt | чёткое правило в конспекте |

**Срок:** 3–6 недель.

---

## Портфолио (то, что показывают на собесе)

Один репо (`ship-ai-sandbox` или отдельный demo):

1. FastAPI LLM gateway (async)  
2. RAG + vector DB + citations  
3. Tools / простой agent  
4. Переключение cloud ↔ Ollama  
5. docker-compose  
6. Golden set + faithfulness + LLM-as-Judge (DeepEval)  
7. Трейс в Langfuse  
8. Короткое демо 2–3 мин  

Для вакансий **GenAI Evaluation** пункты 6–7 обязательны, не «потом».

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
| G GenAI Evaluation | 3-5 нед, **сразу после D** |
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
6. После рабочего RAG следующий навык - **оценка качества** (фаза G), не новый фреймворк.

---

## Следующий шаг

**Фаза G, урок 20:** golden set на Fitllm RAG (уроки 10–11). Потом judge, DeepEval, Langfuse.

Redis, LangGraph и Docker остаются в плане, но идут после первого eval-контура.
