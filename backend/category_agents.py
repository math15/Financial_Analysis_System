#!/usr/bin/env python3
"""
Category Agents Orchestrator
Runs 47 category-specific agents in strict serial waves. Each agent compares the
category data across two JSON inputs and produces two aligned tables.

Usage:
  python category_agents.py quoteA.json quoteB.json

Environment:
  OPENROUTER_API_KEY    – optional; if present, Kimi K2 via OpenRouter will be called
  OPENROUTER_MODEL      – optional; default: moonshotai/kimi-k2:free

Outputs:
  - Prints a markdown report to stdout
  - Writes per-category markdown files in backend/reports/agents/<category>.md
"""
import os
import sys
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Tuple
import re
from openai import AsyncOpenAI
import asyncio
from config import settings

CATEGORIES: List[str] = [
    'Fire',
    'Buildings combined',
    'Office contents',
    'Business interruption',
    'General',
    'Theft',
    'Money',
    'Glass',
    'Fidelity guarantee',
    'Goods in transit',
    'Business all risks',
    'Accidental damage',
    'Public liability',
    "Employers' liability",
    'Stated benefits',
    'Group personal accident',
    'Motor personal accident',
    'Motor General',
    'Motor Specific/Specified',
    'Motor Fleet',
    'Electronic equipment',
    'Umbrella liability',
    'Assist/Value services/  VAS',
    'SASRIA',
    'Intermediary fee',
    'Accounts receivable',
    'Accidental Damage',
    "Employers' Liability",
    'Group Personal Accident/Stated Benefits',
    'Motor Industry Risks',
    'Houseowners',
    'Machinery Breakdown',
    'Householders',
    'Personal, All Risks',
    'Watercraft',
    'Personal Legal Liability',
    'Deterioration of Stock',
    'Personal Umbrella Liability',
    'Greens and Irrigation Systems',
    'Commercial Umbrella Liability',
    'Professional Indemnity',
    'Cyber',
    'Community & Sectional Title',
    'Plant All risk',
    'Contractor All Risk',
    'Hospitality',
    'Total/Final/Debit order Premium incl. VAT',
]

# 47 categories → waves of 10,10,10,10,7
WAVES: List[List[str]] = [
    CATEGORIES[0:10],
    CATEGORIES[10:20],
    CATEGORIES[20:30],
    CATEGORIES[30:40],
    CATEGORIES[40:47],
]

REPORTS_DIR = Path(__file__).resolve().parent / 'reports' / 'agents'
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', settings.OPENROUTER_API_KEY)
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', settings.OPENROUTER_MODEL)

PROMPT_TEMPLATE = (
    "You are a specialist comparison agent for AGENT_CATEGORY.\n"
    "TASK: Do a comprehensive factual comparison with ALL details in your own AGENT_CATEGORY section of these quotes.\n"
    "RULES:\n"
    "- Do NOT omit any item. Every line and value is important.\n"
    "- Preserve original wording (no rewriting).\n"
    "- Normalize currencies to ZAR if present; otherwise copy as-is.\n"
    "- If a feature is Not covered/Not included, mark it clearly and add a red flag token [NOT COVERED].\n"
    "- Create separate tables for each quote with same row order for direct comparison.\n"
    "- Columns: Item | Detail/Value | Notes.\n"
    "INPUT QUOTE A (AGENT_CATEGORY):\n{A}\n\n"
    "INPUT QUOTE B (AGENT_CATEGORY):\n{B}\n\n"
    "{C_SECTION}"
    "OUTPUT:\n"
    "Return strict markdown only:\n"
    "### AGENT_CATEGORY\n"
    "#### Table A – Quote A\n"
    "| Item | Detail/Value | Notes |\n|---|---|---|\n"
    "...rows...\n\n"
    "#### Table B – Quote B\n"
    "| Item | Detail/Value | Notes |\n|---|---|---|\n"
    "...rows...\n"
    "{C_TABLE}"
)


