"""JSON Schema validation with optional jsonschema and a built-in fallback."""

import json
import os
import warnings


def validate(stage: str, data: dict) -> tuple[bool, list[str]]:
    """
    Validate *data* against templates/schemas/{stage}.json.

    Returns (is_valid, error_messages).
    If ``jsonschema`` is unavailable a lightweight type-checking fallback is used.
    """
    schema_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "templates", "schemas", f"{stage}.json"
    )
    schema_path = os.path.abspath(schema_path)

    if not os.path.exists(schema_path):
        return False, [f"Schema file not found: {schema_path}"]

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    # Prefer jsonschema when available
    try:
        import jsonschema

        validator_cls = getattr(jsonschema, "Draft7Validator", jsonschema.Draft202012Validator)
        validator = validator_cls(schema)
        errors = list(validator.iter_errors(data))
        if errors:
            messages = []
            for err in errors:
                path = "/".join(str(p) for p in err.path) or "root"
                messages.append(f"[{path}] {err.message}")
            return False, messages
        return True, []
    except ImportError:
        pass

    # Fallback: resolve $refs and do basic structural validation
    resolved = _resolve_refs(schema, schema)
    errors = _validate_basic(data, resolved, [])
    return (not errors), errors


def _resolve_refs(node, root):
    """Recursively inline ``$ref`` references (local #/definitions/… only)."""
    if isinstance(node, dict):
        if "$ref" in node:
            ref = node["$ref"]
            if ref.startswith("#/"):
                parts = ref.split("/")[1:]
                current = root
                for part in parts:
                    current = current[part]
                return _resolve_refs(current, root)
        return {k: _resolve_refs(v, root) for k, v in node.items()}
    if isinstance(node, list):
        return [_resolve_refs(item, root) for item in node]
    return node


def _validate_basic(data, schema, path):
    """Lightweight recursive validator for draft-07-ish schemas."""
    errors = []
    schema_type = schema.get("type")

    # Handle composite types first
    if "anyOf" in schema and schema_type is None:
        any_ok = False
        for sub in schema["anyOf"]:
            sub_errors = _validate_basic(data, sub, path)
            if not sub_errors:
                any_ok = True
                break
        if not any_ok:
            errors.append(
                f"[{'/'.join(path) or 'root'}] Value does not match anyOf schemas"
            )
        return errors

    if schema_type == "object":
        if not isinstance(data, dict):
            errors.append(
                f"[{'/'.join(path) or 'root'}] Expected object, got {type(data).__name__}"
            )
            return errors
        for req in schema.get("required", []):
            if req not in data:
                errors.append(
                    f"[{'/'.join(path) or 'root'}] Missing required field: {req}"
                )
        for key, prop_schema in schema.get("properties", {}).items():
            if key in data:
                errors.extend(_validate_basic(data[key], prop_schema, path + [key]))
        return errors

    if schema_type == "array":
        if not isinstance(data, list):
            errors.append(
                f"[{'/'.join(path) or 'root'}] Expected array, got {type(data).__name__}"
            )
            return errors
        items_schema = schema.get("items")
        if items_schema:
            for i, item in enumerate(data):
                errors.extend(_validate_basic(item, items_schema, path + [str(i)]))
        if "minItems" in schema and len(data) < schema["minItems"]:
            errors.append(
                f"[{'/'.join(path) or 'root'}] Array too short: {len(data)} < {schema['minItems']}"
            )
        if "maxItems" in schema and len(data) > schema["maxItems"]:
            errors.append(
                f"[{'/'.join(path) or 'root'}] Array too long: {len(data)} > {schema['maxItems']}"
            )
        return errors

    if schema_type == "string":
        if not isinstance(data, str):
            errors.append(
                f"[{'/'.join(path) or 'root'}] Expected string, got {type(data).__name__}"
            )
            return errors
        if "maxLength" in schema and len(data) > schema["maxLength"]:
            errors.append(
                f"[{'/'.join(path) or 'root'}] String too long: {len(data)} > {schema['maxLength']}"
            )
        if "enum" in schema and data not in schema["enum"]:
            errors.append(
                f"[{'/'.join(path) or 'root'}] Invalid value {data!r}, expected one of {schema['enum']}"
            )
        return errors

    if schema_type == "integer":
        if not isinstance(data, int) or isinstance(data, bool):
            errors.append(
                f"[{'/'.join(path) or 'root'}] Expected integer, got {type(data).__name__}"
            )
            return errors
        if "minimum" in schema and data < schema["minimum"]:
            errors.append(
                f"[{'/'.join(path) or 'root'}] Value too small: {data} < {schema['minimum']}"
            )
        if "maximum" in schema and data > schema["maximum"]:
            errors.append(
                f"[{'/'.join(path) or 'root'}] Value too large: {data} > {schema['maximum']}"
            )
        return errors

    if schema_type == "number":
        if not isinstance(data, (int, float)) or isinstance(data, bool):
            errors.append(
                f"[{'/'.join(path) or 'root'}] Expected number, got {type(data).__name__}"
            )
            return errors
        if "minimum" in schema and data < schema["minimum"]:
            errors.append(
                f"[{'/'.join(path) or 'root'}] Value too small: {data} < {schema['minimum']}"
            )
        if "maximum" in schema and data > schema["maximum"]:
            errors.append(
                f"[{'/'.join(path) or 'root'}] Value too large: {data} > {schema['maximum']}"
            )
        return errors

    if schema_type == "boolean":
        if not isinstance(data, bool):
            errors.append(
                f"[{'/'.join(path) or 'root'}] Expected boolean, got {type(data).__name__}"
            )
        return errors

    if schema_type == "null":
        if data is not None:
            errors.append(
                f"[{'/'.join(path) or 'root'}] Expected null, got {type(data).__name__}"
            )
        return errors

    # Unhandled type – warn but do not block
    if schema_type:
        warnings.warn(
            f"Fallback validator does not handle type '{schema_type}'",
            stacklevel=2,
        )

    return errors
