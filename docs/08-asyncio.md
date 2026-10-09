# 08 · Asyncio + AsyncOpenAI

[Уроки](../README.md#уроки) · [← 07](./07-fastapi.md)

LEARNING_PLAN: фаза C, урок 07. В sandbox папка `08-asyncio/`.

## Зачем
Запрос к LLM ждёт сеть секунды. Если gateway синхронный, один запрос занимает воркер, и второй ждёт в очереди. Async отпускает event loop, пока ждём ответ - несколько запросов идут параллельно.

## Простыми словами
Представь кассира в кафе.
- **Sync:** взял заказ → стоит и ждёт кофе → только потом следующий клиент.
- **Async:** взял заказ → пока варят кофе, принимает следующий → отдаёт готовые по мере прихода.

`await` = «я жду сеть, можно заняться другим».  
`AsyncOpenAI` = тот же OpenAI SDK, но методы `async` и их нужно `await`-ить.

Важно: `async def` + внутри обычный `requests.get(...)` - **плохо**. Ты сказал «я async», но всё равно блокируешь loop. Либо `await` async-клиент, либо вынеси sync в `asyncio.to_thread`.

## Как сделали
| Файл | Роль |
|---|---|
| `lib/llm.py` | `get_async_client()`, `ping_async()`, OAuth через `httpx` |
| `08-asyncio/classify.py` | тот же сортировщик 01, но `await create(...)` |
| `08-asyncio/server.py` | FastAPI: health, classify, demos, plan через `to_thread` |
| `08-asyncio/check.py` | sleep-демо + TestClient |

`POST /plan` специально оставляет sync `generate_plan` из урока 04 и зовёт его так:

```python
return await asyncio.to_thread(gym_generate.generate_plan, body.brief)
```

Так loop не блокируется, а большой кусок sync-кода не надо переписывать сразу.

## Как работает
1. `GET /health` - `await ping_async()`.
2. `POST /classify` - `await categorize_note_async(text)`.
3. `POST /demo/sleep` - `asyncio.gather` из N sleep. Wall ≈ один sleep, не сумма.
4. `POST /demo/classify` - N классификаций параллельно. Gateway не блокируется; сама модель может всё равно отвечать по очереди.
5. `POST /plan` - sync генерация в thread pool.

## Что потрогать
```bash
npm run 08                 # http://localhost:8601/docs
npm run check:08
```

В Swagger сначала жми `POST /demo/sleep` с `n=3`, `sleep_sec=0.4`.  
Жди ~0.4с. Если бы было sync подряд - 1.2с.

```bash
curl -X POST http://localhost:8601/demo/sleep \
  -H "Content-Type: application/json" \
  -d '{"n":3,"sleep_sec":0.4}'
```

## Готово, когда
- [ ] Объясняешь: async нужен, потому что LLM = долгое I/O
- [ ] `POST /demo/sleep` даёт `concurrent: true`
- [ ] Знаешь антипаттерн: `async def` + sync `requests` / sync OpenAI
- [ ] Понимаешь `to_thread` как мост для старого sync-кода

## Что запомнить
LLM-gateway на FastAPI почти всегда async. Ждёшь сеть - `await`. Старый sync - `to_thread`, не блокируй loop руками.

## Дальше
План: PostgreSQL (логи/диалоги), потом Redis (кэш эмбеддингов или rate limit).

[Уроки](../README.md#уроки) · [← 07](./07-fastapi.md) · [план](./LEARNING_PLAN.md)
