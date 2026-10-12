# Теория · OpenAI-compatible API

Источник идей: Ed Donner w1 d2 + guide 09. Практика: `lib/llm.py`, урок 03.

## Простыми словами
Chat Completions: «вот диалог - предскажи следующий ход».  
Формат OpenAI стал стандартом. Другие провайдеры дают **тот же** HTTP-контракт на другом `base_url`.

Клиент `openai` в Python - тонкая обёртка над HTTP, **не** код модели GPT.

```python
OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
OpenAI(base_url="https://api.giga.chat/v1", api_key=...)
```

У нас переключение: `LLM_PROVIDER=ollama|gigachat` в `.env`.

## Деньги и риски
Один вызов дёшев; агент с 20–30 вызовами - уже заметно.  
Локальный Ollama = бесплатно по API, платишь электричеством и RAM (урок 06).

## Что запомнить
Один SDK, разные `base_url`. Модель в продукте = endpoint + ключ + схема ответа.
