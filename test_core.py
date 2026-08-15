"""POC: verify that identity/personas/expert.md is actually parsed by OpenAkita.

The parsing logic below is a line-by-line port of OpenAkita v1.27.40:
  src/openakita/agent/persona.py::_parse_preset_field
  src/openakita/agent/persona.py::_parse_dimension_from_style
  src/openakita/agent/persona.py::PersonaManager.load_preset
  src/openakita/agent/persona.py::PersonaManager.get_persona_prompt_section
  src/openakita/prompt/budget.py::estimate_tokens

Run: python /app/test_core.py
Exit code 0 = the persona file is engine-valid.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

PERSONA_PATH = Path(__file__).parent / "identity" / "personas" / "expert.md"

# Injected-prompt budget. SOUL.md budget in OpenAkita is 3600 tokens
# (src/openakita/api/routes/identity.py::_BUDGET_MAP); a persona that costs more
# than the whole soul on every turn is a defect, so cap it here.
MAX_INJECTED_TOKENS = 3000

# ---------------------------------------------------------------------------
# Ported from openakita/agent/persona.py (exact regexes)
# ---------------------------------------------------------------------------

PARSED_SECTIONS = {
    "personality": "性格特征",
    "communication_style": "沟通风格",
    "prompt_snippet": "提示词片段",
    "sticker_config": "表情包配置",
}

DIMENSION_LABELS = {
    "formality": "正式程度",
    "humor": "幽默感",
    "reply_length": "回复长度",
    "emotional_distance": "情感距离",
    "emoji_usage": "表情使用",
}

# PERSONA_DIMENSIONS ranges from persona.py
ENUM_RANGES = {
    "formality": ["very_formal", "formal", "neutral", "casual", "very_casual"],
    "humor": ["none", "occasional", "frequent"],
    "emoji_usage": ["never", "rare", "moderate", "frequent"],
    "reply_length": ["very_short", "short", "moderate", "detailed", "very_detailed"],
    "emotional_distance": ["professional", "friendly", "close", "intimate"],
    "sticker_preference": ["never", "rare", "moderate", "frequent"],
}

EXPECTED = {
    "formality": "neutral",
    "humor": "none",
    "reply_length": "short",
    "emotional_distance": "professional",
    "emoji_usage": "never",
    "sticker_preference": "never",
}


def parse_preset_field(content: str, section_name: str) -> str:
    pattern = rf"## {re.escape(section_name)}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else ""


def parse_dimension_from_style(style_text: str, dimension: str) -> str | None:
    label = DIMENSION_LABELS.get(dimension, "")
    if not label:
        return None
    pattern = rf"-\s*{re.escape(label)}:\s*(\w+)"
    match = re.search(pattern, style_text)
    if match:
        return match.group(1).strip()
    return None


def parse_sticker_frequency(sticker_text: str) -> str | None:
    m = re.search(r"使用频率:\s*(\w+)", sticker_text)
    return m.group(1).strip() if m else None


def estimate_tokens_openakita(text: str) -> int:
    """Port of openakita/prompt/budget.py::estimate_tokens."""
    if not text:
        return 0
    chinese_chars = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    total_chars = len(text)
    english_chars = total_chars - chinese_chars
    return int(chinese_chars / 1.5 + english_chars / 4)


def estimate_tokens_cyrillic_aware(text: str) -> int:
    """Cyrillic is ~2 chars/token on BPE tokenizers; latin ~4; CJK ~1.5.

    Labelled [ESTIMATE] - not an OpenAkita function, used only to expose the real
    system-prompt cost, because budget.py divides all non-CJK chars by 4 and so
    underestimates Cyrillic.
    """
    if not text:
        return 0
    cjk = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    cyr = sum(1 for c in text if "\u0400" <= c <= "\u04ff")
    other = len(text) - cjk - cyr
    return int(cjk / 1.5 + cyr / 2 + other / 4)


def build_prompt_section(preset_name: str, parsed: dict[str, str]) -> str:
    """Port of PersonaManager.get_persona_prompt_section (no user traits, no
    context adaptation - those are runtime-only layers)."""
    parts = [f"## 当前人格: {preset_name}"]
    if parsed["prompt_snippet"]:
        parts.append(f"\n### 角色设定\n{parsed['prompt_snippet']}")
    if parsed["communication_style"]:
        parts.append(f"\n### 沟通风格\n{parsed['communication_style']}")
    if parsed["sticker_config"]:
        parts.append(f"\n### 表情包配置\n{parsed['sticker_config']}")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Lint helpers
# ---------------------------------------------------------------------------

EMOJI_RANGES = [
    (0x1F000, 0x1FAFF),  # pictographs, emoticons, symbols, flags, extended-A
    (0x2600, 0x27BF),  # misc symbols + dingbats (includes U+2705, U+26A0)
    (0x2B00, 0x2BFF),  # misc symbols and arrows (includes U+2B50)
    (0xFE0F, 0xFE0F),  # variation selector-16 (emoji presentation)
    (0x1F1E6, 0x1F1FF),  # regional indicators
    (0x2049, 0x2049),
    (0x203C, 0x203C),
    (0x2122, 0x2122),
    (0x00A9, 0x00A9),
    (0x00AE, 0x00AE),
]

# Phrases the persona forbids. They MAY appear in the file only on a line that
# also carries an explicit prohibition, otherwise the file contradicts itself.
BANNED_PHRASES = [
    "ты абсолютно прав",
    "отличный вопрос",
    "надеюсь, это поможет",
    "нужно ли что-то ещё",
]
PROHIBITION_MARKERS = [
    "never",
    "no ",
    "banned",
    "не ",
    "нет",
    "запрещ",
    "никак",
    "никогда",
]

REQUIRED_RULE_IDS = [
    "1.1", "1.2", "1.3", "1.4", "1.5", "1.6",
    "2.1", "2.2", "2.3", "2.4",
    "3.1", "3.2", "3.3", "3.4", "3.5",
    "4.1", "4.2", "4.3", "4.4",
    "5.1", "5.2", "5.3", "5.4",
    "6.1", "6.2", "6.3", "6.4", "6.5", "6.6",
    "7.1", "7.2", "7.3", "7.4", "7.5",
    "8.1", "8.2", "8.3",
    "9.1", "9.2", "9.3", "9.4", "9.5",
]


def find_emoji(text: str) -> list[tuple[int, str, str]]:
    hits = []
    for idx, ch in enumerate(text):
        cp = ord(ch)
        for lo, hi in EMOJI_RANGES:
            if lo <= cp <= hi:
                try:
                    name = unicodedata.name(ch)
                except ValueError:
                    name = "UNNAMED"
                hits.append((idx, f"U+{cp:04X}", name))
                break
    return hits


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

failures: list[str] = []
checks: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    checks.append((name, ok, detail))
    if not ok:
        failures.append(f"{name}: {detail}")


def main() -> int:
    print("=" * 78)
    print("POC: OpenAkita persona file parse verification")
    print(f"file: {PERSONA_PATH}")
    print("=" * 78)

    # 1. file exists + UTF-8
    if not PERSONA_PATH.exists():
        print(f"FAIL: file not found: {PERSONA_PATH}")
        return 1
    raw = PERSONA_PATH.read_bytes()
    try:
        content = raw.decode("utf-8")
        check("utf-8 decodable", True, f"{len(raw)} bytes")
    except UnicodeDecodeError as e:
        check("utf-8 decodable", False, str(e))
        print("FAIL: not UTF-8")
        return 1

    # 2. persona id is filename-safe per identity API sanitiser
    persona_id = PERSONA_PATH.stem
    check(
        "persona id filename-safe",
        re.fullmatch(r"[\w\-.]+", persona_id) is not None,
        f"id={persona_id}",
    )

    # 3. section headings exist in the exact form the regex requires
    for key, cn in PARSED_SECTIONS.items():
        exact = re.search(rf"^## {re.escape(cn)}[ \t]*$", content, re.MULTILINE)
        check(f"heading exact '## {cn}'", exact is not None, f"section={key}")

    # 4. sections parse non-empty
    parsed = {k: parse_preset_field(content, cn) for k, cn in PARSED_SECTIONS.items()}
    for key, cn in PARSED_SECTIONS.items():
        val = parsed[key]
        check(
            f"section '{cn}' non-empty",
            bool(val),
            f"{len(val)} chars" if val else "EMPTY -> engine sees nothing",
        )

    # 5. dimension values parse, match expectation and are enum-valid
    style = parsed["communication_style"]
    for dim, expected in list(EXPECTED.items())[:5]:
        got = parse_dimension_from_style(style, dim)
        check(f"dimension {dim} parsed", got is not None, f"got={got}")
        check(f"dimension {dim} == {expected}", got == expected, f"got={got}")
        check(
            f"dimension {dim} in enum",
            got in ENUM_RANGES[dim],
            f"got={got} allowed={ENUM_RANGES[dim]}",
        )

    # 6. sticker frequency
    freq = parse_sticker_frequency(parsed["sticker_config"])
    check("sticker 使用频率 parsed", freq is not None, f"got={freq}")
    check("sticker 使用频率 == never", freq == "never", f"got={freq}")
    check(
        "sticker freq in enum",
        freq in ENUM_RANGES["sticker_preference"],
        f"got={freq}",
    )

    # 7. no emoji anywhere in the file
    emoji_hits = find_emoji(content)
    check(
        "zero emoji codepoints",
        not emoji_hits,
        "clean" if not emoji_hits else f"{len(emoji_hits)} hits: {emoji_hits[:5]}",
    )

    # 8. prompt snippet not truncated: every rule id present
    snippet = parsed["prompt_snippet"]
    missing = [r for r in REQUIRED_RULE_IDS if f"{r} " not in snippet]
    check(
        "all rule ids inside 提示词片段",
        not missing,
        "complete" if not missing else f"missing={missing}",
    )

    # 9. no '## ' line inside the snippet (would truncate it in the engine)
    inner_h2 = re.findall(r"^## .*$", snippet, re.MULTILINE)
    check("no '## ' heading inside snippet", not inner_h2, f"found={inner_h2}")

    # 10. self-contradiction lint: banned phrases only inside prohibitions
    lower = content.lower()
    for phrase in BANNED_PHRASES:
        bad_lines = []
        for line in lower.splitlines():
            if phrase in line and not any(m in line for m in PROHIBITION_MARKERS):
                bad_lines.append(line[:80])
        check(
            f"banned phrase '{phrase}' only in prohibition context",
            not bad_lines,
            f"bad={bad_lines}",
        )

    # 11. hard requirements present in the injected snippet
    required_substrings = {
        "russian output rule": "Reply in Russian",
        "unknown label": "[UNKNOWN]",
        "assumption label": "[ASSUMPTION]",
        "hypothesis label": "[HYPOTHESIS]",
        "verified label": "[VERIFIED]",
        "max 5 questions": "maximum 5 numbered questions",
        "no emoji rule": "No emoji",
        "trait override guard": "mined persona traits",
    }
    for name, needle in required_substrings.items():
        check(f"snippet contains {name}", needle in snippet, f"needle={needle!r}")

    # 12. bilingual completeness: the Russian mirror carries every rule id
    mirror = parse_preset_field(
        content, "Русское зеркало правил (справочно, в prompt не попадает)"
    )
    check("russian mirror section present", bool(mirror), f"{len(mirror)} chars")
    missing_ru = [r for r in REQUIRED_RULE_IDS if f"{r} " not in mirror]
    check(
        "russian mirror covers every rule id",
        not missing_ru,
        "complete" if not missing_ru else f"missing={missing_ru}",
    )

    # 13. build the exact system-prompt injection
    injected = build_prompt_section(persona_id, parsed)
    check(
        "russian mirror NOT injected (cost control)",
        mirror.splitlines()[0] not in injected if mirror else False,
        "confirmed",
    )
    check(
        "personality section NOT injected (engine behaviour)",
        parsed["personality"].splitlines()[0] not in injected,
        "confirmed",
    )

    tok_oa = estimate_tokens_openakita(injected)
    tok_cyr = estimate_tokens_cyrillic_aware(injected)
    check(
        f"injected prompt <= {MAX_INJECTED_TOKENS} tokens (cyrillic-aware)",
        tok_cyr <= MAX_INJECTED_TOKENS,
        f"openakita={tok_oa} cyrillic_aware={tok_cyr}",
    )

    # ---- report ----
    print()
    width = max(len(n) for n, _, _ in checks) + 2
    for name, ok, detail in checks:
        print(f"[{'OK' if ok else 'FAIL'}]".ljust(7) + name.ljust(width) + detail)

    print()
    print("-" * 78)
    print("PARSED VALUES (what PersonaManager.load_preset produces)")
    print("-" * 78)
    for dim in ["formality", "humor", "reply_length", "emotional_distance", "emoji_usage"]:
        print(f"  {dim:20} = {parse_dimension_from_style(style, dim)}")
    print(f"  {'sticker_preference':20} = {freq}")
    print(f"  {'personality':20} = {len(parsed['personality'])} chars (parsed, NOT injected)")

    print()
    print("-" * 78)
    print("SYSTEM PROMPT INJECTION (get_persona_prompt_section output)")
    print(f"chars={len(injected)}  tokens_openakita={tok_oa}  tokens_cyrillic_aware={tok_cyr}")
    print("-" * 78)

    print()
    if failures:
        print(f"RESULT: FAIL ({len(failures)} of {len(checks)} checks failed)")
        for f in failures:
            print(f"  - {f}")
        return 1
    print(f"RESULT: PASS ({len(checks)}/{len(checks)} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
