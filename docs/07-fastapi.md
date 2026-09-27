# 07 · FastAPI gateway

[Уроки](../README.md#уроки) · [← 06](./06-gguf.md)

LEARNING_PLAN: фаза C, урок 06. В sandbox папка `07-fastapi/`.

## Зачем
LLM в продукте — это не Streamlit-виджет, а API. Рынок хочет **FastAPI + Pydantic** почти в каждой вакансии. Урок оборачивает уже готовую генерацию плана (04) и поиск по каталогу (05) в HTTP API со Swagger.

## Простыми словами
FastAPI — это тонкий слой, который принимает HTTP-запрос, проверяет тело по Pydantic-схеме, вызывает ту же Python-функцию и отдаёт JSON. `/docs` рисует формы автоматически.

Главное отличие от чат-виджета:
- вход — не `st.text_input`, а `POST /plan` с JSON
- ответ — не markdown, а строгая схема
- ошибки — не трейсбек в браузере, а HTTP-статусы: 422 (невалидный запрос), 502 (LLM не ответил), 503 (провайдер недоступен)

## Как сделали
| Файл | Роль |
|---|---|
| `07-fastapi/server.py` | FastAPI app: `GET /health`, `POST /plan`, `POST /retrieve` |
| `07-fastapi/check.py` | самопроверка через `TestClient` — без ручного curl |
| `docs/07-fastapi.md` | этот конспект |
| `pages/7_07_FastAPI.py` | страница хаба со ссылкой на Swagger |

`server.py` не копирует логику генерации плана, а подгружает `04-gym-plan/generate.py` и `05-rag/embeddings.py` через `importlib` — тот же код, новый интерфейс.

## Как работает
1. `GET /health` — пингует текущего провайдера (`lib.llm.ping`) и возвращает `provider`/`model`. Если провайдер лежит — 503.
2. `POST /plan` — Pydantic-модель `BriefIn` с полем `brief`. Зовёт `generate_plan`, возвращает готовый JSON-план. Ошибки генерации → 502, ошибки валидации → 422.
3. `POST /retrieve` — Pydantic-модель `RetrieveIn` (`brief`, `top_k`). Зовёт `retrieve` из RAG-урока, возвращает список упражнений.
4. Swagger UI доступен на `http://localhost:8600/docs` — можно жать «Try it out» прямо в браузере.

## Что потрогать
```bash
npm run 07          # uvicorn на :8600
```
Открой http://localhost:8600/docs → `POST /plan` → введи brief → Execute.

```bash
npm run check:07    # TestClient: health, plan, retrieve, 422, 404
```

CLI вариант без браузера:
```bash
curl -X POST http://localhost:8600/plan \
  -H "Content-Type: application/json" \
  -d '{"brief":"спина и бицепс, 60 минут"}'
```

## Готово, когда
- [ ] Запускаешь `npm run 07` и видишь Swagger
- [ ] `POST /plan` возвращает план с `exercises`, все `exerciseId` из каталога
- [ ] Объясняешь разницу между 422, 502, 503
- [ ] `npm run check:07` проходит (retrieve может быть пропущен, если Ollama не запущен)

## Что запомнить
FastAPI — это не новый ИИ, это **стандартный способ отдать LLM-функцию по HTTP**. Контракт запроса/ответа — Pydantic. Ошибки — HTTP-статусы. Всё остальное (prompt, whitelist, RAG) остаётся прежним.

## Дальше
План: урок 08 · **asyncio + async OpenAI client** — зачем gateway должен быть async, и как сделать `POST /plan` по-настоящему неблокирующим.

[Уроки](../README.md#уроки) · [← 06](./06-gguf.md) · [план](./LEARNING_PLAN.md)
