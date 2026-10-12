# 09 · Chunking

[Уроки](../README.md#уроки) · [← 08](./08-asyncio.md) · [10 →](./10-chroma-rag.md)

LEARNING_PLAN: фаза D, урок 10. Теория: [theory/04-chunking](./theory/04-chunking.md).  
Идеи: Ed Donner w5 d2 (MIT) → [sources/ed-donner](./sources/ed-donner.md).

## Зачем
Урок 05 искал по **коротким** карточкам упражнений. Документы компании длинные: целиком в промпт не влезут и плохо матчятся. Сначала режем на чанки.

## Простыми словами
**Чанк** - кусок текста + откуда он (`source`).  
**Overlap** - хвост прошлого чанка в начале следующего, чтобы смысл на границе не умер.  
Режем «умно»: абзацы → строки → слова → символы (как RecursiveCharacterTextSplitter, но без LangChain).

База: `knowledge-base/` (учебный бренд **Fitllm**).

## Как сделали
| Файл | Роль |
|---|---|
| `knowledge-base/**/*.md` | документы |
| `lib/kb.py` | загрузка |
| `lib/chunking.py` | recursive split + overlap |
| `09-chunking/check.py` | CLI |
| `09-chunking/app.py` | слайдеры size/overlap |

## Что потрогать
```bash
python 09-chunking/check.py
python 09-chunking/check.py 400 80
npm run 09
```

## Готово, когда
- [ ] Видишь разные `source` у чанков
- [ ] Уменьшение `chunk_size` → больше чанков
- [ ] Понимаешь зачем overlap

## Что запомнить
Без `source` не будет citations. Chunking - подготовка к Chroma (урок 10).

## Дальше
Урок 10: те же чанки → embeddings → Chroma → вопрос-ответ.

[Уроки](../README.md#уроки) · [← 08](./08-asyncio.md) · [10 →](./10-chroma-rag.md)
