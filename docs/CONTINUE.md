# Контекст для нового чата · продолжаем учиться

Дата снимка: **2026-09-20**. Открой этот файл в новом чате и скажи: «продолжай по `docs/CONTINUE.md`».

---

## Кто / зачем

- **Цель роли:** AI Application Engineer - LLM в продукт (API, RAG, tools, качество, деплой).
- **План:** [`LEARNING_PLAN.md`](./LEARNING_PLAN.md)
- **Песочница (уроки):** `/Users/kulishov.a3/WebstormProjects/ship-ai-sandbox`
- **Продукт (мост в прод):** `/Users/kulishov.a3/WebstormProjects/repdraft` → [Repdraft v0.18.0](https://github.com/anatoly-kulishov/Repdraft/releases/tag/v0.18.0)

Принцип: один навык за урок в sandbox → тот же навык в Repdraft, когда готов.

Конспект обязателен: `docs/NN-*.md` простым языком (зачем / как сделали / как работает). Без md урок не закрыт.

---

## Уже закрыто в sandbox

| Урок | Папка / Hub | Навык |
|---|---|---|
| 01 | `01-note-sorter/` · [01-note-sorter.md](./01-note-sorter.md) | Structured output + Pydantic |
| 02 | `02-tool-use/` · [02-tool-use.md](./02-tool-use.md) | Tool use → SQLite |
| 03 | `03-ollama/` · [03-ollama.md](./03-ollama.md) | Local LLM (Ollama) |
| 04 | `04-gym-plan/` · [04-gym-plan.md](./04-gym-plan.md) | Gym plan + catalog whitelist |
| 05 | `05-rag/` · [05-rag.md](./05-rag.md) | Embeddings + cosine по каталогу (фаза D / урок 11) |
| 06 | `06-gguf/` · [06-gguf.md](./06-gguf.md) | GGUF / Q4-Q8, модель под RAM (фаза B / урок 04 плана) |

Стек sandbox: Streamlit hub (`app.py`, `pages/`), `lib/llm.py` / `lib/gigachat.py`, `.env` с GigaChat + Ollama.

Запуск:

```bash
cd /Users/kulishov.a3/WebstormProjects/ship-ai-sandbox
# .venv уже есть
npm run 06          # или run.sh / streamlit
python 06-gguf/check.py
```

---

## Продуктовый мост: Repdraft `/ai` (v0.18.0)

**Смержено в `main`, релиз:** https://github.com/anatoly-kulishov/Repdraft/releases/tag/v0.18.0 · PR #91

### Что умеет пользователь

- **Черновик с ИИ** на `/ai` (не lab): brief → план из whitelist каталога.
- Входы: пустые **Тренировки** («Черновик с ИИ» + Sparkles) и пустой **билдер** («Собрать с ИИ» + Sparkles).
- В **Аккаунте** ссылки на ИИ **нет** (продукт, не бета).
- **Сценарии** (`/scenarios`) доступны всем из Аккаунта; QA-док актуализирован под `/ai`.
- Flow-chrome как у билдера: без RP-лого и tabbar.
- `/lab/ai` → 308 на `/ai`.

### Архитектура (сервер)

| Модуль | Путь | Роль |
|---|---|---|
| API | `src/routes/api/ai/plan/+server.ts` | `GET` availability, `POST` generate |
| UI | `src/routes/ai/+page.svelte` | composer, чипы зон, план → билдер |
| Generate | `src/lib/server/ai/generatePlan.ts` | LLM + parse + whitelist + zone filter + pad |
| Retrieve | `src/lib/server/ai/retrieve.ts` | hybrid cosine∪regex; fallback regex |
| Catalog hints | `src/lib/server/ai/catalog.ts` | slang/зоны, slim zone-first |
| Templates | `src/lib/server/ai/splitTemplates.ts` | push/pull/arms… |
| Embeddings | `src/lib/server/ai/embeddings.ts` + `embedText.ts` | Ollama default; GigaChat embeddings часто 402 |
| Config | `src/lib/server/ai/config.ts` | `AI_PROVIDER` gigachat \| ollama |
| Gate | `npm run check:ai` | все `*.selfcheck.ts` под `src/lib/server/ai/` |

Важные инварианты (уже в adversarial):

- Zone brief: prompt/pad **только** из зоны; пустой pool → `invalid_plan` (не fallback на весь каталог).
- «булки» → ноги; «предплечье» ≠ плечи; word-boundary для EN (`back`/`leg`).
- `droppedUnknownIds` = только unknown ids, не zone drops.

### Embeddings / RAG в продукте

- Файл: `static/data/exercises.embeddings.json` - сейчас **пустой stub** (`items: []`) → runtime всегда **regex**.
- Hybrid включается после: `npm run build:embeddings` (Ollama `nomic-embed-text`).
- В Whats new **не** заявляли RAG/hybrid - честный ship regex + zone templates.

### Нативный splash (в том же релизе)

- Тёмный splash Capacitor, `launchAutoHide: false`, dismiss после web boot.
- Android `colors.xml` + styles SplashScreen API; iOS imageset; `scripts/generate-brand-icons.mjs`.

### Баг, починенный перед релизом

- Петля **←** `/auth` ↔ `/scenarios`: у сценариев был `preferHistoryBack={false}` → push `/auth` в history. Исправлено на history.back (как terms/privacy).

---

## Секреты / прод (открытый хвост)

Локально в `repdraft/.env` ключи GigaChat **есть**. На **Vercel Production** private env для чата, скорее всего, **ещё нет** → `/ai` показывает «ИИ недоступен».

Нужно (не `PUBLIC_*`):

```text
AI_PROVIDER=gigachat
GIGACHAT_API_KEY=…
GIGACHAT_MODEL=GigaChat-2
GIGACHAT_SSL_VERIFY=false
```

Опционально: `GIGACHAT_BASE_URL`, `GIGACHAT_OAUTH_URL`, `GIGACHAT_SCOPE`.

Проверка: `GET /api/ai/plan` → `{"available":true,"provider":"gigachat"}`, затем Redeploy.

Агент может залить из локального `.env`, если дать `VERCEL_TOKEN` (ключ GigaChat в чат не кидать).

Sandbox `.env` - свой набор для Streamlit-уроков (тот же провайдер по смыслу).

---

## Чему научились на практике (связка план ↔ прод)

1. Structured JSON / function calling (GigaChat) vs `json_object` (Ollama).
2. Trust boundary: LLM выбирает только id из whitelist.
3. Retrieve перед генерацией: regex-хинты + (опционально) embeddings.
4. Zone leaks = реальная прод-проблема; adversarial selfchecks как регрессии.
5. Productize: lab → `/ai`, entry points, i18n `aiDraft.*`, flow chrome, сценарии.
6. Delivery: semver ветка, Whats new, `check:ai` в release-gate, GH Release.
7. GGUF / Q4: модель выбирают по RAM, не по постеру; 24 GB Mac → 14B comfortable, 7B для JSON sandbox.

---

## Что делать дальше (обучение)

Ориентир - [`LEARNING_PLAN.md`](./LEARNING_PLAN.md). Логичный порядок после 06:

| Приоритет | Тема плана | Идея следующего урока в sandbox |
|---|---|---|
| 1 | B · урок 05 | Мульти-провайдер уже частично есть (`lib/llm.py`) - довести до явного «один клиент» |
| 2 | C · урок 06 | **FastAPI** gateway: `POST /plan` рядом с Streamlit |
| 3 | D · урок 12 | Qdrant или pgvector (сейчас cosine руками) |
| 4 | E · agents | после tools+RAG |
| 5 | Прод | Залить Vercel secrets; опционально `build:embeddings` и закоммитить индекс |

Видео-запросы: [`YOUTUBE_SEARCH.md`](./YOUTUBE_SEARCH.md).

---

## Команды-якоря

```bash
# Sandbox GGUF
cd /Users/kulishov.a3/WebstormProjects/ship-ai-sandbox
python 06-gguf/check.py

# Repdraft AI gate
cd /Users/kulishov.a3/WebstormProjects/repdraft
npm run check:ai
# optional hybrid:
# npm run build:embeddings
```

---

## Стартовый промпт для нового чата

```text
Продолжаем обучение по docs/CONTINUE.md в ship-ai-sandbox.
Репозитории: ship-ai-sandbox (уроки) и repdraft (продукт, /ai уже в v0.18.0).
Следующий шаг: предложи один следующий урок из LEARNING_PLAN (не всё сразу)
и сразу начни с минимального задания в sandbox.
06-gguf уже есть. Открытый хвост прода: Vercel GIGACHAT_* для /ai.
```

---

## Ссылки

- План: [LEARNING_PLAN.md](./LEARNING_PLAN.md)
- Уроки: [01](./01-note-sorter.md) · [02](./02-tool-use.md) · [03](./03-ollama.md) · [04](./04-gym-plan.md) · [05](./05-rag.md) · [06](./06-gguf.md)
- Repdraft release: https://github.com/anatoly-kulishov/Repdraft/releases/tag/v0.18.0
- Прод preview/prod: `https://repdraft-zeta.vercel.app` (из `.env.example`)
