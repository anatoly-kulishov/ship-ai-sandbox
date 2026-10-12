# Контекст для нового чата · продолжаем учиться

Дата снимка: **2026-10-12**. Открой этот файл в новом чате и скажи: «продолжай по `docs/CONTINUE.md`».

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

| Приоритет | Тема |
|---|---|
| 1 | Redis (кэш эмбеддингов / rate limit) |
| 2 | Agents (фаза E; теория в `theory/06`) |
| 3 | Docker compose gateway+Postgres |
| 4 | Прод: Vercel secrets |

---

## Стартовый промпт

```text
Продолжаем по docs/CONTINUE.md в ship-ai-sandbox.
Уроки 01–12 закрыты (Postgres events есть).
Следующий шаг: Redis или agents — один навык.
```
