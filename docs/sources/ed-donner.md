# Источник · Ed Donner · LLM Engineering

Курс [edwarddonner.com](https://edwarddonner.com/2024/11/13/llm-engineering-resources/) · репозиторий Udemy-компаньон · **MIT License** © 2024 Ed Donner.

В sandbox **не копируем** notebooks и `community-contributions/`. Берём идеи лекций → наши конспекты и уроки (Gradio + `check.py`).

Локальная копия курса (снаружи репо):  
`/Users/kulishov.a3/Downloads/llm_engineering-main`

---

## Карта week → наш план

| Ed Donner | Тема | У нас |
|---|---|---|
| w1 d1–2 | system/user, Chat Completions, OpenAI-compatible | [theory/02](../theory/02-prompts-temperature.md), [03](../theory/03-openai-compatible.md), уроки 01/03 |
| w1 d5 | multi-step LLM (brochure) | идея агентности → [theory/06](../theory/06-agents-react.md) |
| w2 | Gradio chat, tools | hub Gradio, урок 02 |
| w3 | HF / tokenizers | [theory/01](../theory/01-tokens-context.md), позже H23 |
| w4 | code gen | не тащим |
| w5 d1–2 | chunking + Chroma | **09**, **10** |
| w5 d3 | LangChain RAG | **11** |
| w5 d4 | RAG evals | фаза G / теория в 11 |
| w5 d5 | advanced ingest | позже |
| w6–7 | Price is Right / LoRA | [theory/07](../theory/07-finetune-vs-rag.md), фаза H |
| w8 | multi-agent / Modal | [theory/06](../theory/06-agents-react.md), фаза E |
| guide 09 | Ollama / APIs | урок 03 + theory/03 |
| guide 11 | async | урок 08 |
| guide 14 | Docker | [theory/08](../theory/08-docker-basics.md), фаза F |

---

## Что сознательно не переносим

- `community-contributions/` (сотни чужих ноутбуков)
- Colab-only labs как обязательный UI
- весь ML-капстоун «Price is Right» как линейный трек
- Modal.com / CrewAI зоопарк на старте

---

## Attribution

Идеи и учебная структура - Ed Donner (MIT).  
Практика и тексты конспектов в `ship-ai-sandbox` - свои, под роль AI Application Engineer и Repdraft.
