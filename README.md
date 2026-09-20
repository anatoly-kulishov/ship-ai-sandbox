# ship-ai-sandbox

Песочница **AI Application Engineer**: модель в продукте, не чат.

С телефона удобнее читать **один урок за раз** (ссылки ниже).
Код и запуск - с компьютера, внизу страницы.

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

Дальше по плану: один клиент cloud ∪ Ollama, потом FastAPI.

[План обучения](docs/LEARNING_PLAN.md)  
[Что искать на YouTube](docs/YOUTUBE_SEARCH.md)

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
npm run 01                  # один урок
npm run ollama:start
npm run provider:ollama     # или provider:gigachat
python 01-note-sorter/categorize.py "надо купить хлеб"
```

Hub: сайдбар слева. На странице урока - expander **Конспект урока** (тот же текст, что в `docs/`).

---

## Запомнить

1. LLM в продукте отвечает **схемой**, не абзацем.
2. Промпт = правила. Проверка - **твой код** (Pydantic, whitelist).
3. Побочные эффекты (БД) делает код, не модель.
4. Провайдер меняется в `.env`: `LLM_PROVIDER=gigachat` или `ollama`.
5. Сначала ищем по каталогу (RAG), потом генерируем план.

---

Учебный репозиторий, форкай свободно.
