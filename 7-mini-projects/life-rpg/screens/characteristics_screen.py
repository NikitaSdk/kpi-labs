from __future__ import annotations

import math
import tkinter as tk
import customtkinter as ctk

import theme
from screens.base_screen import BaseScreen

_INTEL_STATS = ["Focus", "Problem Solving", "Learning Speed", "Memory", "Creativity"]
_HEALTH_STATS = ["Physical Fitness", "Sleep Quality", "Nutrition", "Endurance", "Mindfulness"]


class CharacteristicsScreen(BaseScreen):
    """
    Characteristics screen: three columns.
      Left  – Intelligence characteristics panel
      Center – Player avatar + level info
      Right – Health characteristics panel
    """

    def __init__(self, parent: ctk.CTkFrame, app, **kwargs) -> None:
        super().__init__(parent, app, current_screen="characteristics", **kwargs)
        self._build_content()

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_content(self) -> None:
        self.content.grid_columnconfigure(0, weight=2)
        self.content.grid_columnconfigure(1, weight=1)
        self.content.grid_columnconfigure(2, weight=2)
        self.content.grid_rowconfigure(0, weight=1)

        self._build_stat_panel(col=0, title="Intelligence", stats=_INTEL_STATS)
        self._build_player_card(col=1)
        self._build_stat_panel(col=2, title="Health",        stats=_HEALTH_STATS)

    # ── Stat panel ────────────────────────────────────────────────────────────

    def _build_stat_panel(self, col: int, title: str, stats: list[str]) -> None:
        pad = (16, 6) if col == 0 else (6, 16)
        panel = ctk.CTkFrame(self.content, fg_color=theme.BG_CARD, corner_radius=18)
        panel.grid(row=0, column=col, sticky="nsew", padx=pad, pady=16)
        panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel,
            text=title,
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=theme.GREEN_BRIGHT,
        ).pack(pady=(22, 2))

        ctk.CTkLabel(
            panel,
            text="(characteristics)",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=theme.TEXT_DIMMER,
        ).pack(pady=(0, 10))

        # Divider
        ctk.CTkFrame(panel, fg_color=theme.BORDER, height=1).pack(fill="x", padx=18, pady=6)

        for stat in stats:
            row_f = ctk.CTkFrame(panel, fg_color="transparent")
            row_f.pack(fill="x", padx=20, pady=5)

            ctk.CTkLabel(
                row_f, text=stat,
                font=ctk.CTkFont(family="Segoe UI", size=13),
                text_color=theme.TEXT_MUTED, anchor="w",
            ).pack(side="left")

            ctk.CTkLabel(
                row_f, text="0",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                text_color=theme.GREEN_PRIMARY, anchor="e",
            ).pack(side="right")

        ctk.CTkFrame(panel, fg_color="transparent", height=16).pack()

    # ── Player card ───────────────────────────────────────────────────────────

    def _build_player_card(self, col: int) -> None:
        panel = ctk.CTkFrame(self.content, fg_color=theme.BG_CARD_ALT, corner_radius=18)
        panel.grid(row=0, column=col, sticky="nsew", padx=6, pady=16)
        panel.grid_columnconfigure(0, weight=1)

        # Stick-figure canvas
        fig_canvas = tk.Canvas(
            panel, width=100, height=120,
            bg=theme.BG_CARD_ALT, highlightthickness=0,
        )
        fig_canvas.pack(pady=(28, 8))
        self._draw_stick_figure(fig_canvas, cx=50, cy=60)

        ctk.CTkLabel(
            panel, text="Hero",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=theme.GREEN_BRIGHT,
        ).pack(pady=(6, 4))

        ctk.CTkFrame(panel, fg_color=theme.BORDER, height=1).pack(fill="x", padx=16, pady=6)

        for label, value in [("Level", "1"), ("Hours Played", "0")]:
            row_f = ctk.CTkFrame(panel, fg_color="transparent")
            row_f.pack(fill="x", padx=16, pady=4)

            ctk.CTkLabel(
                row_f, text=label,
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color=theme.TEXT_MUTED, anchor="w",
            ).pack(side="left")

            ctk.CTkLabel(
                row_f, text=value,
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                text_color=theme.GREEN_PRIMARY, anchor="e",
            ).pack(side="right")

        ctk.CTkFrame(panel, fg_color="transparent", height=16).pack()

    # ── Drawing helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _draw_stick_figure(canvas: tk.Canvas, cx: int, cy: int) -> None:
        c = theme.GREEN_PRIMARY
        w = 2
        head_r = 16
        # Head
        canvas.create_oval(
            cx - head_r, cy - 55, cx + head_r, cy - 55 + head_r * 2,
            outline=c, width=w,
        )
        # Body
        canvas.create_line(cx, cy - 23, cx, cy + 12, fill=c, width=w)
        # Arms
        canvas.create_line(cx - 24, cy - 10, cx + 24, cy - 10, fill=c, width=w)
        # Left leg
        canvas.create_line(cx, cy + 12, cx - 20, cy + 42, fill=c, width=w)
        # Right leg
        canvas.create_line(cx, cy + 12, cx + 20, cy + 42, fill=c, width=w)
