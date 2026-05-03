#!/usr/bin/env python3
"""Broadcast Craft CLI – Book Bridge Orchestrator.

Sub-commands:
    stage     Render a single-stage prompt template to stdout.
    validate  Validate a JSON file against its stage schema.
    pipeline  Render all 5 stage prompts into .broadcast-craft/staging/.
"""

import argparse
import json
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

from lib import prompt_builder, state as state_mod, validator  # noqa: E402

_WORKDIR = os.path.dirname(_SCRIPT_DIR)

_STAGE_MAP = {
    "1": "stage_01",
    "01": "stage_01",
    "stage_01": "stage_01",
    "stage_01_book_anchor": "stage_01",
    "book_anchor": "stage_01",
    "anchor": "stage_01",
    "2": "stage_02",
    "02": "stage_02",
    "stage_02": "stage_02",
    "stage_02_pain_mapping": "stage_02",
    "pain_mapping": "stage_02",
    "pain": "stage_02",
    "3": "stage_03",
    "03": "stage_03",
    "stage_03": "stage_03",
    "stage_03_story_bridge": "stage_03",
    "story_bridge": "stage_03",
    "bridge": "stage_03",
    "4": "stage_04",
    "04": "stage_04",
    "stage_04": "stage_04",
    "stage_04_compose": "stage_04",
    "compose": "stage_04",
    "5": "stage_05",
    "05": "stage_05",
    "stage_05": "stage_05",
    "stage_05_review": "stage_05",
    "review": "stage_05",
}

_TEMPLATE_FILENAME = {
    "stage_01": "stage_01_book_anchor.md",
    "stage_02": "stage_02_pain_mapping.md",
    "stage_03": "stage_03_story_bridge.md",
    "stage_04": "stage_04_compose.md",
    "stage_05": "stage_05_review.md",
}


def _normalize_stage(name: str) -> str:
    key = name.lower().strip()
    mapped = _STAGE_MAP.get(key)
    if mapped is None:
        raise ValueError(
            f"Unknown stage '{name}'. Valid aliases: {sorted(set(_STAGE_MAP.keys()))}"
        )
    return mapped


def _template_path(stage: str) -> str:
    return os.path.join(_WORKDIR, "templates", "prompts", _TEMPLATE_FILENAME[stage])


def _safe_filename(text: str) -> str:
    """Sanitise arbitrary text for use in a filesystem filename."""
    keep = []
    for ch in text:
        if ch.isalnum() or ch in ("_", "-"):
            keep.append(ch)
        else:
            keep.append("_")
    return "".join(keep)[:40]


def _build_context(stage, book_title, target_persona, fallback_theme, platform, duration, workdir):
    """Assemble the rendering context for a given stage."""
    ctx = {
        "book_title": book_title,
        "target_persona": target_persona,
        "fallback_theme": fallback_theme or "",
        "platform": platform,
        "length": duration,
        "audience": {"platform": platform},
        "output": {"duration": duration, "length": duration},
    }

    # Load prior stage outputs from state file
    safe_book = _safe_filename(book_title)
    safe_persona = _safe_filename(target_persona)
    state_key = f"{safe_book}_{safe_persona}"
    state = state_mod.load(workdir, state_key, "book_bridge")

    if stage in ("stage_02", "stage_03", "stage_04", "stage_05"):
        if "stage_01" in state:
            ctx.setdefault("state", {})["stage_01"] = state["stage_01"]

    if stage in ("stage_03", "stage_04", "stage_05"):
        if "stage_02" in state:
            ctx.setdefault("state", {})["stage_02"] = state["stage_02"]

    if stage in ("stage_04", "stage_05"):
        if "stage_03" in state:
            ctx.setdefault("state", {})["stage_03"] = state["stage_03"]

    if stage == "stage_05":
        if "stage_04" in state:
            ctx.setdefault("state", {})["stage_04"] = state["stage_04"]

    return ctx


