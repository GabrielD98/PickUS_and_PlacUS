import json
from pathlib import Path
from typing import Any

from data import DATA_DIR, SETTINGS_PATH


def read_settings() -> dict[str, Any]:
    """Return settings or an empty dict when the file is missing or invalid."""
    try:
        with open(SETTINGS_PATH, "r") as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
    except (FileNotFoundError, json.JSONDecodeError):
        _initialize_settings_file()
    return {}


def write_settings(settings: dict[str, Any]) -> None:
    _ensure_data_dir()
    with open(SETTINGS_PATH, "w") as file:
        json.dump(settings, file, indent=4)


def _ensure_data_dir() -> None:
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)


def _initialize_settings_file() -> None:
    _ensure_data_dir()
    with open(SETTINGS_PATH, "w") as file:
        json.dump({}, file, indent=4)