def load_json(path: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def select_category_payload(doc: Dict[str, Any], category: str) -> Any:
    if not isinstance(doc, dict):
        return None
    # Case-insensitive match on keys
    for key, value in doc.items():
        if key.strip().lower() == category.strip().lower():
            return value
    # Try fuzzy synonyms for a few known pairs
    syns = {
        "employers' liability": ["employers liability"],
        'motor specific/specified': ['motor specific', 'motor specified'],
        'business all risks': ['all risks', 'business all risk'],
        'electronic equipment': ['computer and electronic equipment', 'computer equipment'],
    }
    cat_l = category.strip().lower()
    for base, variants in syns.items():
        if cat_l == base:
            for v in variants:
                for key, value in doc.items():
                    if key.strip().lower() == v:
                        return value
    return None


def flatten(obj: Any, prefix: str = '') -> List[Tuple[str, str]]:
    rows: List[Tuple[str, str]] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            rows.extend(flatten(v, key))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            key = f"{prefix}[{i}]" if prefix else f"[{i}]"
            rows.extend(flatten(v, key))
    else:
        rows.append((prefix or 'value', str(obj)))
    return rows


def rows_to_markdown(rows: List[Tuple[str, str]]) -> str:
    lines = ["| Item | Detail/Value | Notes |", "|---|---|---|"]
    for k, v in rows:
        val = v.strip().replace('\n', ' ')
        # Flag obvious not covered cases
        note = "[NOT COVERED]" if re.search(r"not\s+(covered|included)", val, re.I) else ""
        lines.append(f"| {k} | {val} | {note} |")
    return "\n".join(lines)


def build_local_markdown(category: str, a_payload: Any, b_payload: Any, c_payload: Any = None) -> str:
    rows_a = flatten(a_payload) if a_payload is not None else [("info", "No data found for this category in Quote A")]
    rows_b = flatten(b_payload) if b_payload is not None else [("info", "No data found for this category in Quote B")]
    rows_c = flatten(c_payload) if c_payload is not None else None
    md_a = rows_to_markdown(rows_a)
    md_b = rows_to_markdown(rows_b)
    out = []
    out.append(f"### {category}")
    out.append("#### Table A – Quote A")
    out.append(md_a)
    out.append("")
    out.append("#### Table B – Quote B")
    out.append(md_b)
    out.append("")
    if rows_c is not None:
        md_c = rows_to_markdown(rows_c)
        out.append("#### Table C – Quote C")
        out.append(md_c)
        out.append("")
    return "\n".join(out)


async def call_kimi_k2(category: str, a_payload: Any, b_payload: Any, c_payload: Any = None) -> str:
    if not OPENROUTER_API_KEY:
        return build_local_markdown(category, a_payload, b_payload)
    client = AsyncOpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL
    )
   
    # Handle 3-quote scenario
    c_section = ""
    c_table = ""
    if c_payload is not None:
        c_section = f"INPUT QUOTE C (AGENT_CATEGORY):\n{json.dumps(c_payload, ensure_ascii=False, indent=2)}\n\n"
        c_table = "\n#### Table C – Quote C\n| Item | Detail/Value | Notes |\n|---|---|---|\n...rows...\n"
   
    prompt = PROMPT_TEMPLATE.format(
        A=json.dumps(a_payload, ensure_ascii=False, indent=2),
        B=json.dumps(b_payload, ensure_ascii=False, indent=2),
        C_SECTION=c_section,
        C_TABLE=c_table
    ).replace('AGENT_CATEGORY', category)
    try:
        completion = await client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.0,
        )
        text = completion.choices[0].message.content
        if not text.strip():
            return build_local_markdown(category, a_payload, b_payload)
        return text
    except Exception as e:
        print(f"Error calling OpenRouter API for {category}: {e}", file=sys.stderr)
        return build_local_markdown(category, a_payload, b_payload)


async def run_wave(wave_categories: List[str], doc_a: Dict[str, Any], doc_b: Dict[str, Any], doc_c: Dict[str, Any] = None) -> Dict[str, str]:
    results: Dict[str, str] = {}
    tasks = []
    for cat in wave_categories:
        a_payload = select_category_payload(doc_a, cat)
        b_payload = select_category_payload(doc_b, cat)
        c_payload = select_category_payload(doc_c, cat) if doc_c else None
        tasks.append(call_kimi_k2(cat, a_payload, b_payload, c_payload))
    
    # Run all tasks in parallel and collect results
    task_results = await asyncio.gather(*tasks, return_exceptions=True)
    for i, cat in enumerate(wave_categories):
        try:
            if isinstance(task_results[i], Exception):
                results[cat] = build_local_markdown(cat, None, None)
            else:
                results[cat] = task_results[i]
        except Exception:
            results[cat] = build_local_markdown(cat, None, None)
    return results


def save_category_markdown(category: str, content: str) -> None:
    safe = re.sub(r"[^a-z0-9._-]+", "_", category.lower())
    path = REPORTS_DIR / f"{safe}.md"
    path.write_text(content, encoding='utf-8')


async def main() -> None:
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python category_agents.py quoteA.json quoteB.json [quoteC.json]", file=sys.stderr)
        sys.exit(1)
    doc_a = load_json(sys.argv[1])
    doc_b = load_json(sys.argv[2])
    doc_c = load_json(sys.argv[3]) if len(sys.argv) == 4 else None

    quotes_count = 3 if doc_c else 2
    print(f"# Category Agents Comparison ({quotes_count} quotes)\n")
    print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    all_results: Dict[str, str] = {}
    for wave_index, wave in enumerate(WAVES, start=1):
        print(f"## Wave {wave_index} – categories {wave[0]} ... {wave[-1]}\n")
        wave_results = await run_wave(wave, doc_a, doc_b, doc_c)
        # strict serial: wait for wave to complete before next
        for cat in wave:
            content = wave_results.get(cat, build_local_markdown(cat, None, None))
            all_results[cat] = content
            save_category_markdown(cat, content)
            print(content)
            print("\n---\n")

    # Write an index file linking all categories
    index_lines = ["# Agents Output Index\n"]
    for cat in CATEGORIES:
        safe = re.sub(r"[^a-z0-9._-]+", "_", cat.lower())
        index_lines.append(f"- {cat}: reports/agents/{safe}.md")
    (REPORTS_DIR.parent / 'agents_index.md').write_text("\n".join(index_lines), encoding='utf-8')

    print("All waves completed.")


if __name__ == '__main__':
    asyncio.run(main()) 