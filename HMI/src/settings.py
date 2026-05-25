import json
from pathlib import Path
from typing import Any

from data import DATA_DIR, DEBUG_SETTINGS_PATH


def read_debug_settings() -> dict[str, Any]:
    try:
        with open(DEBUG_SETTINGS_PATH, "r") as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
    except (FileNotFoundError, json.JSONDecodeError):
        _initialize_settings_file()
    return {}


def write_debug_settings(settings: dict[str, Any]) -> None:
    _ensure_data_dir()
    with open(DEBUG_SETTINGS_PATH, "w") as file:
        json.dump(settings, file, indent=4)


def _ensure_data_dir() -> None:
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)


def _initialize_settings_file() -> None:
    _ensure_data_dir()
    with open(DEBUG_SETTINGS_PATH, "w") as file:
        json.dump({}, file, indent=4)
