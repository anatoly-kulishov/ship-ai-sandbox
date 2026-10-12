# Gradio hub (как учиться в UI)

[Уроки](../README.md#уроки)

## Зачем Gradio
Один интерфейс для всех уроков. На рынке Gradio часто для демо и Hugging Face Spaces. Здесь он - учебный хаб, не замена FastAPI.

## Как пользоваться
1. `npm run hub` → http://localhost:8501
2. Навбар сверху: Home + уроки 01…12
3. На странице урока открой **Конспект урока** - тот же текст, что в `docs/`
4. Один урок отдельно: `npm run 01` … `npm run 11`
5. Уроки 07/08 - API отдельно (`npm run 07` / `08`), в hub только шпаргалка
6. Теория без UI: [`docs/theory/`](./theory/README.md)

## Что где
| Файл | Роль |
|---|---|
| `app.py` | multipage hub (`demo.route`) |
| `lib/ui.py` | тема, конспект-accordion, launch |
| `NN-…/app.py` | UI урока, `build()` → `gr.Blocks` |

Бизнес-логика (categorize, generate_plan, embeddings) **не** в Gradio - только кнопки и таблицы.
