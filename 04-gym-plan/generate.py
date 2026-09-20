"""04 · Gym plan — domain structured output + catalog whitelist.

Skill: brief → workout plan JSON with exerciseId only from fixture catalog.
Providers: GigaChat / Ollama via lib.llm (LLM_PROVIDER).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError, field_validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib.llm import MODEL, get_client, provider_name  # noqa: E402

CATALOG_PATH = Path(__file__).resolve().parent / "catalog.fixture.json"


MIN_EXERCISES = 5
MAX_EXERCISES = 8


class PlanExercise(BaseModel):
    exerciseId: str
    sets: int = Field(ge=2, le=5)
    reps: int = Field(ge=5, le=20)
    restSec: int = Field(ge=30, le=180)


class WorkoutPlanOut(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    exercises: list[PlanExercise] = Field(min_length=1, max_length=MAX_EXERCISES)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()


def load_catalog() -> list[dict]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def catalog_whitelist(catalog: list[dict]) -> set[str]:
    return {str(x["id"]) for x in catalog}


def catalog_prompt_lines(catalog: list[dict]) -> str:
    lines = []
    for x in catalog:
        title = x.get("name_ru") or x.get("name")
        lines.append(
            f"- {x['id']}: {title} | {x.get('body_part')} | {x.get('equipment')} | {x.get('target')}"
        )
    return "\n".join(lines)


def filter_known_ids(plan: WorkoutPlanOut, allowed: set[str]) -> WorkoutPlanOut:
    kept = [e for e in plan.exercises if e.exerciseId in allowed]
    if not kept:
        raise ValueError(
            "После whitelist не осталось упражнений — модель вернула неизвестные id"
        )
    return WorkoutPlanOut(name=plan.name, exercises=kept)


def pad_to_min(plan: WorkoutPlanOut, catalog: list[dict], allowed: set[str]) -> WorkoutPlanOut:
    have = {e.exerciseId for e in plan.exercises}
    exercises = list(plan.exercises)
    for row in catalog:
        if len(exercises) >= MIN_EXERCISES:
            break
        eid = str(row["id"])
        if eid not in allowed or eid in have:
            continue
        have.add(eid)
        exercises.append(PlanExercise(exerciseId=eid, sets=3, reps=10, restSec=90))
    if len(exercises) < min(MIN_EXERCISES, len(catalog), 4):
        raise ValueError(
            f"План слишком короткий после добора: {len(exercises)} (нужно ≥{MIN_EXERCISES})"
        )
    return WorkoutPlanOut(name=plan.name, exercises=exercises[:MAX_EXERCISES])


SYSTEM_TEMPLATE = """
Ты — API генерации плана тренировки для приложения Repdraft. Не чат-бот.
Собери силовой план для зала: безопасный, логичный по нагрузке, без воды.

Верни ТОЛЬКО валидный JSON без markdown:
{{
  "name": "краткое название плана",
  "exercises": [
    {{"exerciseId": "<id из каталога>", "sets": 4, "reps": 6, "restSec": 150}},
    {{"exerciseId": "<id из каталога>", "sets": 3, "reps": 10, "restSec": 90}},
    {{"exerciseId": "<id из каталога>", "sets": 3, "reps": 12, "restSec": 60}}
  ]
}}

Правила состава:
1. exerciseId — СТРОГО из списка каталога ниже. Не выдумывай id.
2. ОБЯЗАТЕЛЬНО 5–8 упражнений. Норма для «полноценной» сессии — 6.
3. Без дублей id. Порядок: тяжёлые/базовые (multi-joint) → вспомогательные → изоляция.
4. Учитывай зоны и оборудование из brief (штанга/гантели/кабель/тренажёры и т.д.).
5. Если в brief есть минуты — уложись в бюджет: ~45 мин ≈ 5–6 упр., ~60 мин ≈ 6–7, ~75+ ≈ 7–8.
6. Если brief мусорный — простой full-body из каталога (5+ упр.), всё равно с разной нагрузкой.

