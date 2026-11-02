import copy
import json
import os
from datetime import datetime
from tkinter import messagebox

DATA_FILE = "life_rpg_save.json"

_DEFAULT: dict = {
    "player": {
        "name": "Hero",
        "class": "Novice",
        "level": 1,
        "xp": 0,
        "xp_to_next": 100,
        "gold": 0,
        "hours_played": 0,
        "stats": {
            "Intelligence": 1,
            "Health": 1,
            "Discipline": 1,
            "Charisma": 1,
            "Strength": 1,
        },
    },
    "plans": {
        "daily":   {},   # "YYYY-MM-DD" -> [{"text": str, "done": bool}]
        "weekly":  [],   # [{"text": str, "done": bool, "key": "YYYY-Www"}]
        "monthly": [],   # [{"text": str, "done": bool, "key": "YYYY-MM"}]
    },
    "quests": [],
    "dailies": [],
    "achievements": [],
    "event_log": [],
}


class DataManager:
    """Handles all persistent game state: load, save, and log."""

    def __init__(self) -> None:
        self.data: dict = copy.deepcopy(_DEFAULT)

    # ── Persistence ───────────────────────────────────────────────────────────

    def load(self) -> bool:
        if not os.path.exists(DATA_FILE):
            return False
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as fh:
                saved = json.load(fh)
            self._deep_merge(self.data, saved)
            return True
        except Exception as exc:
            messagebox.showerror("Load Error", f"Could not load save file.\n{exc}")
            return False

    def save(self) -> None:
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as fh:
                json.dump(self.data, fh, ensure_ascii=False, indent=4)
        except Exception as exc:
            messagebox.showerror("Save Error", f"Could not save data.\n{exc}")

    # ── Event log ─────────────────────────────────────────────────────────────

    def add_log(self, text: str) -> None:
        self.data["event_log"].append(
            {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "text": text}
        )
        if len(self.data["event_log"]) > 500:
            self.data["event_log"] = self.data["event_log"][-500:]

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def today() -> str:
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def _deep_merge(base: dict, override: dict) -> None:
        for key, val in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(val, dict):
                DataManager._deep_merge(base[key], val)
            else:
                base[key] = val
