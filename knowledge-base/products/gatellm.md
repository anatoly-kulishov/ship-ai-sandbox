# Gatellm

Gatellm - HTTP API вокруг Draftllm и Retrievellm.

## Эндпоинты (учебные)
- `GET /health` - жив ли сервис и какой провайдер
- `POST /plan` - brief → план
- `POST /retrieve` - brief → top-k упражнений

## Почему FastAPI
Swagger из коробки, Pydantic на границах, async для параллельных вызовов LLM (урок 08).

## Провайдеры
`LLM_PROVIDER=gigachat` или `ollama`. Клиент один: OpenAI-compatible SDK.