Программирование sets / reps / restSec (обязательно варьируй, не копируй один шаблон на все):
7. База (жим/тяга/присед/гребля и аналоги): sets 3–5, reps 5–8, restSec 120–180.
8. Вспомогательные compound: sets 3–4, reps 8–12, restSec 90–120.
9. Изоляция (бицепс/трицепс/дельты/икры и т.п.): sets 2–3, reps 10–15, restSec 45–75.
10. Кор / лёгкая техника: sets 2–3, reps 12–20, restSec 30–60.
11. В одном плане минимум 3 разных комбинации (sets,reps,restSec). Не ставь всем одинаковые 3×10×90.
12. Диапазоны чисел: sets 2–5, reps 5–20, restSec 30–180 (целые).
13. Не дублируй почти одинаковые движения (две тяги в наклоне, три сгибания на бицепс со штангой). Один паттерн — одно упражнение; смена плоскости/оборудования только если даёт явный смысл.
14. Сплит из двух зон (например спина+бицепс): 2–3 тяги/базы + 1–2 изоляции на вторую зону. Изоляция одной мышцы — не больше ~40% списка.

КАТАЛОГ (id | название | зона | оборудование | target):
{catalog}
""".strip()


SUBMIT_PLAN_FUNCTION = {
    "name": "submit_plan",
    "description": "Силовой план 5–8 упр. с разной нагрузкой (база тяжелее, изоляция легче)",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "exercises": {
                "type": "array",
                "minItems": 5,
                "maxItems": 8,
                "items": {
                    "type": "object",
                    "properties": {
                        "exerciseId": {"type": "string"},
                        "sets": {"type": "integer", "minimum": 2, "maximum": 5},
                        "reps": {"type": "integer", "minimum": 5, "maximum": 20},
                        "restSec": {"type": "integer", "minimum": 30, "maximum": 180},
                    },
                    "required": ["exerciseId", "sets", "reps", "restSec"],
                },
            },
        },
        "required": ["name", "exercises"],
    },
}


def _parse_payload(raw: object) -> WorkoutPlanOut:
    if isinstance(raw, dict):
        return WorkoutPlanOut.model_validate(raw)
    if isinstance(raw, str):
        text = raw.strip()
        if text.startswith("```"):
            text = text.strip("`")
            if text.startswith("json"):
                text = text[4:].strip()
        return WorkoutPlanOut.model_validate_json(text)
    raise ValueError(f"Unexpected payload type: {type(raw)}")


def generate_plan(brief: str, catalog: list[dict] | None = None) -> dict:
    catalog = catalog or load_catalog()
    allowed = catalog_whitelist(catalog)
    system = SYSTEM_TEMPLATE.format(catalog=catalog_prompt_lines(catalog))
    client = get_client()
    provider = provider_name()

    raw_payload: object
    if provider == "gigachat":
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": brief},
            ],
            functions=[SUBMIT_PLAN_FUNCTION],
            function_call={"name": "submit_plan"},
            temperature=0.2,
        )
        fn = response.choices[0].message.function_call
        if not fn:
            raise ValueError(f"No function_call: {response.choices[0].message}")
        raw_payload = fn.arguments
    else:
        kwargs: dict = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": brief},
            ],
            "temperature": 0.2,
        }
        try:
            response = client.chat.completions.create(
                **kwargs,
                response_format={"type": "json_object"},
            )
        except Exception:
            response = client.chat.completions.create(**kwargs)
        raw_payload = response.choices[0].message.content or "{}"

    try:
        plan = _parse_payload(raw_payload)
    except ValidationError as e:
        raise ValueError(f"Invalid plan payload: {raw_payload}") from e

    before = len(plan.exercises)
    plan = filter_known_ids(plan, allowed)
    after_filter = len(plan.exercises)
    plan = pad_to_min(plan, catalog, allowed)
    return {
        "ok": True,
        "provider": provider,
        "model": MODEL,
        "brief": brief,
        "plan": plan.model_dump(mode="json"),
        "droppedUnknownIds": before - after_filter,
    }


if __name__ == "__main__":
    brief = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "грудь и трицепс, 45 минут, только штанга и гантели"
    )
    result = generate_plan(brief)
    print(json.dumps(result, ensure_ascii=False, indent=2))
