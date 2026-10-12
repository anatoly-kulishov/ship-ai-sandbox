# 11 · LangChain RAG

[Уроки](../README.md#уроки) · [← 10](./10-chroma-rag.md)

LEARNING_PLAN: фаза D, урок 14. Идеи: Ed Donner w5 d3.

## Зачем
Рынок пишет «LangChain» в вакансиях. Смысл тот же, что в уроке 10: splitter → vector store → prompt → LLM. Фреймворк - обёртка, не магия.

## Простыми словами
| Урок 10 | Урок 11 |
|---|---|
| `lib/chunking.py` | `RecursiveCharacterTextSplitter` |
| `chromadb` напрямую | `langchain_chroma.Chroma` |
| ручной `messages=[…]` | `ChatPromptTemplate \| ChatOpenAI` |

Эмбеддинги те же: Ollama. Провайдер чата - наш `.env`.

## Как сделали
| Файл | Роль |
|---|---|
| `11-langchain-rag/pipeline.py` | ingest + ask |
| `11-langchain-rag/check.py` | CLI |
| `11-langchain-rag/app.py` | Gradio |

Индекс лежит отдельно: `vector_db_lc/`, чтобы не путать с уроком 10.

## Что потрогать
```bash
python 11-langchain-rag/check.py ingest
python 11-langchain-rag/check.py ask "Что такое Gatellm?"
npm run 11
```

Сравни ответ с `python 10-chroma-rag/check.py ask "…"`.

## Готово, когда
- [ ] Понимаешь: LC не отменяет chunking и «не знаю»
- [ ] Можешь объяснить цепочку `PROMPT | llm` своими словами

## Что запомнить
Сначала руки (05 → 09 → 10), потом фреймворк (11). На собесе это звучит увереннее, чем «я только по туториалу LC».

## Дальше
Урок 12: **PostgreSQL** - лог classify/plan в `events`.  
Теория: [agents](./theory/06-agents-react.md) · [docker](./theory/08-docker-basics.md).

[Уроки](../README.md#уроки) · [← 10](./10-chroma-rag.md) · [12 →](./12-postgres.md)
