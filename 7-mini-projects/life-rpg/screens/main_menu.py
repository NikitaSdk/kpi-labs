from __future__ import annotations

import random

import customtkinter as ctk
import theme


_DAILY_TIPS: list[str] = [
    "Start with the hardest task of the day.",
    "Small, consistent steps beat occasional big leaps.",
    "Track your progress — what gets measured, gets improved.",
    "Rest is part of growth. Don't skip recovery.",
    "Discipline means choosing long-term gain over short-term comfort.",
    "One percent better every day — 37× better in a year.",
    "The best time to start was yesterday. The second best is now.",
]

_BUTTONS: list[tuple[str, str]] = [
    ("Make a Plan",  "play"),
    ("Statistics",   "characteristics"),
    ("Achievements", "achievements"),
    ("Exit",         "exit"),
]


class MainMenuScreen(ctk.CTkFrame):

    def __init__(self, parent: ctk.CTkFrame, app, **kwargs) -> None:
        super().__init__(parent, fg_color="transparent", corner_radius=0, **kwargs)
        self._app = app
        self._build()

    def _build(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center = ctk.CTkFrame(self, fg_color="transparent")
        center.grid(row=0, column=0)

        # ── Logo ──────────────────────────────────────────────────────────────
        ctk.CTkLabel(
            center,
            text="LIFE RPG",
            font=ctk.CTkFont(family="Segoe UI", size=72, weight="bold"),
            text_color=theme.GREEN_BRIGHT,
        ).pack(pady=(0, 6))

        ctk.CTkLabel(
            center,
            text="Level up your real life",
            font=ctk.CTkFont(family="Segoe UI", size=18),
            text_color=theme.TEXT_MUTED,
        ).pack(pady=(0, 28))

        # ── Daily tip (text only) ──────────────────────────────────────────────
        tip_frame = ctk.CTkFrame(
            center,
            fg_color=theme.BG_CARD,
            corner_radius=10,
            border_width=1,
            border_color=theme.BORDER,
        )
        tip_frame.pack(pady=(0, 32), ipadx=10, ipady=6)

        ctk.CTkLabel(
            tip_frame,
            text=random.choice(_DAILY_TIPS),
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=theme.TEXT_DIM,
            wraplength=380,
        ).pack(padx=20, pady=10)

        # ── Menu buttons ──────────────────────────────────────────────────────
        for label, action in _BUTTONS:
            is_exit = action == "exit"
            ctk.CTkButton(
                center,
                text=label,
                width=400,
                height=54,
                corner_radius=10,
                font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"),
                fg_color=theme.RED_DIM    if is_exit else theme.GREEN_DIM,
                hover_color=theme.RED_HOVER if is_exit else theme.GREEN_DARK,
                text_color="#888888"      if is_exit else theme.GREEN_BRIGHT,
                command=lambda a=action: self._on_click(a),
            ).pack(pady=9)

    def _on_click(self, action: str) -> None:
        if action == "exit":
            self._app.quit()
        else:
            self._app.show_screen(action)
