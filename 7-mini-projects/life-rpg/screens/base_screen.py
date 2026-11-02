from __future__ import annotations

import customtkinter as ctk
import theme

# Navigation items shown per screen (excluding the current screen itself)
_NAV_MAP: dict[str, list[tuple[str, str]]] = {
    "play": [
        ("Main Menu",       "main_menu"),
        ("Characteristics", "characteristics"),
        ("Achievements",    "achievements"),
        ("Progress",        "progress"),
    ],
    "characteristics": [
        ("Main Menu",    "main_menu"),
        ("Make a Plan",  "play"),
        ("Achievements", "achievements"),
        ("Progress",     "progress"),
    ],
    "achievements": [
        ("Main Menu",       "main_menu"),
        ("Make a Plan",     "play"),
        ("Characteristics", "characteristics"),
        ("Progress",        "progress"),
    ],
    "progress": [
        ("Main Menu",       "main_menu"),
        ("Make a Plan",     "play"),
        ("Characteristics", "characteristics"),
        ("Achievements",    "achievements"),
    ],
}

_TITLES: dict[str, str] = {
    "play":            "Make a Plan",
    "characteristics": "Characteristics",
    "achievements":    "Achievements",
    "progress":        "Progress",
}


class BaseScreen(ctk.CTkFrame):
    """
    Base frame for every in-game screen.

    Layout (top-to-bottom):
      row 0 – navigation bar  (links to other screens)
      row 1 – section title   (name of the current screen)
      row 2 – content area    (filled by sub-classes via self.content)
    """

    def __init__(self, parent: ctk.CTkFrame, app, current_screen: str, **kwargs) -> None:
        super().__init__(parent, fg_color=theme.BG, corner_radius=0, **kwargs)
        self._app = app
        self._current = current_screen

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_navbar()
        self._build_title_bar()
        self._build_content_area()

    # ── Navbar ────────────────────────────────────────────────────────────────

    def _build_navbar(self) -> None:
        bar = ctk.CTkFrame(self, fg_color=theme.BG_NAVBAR, corner_radius=0, height=46)
        bar.grid(row=0, column=0, sticky="ew")
        bar.grid_propagate(False)

        nav_items = _NAV_MAP.get(self._current, [])
        for label, key in nav_items:
            btn = ctk.CTkButton(
                bar,
                text=label,
                width=150,
                height=38,
                corner_radius=0,
                fg_color="transparent",
                hover_color=theme.GREEN_DIM,
                text_color=theme.TEXT_MUTED,
                font=ctk.CTkFont(family="Segoe UI", size=13),
                border_width=0,
                command=lambda k=key: self._navigate(k),
            )
            btn.pack(side="left", padx=1, pady=4)

    def _build_title_bar(self) -> None:
        bar = ctk.CTkFrame(self, fg_color=theme.BG_TITLE, corner_radius=0, height=38)
        bar.grid(row=1, column=0, sticky="ew")
        bar.grid_propagate(False)

        title = _TITLES.get(self._current, "")
        ctk.CTkLabel(
            bar,
            text=title,
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=theme.GREEN_BRIGHT,
        ).pack(fill="x", padx=20, pady=0)

    def _build_content_area(self) -> None:
        self.content = ctk.CTkFrame(self, fg_color=theme.BG_PANEL, corner_radius=0)
        self.content.grid(row=2, column=0, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

    # ── Navigation ────────────────────────────────────────────────────────────

    def _navigate(self, key: str) -> None:
        self._app.show_screen(key)
