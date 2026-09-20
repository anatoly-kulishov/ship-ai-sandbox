"""GGUF / quantization: estimate RAM and pick a local model that fits.

Ollama serves GGUF (llama.cpp). Default tags like `qwen2.5:7b` are Q4_K_M.
This is a rule-of-thumb calculator, not a profiler: long context eats extra
KV-cache RAM on top of weights.
"""

from __future__ import annotations

import json
import platform
import subprocess
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass

# bytes/param for weights. Q4_K_M ≈ 0.55; runtime+short KV on top.
BPP: dict[str, float] = {"q4": 0.55, "q5": 0.70, "q8": 1.05, "fp16": 2.0}
RUNTIME_GB = 1.5
KV_HEADROOM_GB = 4.0
OLLAMA_TAGS = "http://localhost:11434/api/tags"


@dataclass(frozen=True)
class Hardware:
    ram_gb: float
    chip: str
    unified: bool
    os: str


@dataclass(frozen=True)
class Model:
    tag: str
    params_b: float
    quant: str
    note: str = ""

    @property
    def ram_gb(self) -> float:
        return round(estimate_ram_gb(self.params_b, self.quant), 2)


# Pullable Ollama defaults (Q4). Q5/Q8/FP16 are the same sizes via estimate_ram_gb.
CATALOG: tuple[Model, ...] = (
    Model("qwen2.5:3b", 3.0, "q4", "текущий default sandbox"),
    Model("qwen2.5:7b", 7.0, "q4", "structured JSON, запас по качеству"),
    Model("qwen2.5:14b", 14.0, "q4", "качество вверх, медленнее"),
    Model("qwen2.5:32b", 32.0, "q4", "нужно много unified RAM"),
    Model("llama3.1:70b", 70.0, "q4", "сервер, не ноутбук"),
)


def estimate_ram_gb(params_b: float, quant: str) -> float:
    bpp = BPP[quant]
    return params_b * bpp + RUNTIME_GB


def os_reserve_gb(total_ram_gb: float) -> float:
    # ponytail: clamp, not a per-SKU table. Ceiling: ignores dGPU split; upgrade = nvidia-smi path.
    return min(8.0, max(3.0, total_ram_gb * 0.30))


def usable_gb(total_ram_gb: float) -> float:
    return max(0.0, total_ram_gb - os_reserve_gb(total_ram_gb))


def _comfort_budget(usable: float) -> float:
    return usable - min(KV_HEADROOM_GB, usable * 0.25)


def probe() -> Hardware:
    system = platform.system()
    if system == "Darwin":
        ram = int(subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True)) / (1024**3)
        chip = subprocess.check_output(
            ["sysctl", "-n", "machdep.cpu.brand_string"], text=True
        ).strip()
        return Hardware(ram_gb=round(ram, 1), chip=chip, unified=True, os=system)
    if system == "Linux":
        mem_kb = 0
        with open("/proc/meminfo", encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("MemTotal:"):
                    mem_kb = int(line.split()[1])
                    break
        return Hardware(
            ram_gb=round(mem_kb / (1024**2), 1),
            chip=platform.processor() or "linux",
            unified=False,
            os=system,
        )
    raise RuntimeError(f"unsupported os: {system}")


def _largest(models: list[Model]) -> Model | None:
    if not models:
        return None
    return max(models, key=lambda m: (m.params_b, -BPP[m.quant]))


def pick(models: tuple[Model, ...] | list[Model], usable: float) -> dict[str, Model | None]:
    """recommended = comfortable headroom; stretch = largest that still fits."""
    all_models = list(models)
    stretch = _largest([m for m in all_models if m.ram_gb <= usable])
    recommended = _largest([m for m in all_models if m.ram_gb <= _comfort_budget(usable)]) or stretch
    fitting = [m for m in all_models if m.ram_gb <= usable]
    sandbox = next((m for m in all_models if m.tag == "qwen2.5:7b" and m.ram_gb <= usable), None)
    if sandbox is None:
        sandbox = min(fitting, key=lambda m: m.params_b) if fitting else None
    return {"recommended": recommended, "stretch": stretch, "sandbox": sandbox}


def list_ollama_models(timeout: float = 1.5) -> list[dict]:
    try:
        with urllib.request.urlopen(OLLAMA_TAGS, timeout=timeout) as resp:
            data = json.load(resp)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return []
    out = []
    for item in data.get("models") or []:
        out.append(
            {
                "name": item.get("name") or "",
                "size_gb": round(float(item.get("size") or 0) / 1e9, 2),
            }
        )
    return out


def report(hw: Hardware | None = None) -> dict:
    hw = hw or probe()
    usable = round(usable_gb(hw.ram_gb), 2)
    reserve = round(os_reserve_gb(hw.ram_gb), 2)
    choices = pick(CATALOG, usable)
    rows = []
    rec = choices["recommended"]
    stretch = choices["stretch"]
    for model in CATALOG:
        if model.ram_gb <= _comfort_budget(usable):
            status = "ok"
        elif model.ram_gb <= usable:
            status = "tight"
        else:
            status = "no"
        rows.append(
            {
                "tag": model.tag,
                "params_b": model.params_b,
                "quant": model.quant,
                "ram_gb": model.ram_gb,
                "status": status,
                "note": model.note,
                "pick": model.tag == (rec.tag if rec else None),
                "stretch": model.tag == (stretch.tag if stretch else None),
            }
        )
    quant_7b = {q: round(estimate_ram_gb(7.0, q), 2) for q in ("q4", "q5", "q8", "fp16")}
    return {
        "hardware": asdict(hw),
        "os_reserve_gb": reserve,
        "usable_gb": usable,
        "recommended": rec.tag if rec else None,
        "stretch": stretch.tag if stretch else None,
        "sandbox": choices["sandbox"].tag if choices["sandbox"] else None,
        "catalog": rows,
        "quant_7b_ram_gb": quant_7b,
        "installed": list_ollama_models(),
    }
