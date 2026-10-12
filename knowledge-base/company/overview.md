# Overview · Fitllm

Fitllm - учебная «компания» для RAG в ship-ai-sandbox (аналог Insurellm из курса Ed Donner, но прозал и ИИ-план тренировок).

Основана в 2024 как sandbox-бренд. Продукт связки: **Repdraft** (мобильный зал) + локальные уроки AI Application Engineer.

## Продукты
- **Draftllm** - черновик плана тренировки из brief пользователя
- **Retrievellm** - поиск упражнений по смыслу (embeddings)
- **Gatellm** - FastAPI gateway: health, plan, retrieve

## Принципы
1. Модель выбирает только id из каталога (whitelist).
2. Сначала retrieve, потом генерация.
3. Зона brief важнее «красивого» текста модели.
