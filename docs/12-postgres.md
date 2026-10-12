# 12 · PostgreSQL

[Уроки](../README.md#уроки) · [← 11](./11-langchain-rag.md)

LEARNING_PLAN: фаза C, урок 08. Папка `12-postgres/`.

## Зачем
SQLite (урок 02) удобен для одного файла. В продукте логи диалогов, планов и retrieve обычно живут в **Postgres**: несколько сервисов, JSONB, индексы, бэкапы.

## Простыми словами
После вызова LLM мы **не выбрасываем** результат. Пишем строку в таблицу `events`:

| Колонка | Смысл |
|---|---|
| `kind` | `classify` / `plan` / `smoke` … |
| `brief` | исходный текст пользователя |
| `payload` | JSON ответа (JSONB) |
| `created_at` | когда записали |

API: `POST /classify`, `POST /plan` → ответ + `event`.  
Лента: `GET /events`.

## Как сделали
| Файл | Роль |
|---|---|
| `12-postgres/db.py` | connect, schema, log, list |
| `12-postgres/server.py` | FastAPI :8602 |
| `12-postgres/check.py` | smoke без UI |
| `12-postgres/app.py` | Gradio |
| `scripts/postgres-up.sh` | Homebrew Postgres + роль `ship` |
| `docker-compose.yml` | альтернатива, если есть Docker |

`DATABASE_URL` в `.env` (см. `.env.example`).

## Что потрогать
```bash
npm run postgres:up
npm run check:12
npm run check:12:llm    # classify → строка в events
npm run 12              # API :8602 + Swagger
npm run 12:ui           # Gradio
```

## Готово, когда
- [ ] `check:12` печатает `ping` и `logged`
- [ ] После classify в `GET /events` видна запись
- [ ] Понимаешь: LLM эфемерен, лог в БД - нет

## Что запомнить
Gateway без персистентности - демо. С Postgres появляется история для отладки, evals и продукта.

## Дальше
Redis (кэш / rate limit) или agents. Теория: [docker](./theory/08-docker-basics.md).

[Уроки](../README.md#уроки) · [← 11](./11-langchain-rag.md) · [план](./LEARNING_PLAN.md)
