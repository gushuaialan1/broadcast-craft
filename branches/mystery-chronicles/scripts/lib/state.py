"""State persistence for broadcast-craft pipeline stages."""

import json
import os


def load(workdir: str, event_name: str, protagonist: str) -> dict:
    """
    Load state from workdir/.broadcast-craft/state/{event}_{protagonist}.json.
    Returns an initial state dict if the file does not exist.
    """
    filename = f"{event_name}_{protagonist}.json"
    filepath = os.path.join(workdir, ".broadcast-craft", "state", filename)

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    return {"event": event_name, "protagonist": protagonist}


def merge(state: dict, stage: str, data: dict) -> dict:
    """
    Merge *data* into *state* under the key *stage*.
    Returns a new dict (shallow copy of state with the stage updated).
    """
    new_state = dict(state)
    new_state[stage] = data
    return new_state


def save(state: dict, workdir: str) -> None:
    """
    Persist *state* back to
    workdir/.broadcast-craft/state/{event}_{protagonist}.json.
    Creates parent directories automatically.
    """
    event = state.get("event", "unknown")
    protagonist = state.get("protagonist", "unknown")
    filename = f"{event}_{protagonist}.json"
    dirpath = os.path.join(workdir, ".broadcast-craft", "state")
    filepath = os.path.join(dirpath, filename)

    os.makedirs(dirpath, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
