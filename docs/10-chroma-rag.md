# 10 · Chroma RAG

[Уроки](../README.md#уроки) · [← 09](./09-chunking.md) · [11 →](./11-langchain-rag.md)

LEARNING_PLAN: фаза D, уроки 12–13 (Chroma вместо Qdrant на старте).  
Теория: [theory/05-vector-stores](./theory/05-vector-stores.md). Идеи: Ed Donner w5.

## Зачем
Урок 05 = cosine по JSON каталога. Здесь = **документы** компании Fitllm в vector store. Так устроен knowledge-worker из курса Ed, только домен зала/ИИ.

## Простыми словами
1. Нарезаем md (урок 09).  
2. Каждый чанк → embedding (Ollama `nomic-embed-text`).  
3. Кладём в **Chroma** (папка `vector_db/`).  
4. Вопрос → top-k чанков → LLM с правилом «не знаю».

## Как сделали
| Файл | Роль |
|---|---|
| `10-chroma-rag/store.py` | ingest / retrieve |
| `10-chroma-rag/answer.py` | промпт + LLM |
| `10-chroma-rag/check.py` | `ingest` / `retrieve` / `ask` |
| `10-chroma-rag/app.py` | Gradio |

## Что потрогать
```bash
npm run ollama:start
ollama pull nomic-embed-text
python 10-chroma-rag/check.py ingest
python 10-chroma-rag/check.py ask "Какие продукты у Fitllm?"
npm run 10
```

## Готово, когда
- [ ] Ingest без ошибки, count > 0
- [ ] Вопрос про Draftllm отвечает по базе
- [ ] Вопрос «курс доллара завтра» → «не знаю по базе Fitllm»

## Что запомнить
Vector DB хранит поиск. Правду для ответа всё ещё проверяешь правилами промпта + своими глазами.

## Дальше
Урок 11: тот же RAG через тонкий LangChain.

[Уроки](../README.md#уроки) · [← 09](./09-chunking.md) · [11 →](./11-langchain-rag.md)