def cmd_stage(args):
    stage = _normalize_stage(args.stage_name)
    platform = args.platform or "抖音"
    duration = args.length or "60s"
    book = args.book_title
    persona = args.target_persona
    fallback = args.fallback_theme

    ctx = _build_context(
        stage, book, persona, fallback, platform, duration, _WORKDIR
    )
    tpl = _template_path(stage)
    if not os.path.exists(tpl):
        print(f"Error: Template not found: {tpl}", file=sys.stderr)
        sys.exit(1)

    rendered = prompt_builder.render(tpl, ctx)
    print(rendered)


def cmd_validate(args):
    stage = _normalize_stage(args.stage_name)

    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8") as f:
        data = json.load(f)

    is_valid, errors = validator.validate(stage, data)
    if is_valid:
        print(f"✓ {stage} validation passed.")
    else:
        print(f"✗ {stage} validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)


def cmd_pipeline(args):
    platform = args.platform or "抖音"
    duration = args.length or "60s"
    book = args.book_title
    persona = args.target_persona
    fallback = args.fallback_theme

    staging_dir = os.path.join(_WORKDIR, ".broadcast-craft", "staging")
    os.makedirs(staging_dir, exist_ok=True)

    stages = [
        "stage_01",
        "stage_02",
        "stage_03",
        "stage_04",
        "stage_05",
    ]

    for stage in stages:
        ctx = _build_context(
            stage, book, persona, fallback, platform, duration, _WORKDIR
        )
        tpl = _template_path(stage)
        if not os.path.exists(tpl):
            print(f"Warning: Template not found: {tpl}", file=sys.stderr)
            continue

        rendered = prompt_builder.render(tpl, ctx)
        safe_book = _safe_filename(book)
        safe_persona = _safe_filename(persona)
        out_name = f"{stage}_{safe_book}_{safe_persona}.md"
        out_path = os.path.join(staging_dir, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"Generated: {out_path}")

    print(f"\nAll 5 stage prompts written to {staging_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Broadcast Craft CLI – Book Bridge Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s stage stage_01 --book-title "非暴力沟通" --target-persona "30岁管理层升迁瓶颈" --length 60s --platform 抖音
  %(prog)s validate stage_01 --file output.json
  %(prog)s pipeline --book-title "非暴力沟通" --target-persona "30岁管理层升迁瓶颈"
        """,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # stage
    p_stage = sub.add_parser("stage", help="Render a stage prompt to stdout")
    p_stage.add_argument("stage_name", help="Stage name (e.g. stage_01, 01, anchor)")
    p_stage.add_argument("--book-title", required=True, help="Book title")
    p_stage.add_argument("--target-persona", required=True, help="Target audience persona (free text, any demographic)")
    p_stage.add_argument("--fallback-theme", default=None, help="Fallback theme when book info is not retrievable online")
    p_stage.add_argument("--length", default="60s", help="Video duration")
    p_stage.add_argument("--platform", default="抖音", help="Target platform")
    p_stage.set_defaults(func=cmd_stage)

    # validate
    p_val = sub.add_parser("validate", help="Validate JSON against stage schema")
    p_val.add_argument("stage_name", help="Stage name")
    p_val.add_argument("--file", required=True, help="JSON file path")
    p_val.set_defaults(func=cmd_validate)

    # pipeline
    p_pipe = sub.add_parser("pipeline", help="Generate all 5 stage prompts")
    p_pipe.add_argument("--book-title", required=True, help="Book title")
    p_pipe.add_argument("--target-persona", required=True, help="Target audience persona")
    p_pipe.add_argument("--fallback-theme", default=None, help="Fallback theme")
    p_pipe.add_argument("--length", default="60s", help="Video duration")
    p_pipe.add_argument("--platform", default="抖音", help="Target platform")
    p_pipe.set_defaults(func=cmd_pipeline)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
