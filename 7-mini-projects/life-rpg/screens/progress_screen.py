from __future__ import annotations

import customtkinter as ctk
import theme
from screens.base_screen import BaseScreen


class ProgressScreen(BaseScreen):
    """
    Progress-bar screen — skeleton placeholder.
    Will display XP, stats progress bars, and time-based metrics.
    """

    def __init__(self, parent: ctk.CTkFrame, app, **kwargs) -> None:
        super().__init__(parent, app, current_screen="progress", **kwargs)
        self._build_content()

    def _build_content(self) -> None:
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        center = ctk.CTkFrame(self.content, fg_color="transparent")
        center.grid(row=0, column=0)

        ctk.CTkLabel(
            center,
            text="Progress",
            font=ctk.CTkFont(family="Segoe UI", size=36, weight="bold"),
            text_color=theme.GREEN_BRIGHT,
        ).pack(pady=(0, 16))

        ctk.CTkLabel(
            center,
            text="XP bars, stat tracking and timeline charts\nwill appear here.",
            font=ctk.CTkFont(family="Segoe UI", size=15),
            text_color=theme.TEXT_MUTED,
            justify="center",
        ).pack()

        # ── Preview skeleton bars ─────────────────────────────────────────────
        preview = ctk.CTkFrame(center, fg_color=theme.BG_CARD, corner_radius=14, width=400)
        preview.pack(pady=32, padx=20)
        preview.pack_propagate(False)
        preview.configure(height=200)

        for label, val in [("XP", 0.35), ("Intelligence", 0.55), ("Health", 0.2)]:
            row_f = ctk.CTkFrame(preview, fg_color="transparent")
            row_f.pack(fill="x", padx=22, pady=10)

            ctk.CTkLabel(
                row_f, text=label,
                font=ctk.CTkFont(family="Segoe UI", size=13),
                text_color=theme.TEXT_MUTED, width=110, anchor="w",
            ).pack(side="left")

            bar = ctk.CTkProgressBar(row_f, height=14, corner_radius=6)
            bar.pack(side="left", fill="x", expand=True)
            bar.configure(
                progress_color=theme.GREEN_PRIMARY,
                fg_color=theme.GREEN_DIM,
            )
            bar.set(val)
