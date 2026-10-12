# ship-ai-sandbox

Песочница **AI Application Engineer**: модель в продукте, не чат.

С телефона удобнее читать **один урок за раз** (ссылки ниже).  
Код и Gradio-hub - с компьютера.

## Уроки

1. [01 · Сортировщик](docs/01-note-sorter.md)  
   Текст → JSON. Pydantic проверяет схему.

2. [02 · Tool use](docs/02-tool-use.md)  
   Модель вызывает `save_note`. Код пишет в SQLite.

3. [03 · Ollama](docs/03-ollama.md)  
   Тот же сортировщик, но модель на своём компьютере.

4. [04 · Gym plan](docs/04-gym-plan.md)  
   Brief → план. Только id из каталога.

5. [05 · RAG](docs/05-rag.md)  
   Сначала найти упражнения по смыслу, потом уже план.

6. [06 · GGUF](docs/06-gguf.md)  
   Q4/Q8 и сколько RAM нужно на 7B/14B.

7. [07 · FastAPI](docs/07-fastapi.md)  
   Тот же план, но через HTTP API со Swagger.

8. [08 · Asyncio](docs/08-asyncio.md)  
   AsyncOpenAI: gateway не блокируется, пока ждёт LLM.

9. [09 · Chunking](docs/09-chunking.md)  
   Документы → чанки с overlap и `source`.

10. [10 · Chroma RAG](docs/10-chroma-rag.md)  
    Docs-RAG: Chroma + Ollama embeddings + «не знаю».

11. [11 · LangChain RAG](docs/11-langchain-rag.md)  
    Тот же RAG через тонкий LangChain.

12. [12 · PostgreSQL](docs/12-postgres.md)  
    LLM-вызов → строка в `events` (JSONB).

Дальше по плану: Redis, agents, Docker.

[План](docs/LEARNING_PLAN.md) · [Теория](docs/theory/README.md) · [Ed Donner карта](docs/sources/ed-donner.md) · [Gradio hub](docs/gradio-hub.md) · [YouTube](docs/YOUTUBE_SEARCH.md) · [CONTINUE](docs/CONTINUE.md)

---

## Запуск (компьютер)

```bash
git clone https://github.com/anatoly-kulishov/ship-ai-sandbox.git
cd ship-ai-sandbox
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Ключ GigaChat: [Sber Developers Studio](https://developers.sber.ru/studio) → API → Authorization key.  
Вставь в `.env` как `GIGACHAT_API_KEY`. Не коммить `.env`.

```bash
npm run hub                 # все уроки, http://localhost:8501
npm run 09                  # chunking
npm run check:09
npm run ollama:start
ollama pull nomic-embed-text
npm run check:10:ingest && npm run check:10
npm run check:11:ingest && npm run check:11
npm run postgres:up
npm run check:12
```

**Hub:** Gradio, навбар сверху по урокам. Accordion **Конспект урока** = текст из `docs/`.

---

## Запомнить

1. LLM в продукте отвечает **схемой**, не абзацем.
2. Промпт = правила. Проверка - **твой код** (Pydantic, whitelist).
3. Сначала retrieve (каталог или docs), потом генерация.
4. Chunking → vector store → «не знаю», если нет в контексте.
5. LangChain - после своего RAG, не вместо.

---

Учебный репозиторий, форкай свободно.  
Идеи лекций частично из курса Ed Donner (MIT) - см. [docs/sources/ed-donner.md](docs/sources/ed-donner.md).
