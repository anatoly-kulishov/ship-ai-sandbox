"""Streamlit UI for lesson 06 — GGUF / quantization calculator."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from recommend import report


def render() -> None:
    st.title("06 · GGUF / quantization")
    st.caption("Сколько RAM нужно на Q4/Q5/Q8 и какая модель влезает в это железо")
    with st.expander("Конспект урока"):
        st.markdown((ROOT / "docs" / "06-gguf.md").read_text(encoding="utf-8"))

    data = report()
    hw = data["hardware"]

    with st.container(horizontal=True, gap="medium"):
        st.metric("RAM", f"{hw['ram_gb']} GB")
        st.metric("Usable", f"{data['usable_gb']} GB")
        st.metric("OS reserve", f"{data['os_reserve_gb']} GB")
    st.caption(f"{hw['chip']} · unified={hw['unified']} · {hw['os']}")

    rec, stretch, sandbox = data["recommended"], data["stretch"], data["sandbox"]
    st.info(
        f"**Comfortable:** `{rec}` · **stretch:** `{stretch}` · **sandbox JSON:** `{sandbox}`"
    )

    st.subheader("Catalog (Q4 Ollama defaults)")
    st.dataframe(data["catalog"], width="stretch", hide_index=True)

    st.subheader("Same 7B, different quant")
    st.dataframe(
        [{"quant": q, "ram_gb": gb} for q, gb in data["quant_7b_ram_gb"].items()],
        width="stretch",
        hide_index=True,
    )

    with st.expander("Formula"):
        st.markdown(
            """
`RAM ≈ params_B × bytes/param + 1.5 GB runtime`

| Quant | bytes/param | typical Ollama |
|---|---|---|
| Q4_K_M | 0.55 | default `:7b` / `:14b` tags |
| Q5 | 0.70 | чуть лучше Q4, заметно больше RAM |
| Q8 | 1.05 | почти FP16 по качеству, ~2× Q4 |
| FP16 | 2.00 | без квантизации, редко для ноутбука |

GGUF = контейнер весов для llama.cpp. Ollama крутит GGUF, не «магический другой формат».
Длинный context (KV-cache) сверху. Поэтому **recommended** оставляет запас, **stretch** - впритык.
"""
        )

    installed = data["installed"]
    st.subheader("Installed in Ollama")
    if installed:
        st.dataframe(installed, width="stretch", hide_index=True)
    else:
        st.warning("Ollama не отвечает на `localhost:11434`. Урок не требует pull.")

    st.caption("Этот урок ничего не качает. Pull - отдельное решение, когда поймёшь цифры.")


if __name__ == "__main__":
    st.set_page_config(page_title="06 GGUF", page_icon=":material/memory:", layout="centered")
    render()
