from __future__ import annotations

import math
import tkinter as tk
import customtkinter as ctk

import theme
from screens.base_screen import BaseScreen

_PLACEHOLDER_ACHIEVEMENTS: list[tuple[str, str, bool]] = [
    ("First Steps",       "Complete your first task",          True),
    ("Day Warrior",       "Complete all daily tasks",          True),
    ("Week Champion",     "Finish a full week plan",           False),
    ("Brain Power",       "Boost Intelligence 5 times",        False),
    ("Iron Will",         "Log 10 consecutive days",           False),
    ("Health Seeker",     "Boost Health 5 times",              False),
    ("Month Master",      "Complete a full month plan",        False),
    ("Scholar",           "Study for 100 hours",               False),
    ("Legendary",         "Reach character level 10",          False),
    ("Disciplined Mind",  "Complete 30 daily plans in a row",  False),
]


class AchievementsScreen(BaseScreen):
    """
    Achievements screen: scrollable 2-column grid of achievement cards.
    Each card shows a star icon, name and description.
    Unlocked achievements are highlighted.
    """

    def __init__(self, parent: ctk.CTkFrame, app, **kwargs) -> None:
        super().__init__(parent, app, current_screen="achievements", **kwargs)
        self._build_content()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_content(self) -> None:
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        scroll = ctk.CTkScrollableFrame(
            self.content, fg_color=theme.BG_PANEL, corner_radius=0,
        )
        scroll.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        self._populate(scroll)

    def _populate(self, parent: ctk.CTkScrollableFrame) -> None:
        cols = 2
        for col in range(cols):
            parent.grid_columnconfigure(col, weight=1)

        for idx, (name, desc, unlocked) in enumerate(_PLACEHOLDER_ACHIEVEMENTS):
            row = idx // cols
            col = idx % cols
            self._card(parent, row, col, name, desc, unlocked)

    # ── Achievement card ──────────────────────────────────────────────────────

    def _card(
        self,
        parent: ctk.CTkScrollableFrame,
        row: int,
        col: int,
        name: str,
        desc: str,
        unlocked: bool,
    ) -> None:
        card_bg  = theme.BG_CARD_ALT if unlocked else theme.BG_CARD
        name_col = theme.GREEN_BRIGHT if unlocked else theme.TEXT_MUTED
        star_col = theme.GREEN_PRIMARY if unlocked else theme.GREEN_DIM

        card = ctk.CTkFrame(parent, fg_color=card_bg, corner_radius=14)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=14, pady=14)

        # Star icon via Canvas
        star_cv = tk.Canvas(
            inner, width=40, height=40,
            bg=card_bg, highlightthickness=0,
        )
        star_cv.pack(side="left", padx=(0, 12))
        self._draw_star(star_cv, cx=20, cy=20, r=15, color=star_col)

        text_area = ctk.CTkFrame(inner, fg_color="transparent")
        text_area.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            text_area, text=name,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=name_col, anchor="w",
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_area, text=desc,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=theme.TEXT_DIMMER, anchor="w",
        ).pack(anchor="w")

        if unlocked:
            ctk.CTkLabel(
                text_area, text="✓ Unlocked",
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=theme.GREEN_PRIMARY, anchor="w",
            ).pack(anchor="w", pady=(2, 0))

    # ── Drawing helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _draw_star(canvas: tk.Canvas, cx: int, cy: int, r: int, color: str) -> None:
        points: list[float] = []
        for i in range(5):
            outer_a = math.pi / 2 + i * 2 * math.pi / 5
            points += [
                cx + r * math.cos(outer_a),
                cy - r * math.sin(outer_a),
            ]
            inner_a = outer_a + math.pi / 5
            ri = r * 0.42
            points += [
                cx + ri * math.cos(inner_a),
                cy - ri * math.sin(inner_a),
            ]
        canvas.create_polygon(points, outline=color, fill="", width=2)
