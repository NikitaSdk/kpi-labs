from __future__ import annotations

import tkinter as tk

import customtkinter as ctk

import theme
from data_manager import DataManager
from widgets.animated_background import AnimatedBackground
from screens.main_menu import MainMenuScreen
from screens.play_screen import PlayScreen
from screens.characteristics_screen import CharacteristicsScreen
from screens.achievements_screen import AchievementsScreen
from screens.progress_screen import ProgressScreen


_SCREEN_CLASSES: dict[str, type] = {
    "play":            PlayScreen,
    "characteristics": CharacteristicsScreen,
    "achievements":    AchievementsScreen,
    "progress":        ProgressScreen,
}


class App(ctk.CTk):
    """
    Root application window.

    Responsibilities:
      • Window configuration and theming
      • Animated background management
      • Screen lifecycle (create / swap / destroy)
      • Expose shared data manager (self.dm) to screens
    """

    def __init__(self) -> None:
        theme.setup()
        super().__init__()

        self.title("LifeRPG")
        self.geometry("1200x750")
        self.minsize(960, 600)
        self.configure(fg_color=theme.BG)

        self.dm = DataManager()
        self.dm.load()

        self._current_screen: ctk.CTkFrame | None = None

        self._init_layers()
        self.show_screen("main_menu")

    # ── Layer setup ───────────────────────────────────────────────────────────

    def _init_layers(self) -> None:
        # Layer 1 – Animated canvas packed to fill the window.
        # place() on tk.Canvas children of CTk windows causes a Tcl error in
        # Python 3.11 ("bad window path name '1'"), so we use pack() here.
        self._bg = AnimatedBackground(self)
        self._bg.pack(fill="both", expand=True)
        self._bg.start()

        # Layer 2 – Screen container embedded INSIDE the canvas via create_window.
        # This is the standard tkinter pattern for overlaying widgets on a canvas.
        self._container = ctk.CTkFrame(self._bg, fg_color=theme.BG, corner_radius=0)
        self._win_id = self._bg.create_window(8, 8, anchor="nw", window=self._container)
        self._bg.bind("<Configure>", self._on_canvas_resize, add="+")

        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)

    def _on_canvas_resize(self, event: tk.Event) -> None:
        """Keep the content container sized to canvas minus the 8 px border."""
        w = max(event.width - 16, 1)
        h = max(event.height - 16, 1)
        self._bg.itemconfigure(self._win_id, width=w, height=h)

    # ── Screen management ─────────────────────────────────────────────────────

    def show_screen(self, name: str) -> None:
        """Destroy the current screen and replace it with the named one."""
        if self._current_screen is not None:
            self._current_screen.grid_forget()
            self._current_screen.destroy()
            self._current_screen = None

        if name == "main_menu":
            screen: ctk.CTkFrame = MainMenuScreen(self._container, app=self)
        elif name in _SCREEN_CLASSES:
            screen = _SCREEN_CLASSES[name](self._container, app=self)
        else:
            return

        screen.grid(row=0, column=0, sticky="nsew")
        self._current_screen = screen

