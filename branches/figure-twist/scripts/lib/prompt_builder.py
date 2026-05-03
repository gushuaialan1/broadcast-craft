"""Prompt template renderer supporting {{dot.path}} placeholders."""

import json
import re
import warnings


_RE_PLACEHOLDER = re.compile(r"\{\{([^{}]+?)\}\}", re.DOTALL)


def render(template_path: str, context: dict) -> str:
    """
    Read a markdown template and replace {{dot.path}} placeholders with values
    from *context*.

    Supported syntax:
        {{var}}
        {{obj.field}}
        {{arr[0]}}
        {{expr | json}}
        {{expr | join}}
        {{arr[other.field - 1].name}}

    Missing paths are replaced with an empty string and a warning is emitted.
    """
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    def _replacer(match: re.Match) -> str:
        expr = match.group(1).strip()
        try:
            value = _resolve(expr, context)
        except Exception as exc:  # noqa: BLE001
            warnings.warn(
                f"Failed to resolve placeholder '{{{{{expr}}}}}': {exc}",
                stacklevel=2,
            )
            return ""
        return str(value) if value is not None else ""

    return _RE_PLACEHOLDER.sub(_replacer, template)


def _resolve(expr: str, context: dict) -> str:
    """Evaluate an expression, applying any trailing filters."""
    parts = [p.strip() for p in expr.split("|")]
    raw_value = _eval_value(parts[0], context)

    for filt in parts[1:]:
        raw_value = _apply_filter(filt, raw_value)

    if raw_value is None:
        warnings.warn(
            f"Placeholder '{{{{{expr}}}}} resolved to None", stacklevel=3
        )
        return ""

    return str(raw_value)


def _apply_filter(name: str, value):
    """Apply a built-in filter."""
    if name == "json":
        return json.dumps(value, ensure_ascii=False, indent=2)
    if name == "join":
        if isinstance(value, (list, tuple)):
            return ", ".join(str(x) for x in value)
        return str(value)
    warnings.warn(f"Unknown filter '{name}'", stacklevel=3)
    return value


def _eval_value(expr: str, ctx: dict):
    """Evaluate a value expression (no filters) against a context dict."""
    expr = expr.strip()

    # Simple integer arithmetic: a - 1, a + 2
    m = re.match(r"^(.+?)\s*([+-])\s*(\d+)$", expr)
    if m:
        left = _eval_value(m.group(1).strip(), ctx)
        if left is None:
            return None
        op, right = m.group(2), int(m.group(3))
        return left - right if op == "-" else left + right

    tokens = _tokenize(expr)
    value = ctx
    for token in tokens:
        if value is None:
            break
        if isinstance(token, str):
            value = value.get(token) if isinstance(value, dict) else None
        elif isinstance(token, int):
            try:
                value = value[token]
            except (IndexError, TypeError):
                value = None
        elif isinstance(token, tuple) and token[0] == "expr":
            idx = _eval_value(token[1], ctx)
            try:
                value = value[idx]
            except (IndexError, TypeError, KeyError):
                value = None
        else:
            value = None
    return value


def _tokenize(expr: str):
    """Split an expression into attribute / index tokens."""
    tokens = []
    current = ""
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch == ".":
            if current:
                tokens.append(current)
                current = ""
            i += 1
        elif ch == "[":
            if current:
                tokens.append(current)
                current = ""
            j = i + 1
            depth = 1
            while j < len(expr) and depth > 0:
                if expr[j] == "[":
                    depth += 1
                elif expr[j] == "]":
                    depth -= 1
                j += 1
            inner = expr[i + 1 : j - 1]
            try:
                tokens.append(int(inner))
            except ValueError:
                tokens.append(("expr", inner))
            i = j
        else:
            current += ch
            i += 1
    if current:
        tokens.append(current)
    return tokens
