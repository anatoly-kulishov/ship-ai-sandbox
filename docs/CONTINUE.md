# Контекст для нового чата · продолжаем учиться

Дата снимка: **2026-10-19**. Открой этот файл в новом чате и скажи: «продолжай по `docs/CONTINUE.md`».

---

## Кто / зачем

- **Цель роли:** AI Application Engineer - LLM в продукт (API, RAG, tools, качество, деплой).
- **План:** [`LEARNING_PLAN.md`](./LEARNING_PLAN.md)
- **Теория:** [`theory/`](./theory/README.md) · [`sources/ed-donner.md`](./sources/ed-donner.md)
- **Песочница:** `/Users/kulishov.a3/WebstormProjects/ship-ai-sandbox`
- **Продукт:** `/Users/kulishov.a3/WebstormProjects/repdraft` → [Repdraft v0.18.0](https://github.com/anatoly-kulishov/Repdraft/releases/tag/v0.18.0)

Конспект обязателен: `docs/NN-*.md` простым языком.

---

## Уже закрыто в sandbox

| Урок | Навык |
|---|---|
| 01–11 | structured → tools → Ollama → gym → cosine RAG → GGUF → FastAPI → asyncio → chunking → Chroma → LangChain |
| **12** | `12-postgres/` · [12-postgres.md](./12-postgres.md) · Postgres `events` JSONB |

Animator/whiteboard - эксперимент, **не** часть трека. Медиа в `docs/media/` можно игнорить.

```bash
npm run postgres:up
npm run check:12
npm run check:12:llm
npm run 12          # :8602
```

`DATABASE_URL=postgresql://ship:ship@127.0.0.1:5432/ship_ai` (Homebrew `postgresql@16`).

---

## Прод-мост Repdraft

`/ai` в v0.18.0. Хвост: Vercel `GIGACHAT_*` на Production; embeddings stub → regex.

---

## Дальше

Ориентир вакансии: [hh · GenAI Evaluation](https://spb.hh.ru/vacancy/138480763). Детали в фазе G [`LEARNING_PLAN.md`](./LEARNING_PLAN.md).

| Приоритет | Тема |
|---|---|
| 1 | **G · golden set** на Fitllm RAG (урок 20): 20-30 вопросов, source, pass/fail |
| 2 | LLM-as-Judge + сверка с ручной пометкой |
| 3 | DeepEval-сьют и трейс в Langfuse |
| 4 | Сравнение двух провайдеров на одном сете |
| 5 | Потом agents + LangGraph, Redis, Docker, pgvector или Qdrant |
| 6 | Прод: Vercel secrets |

---

## Стартовый промпт

```text
Продолжаем по docs/CONTINUE.md в ship-ai-sandbox.
Уроки 01–12 закрыты. Следующий шаг один: урок 20, golden set для Fitllm RAG (фаза G, GenAI Evaluation).
Не Redis и не agents, пока нет первого eval-контура.
```
