import tkinter as tk


class AnimatedBackground(tk.Canvas):
    """
    Static full-window canvas used as the bottom layer behind all widgets.
    Renders a plain solid background matching the app theme.

    NOTE: Never use self._w or self._h — those are reserved tkinter attributes.
          We use _cw / _ch instead.
    """

    _BG = "#0d0d0d"

    def __init__(self, parent: tk.Misc, **kwargs) -> None:
        super().__init__(parent, bg=self._BG, highlightthickness=0, **kwargs)
        self._cw: int = 1
        self._ch: int = 1
        self.bind("<Configure>", self._on_configure)

    def _on_configure(self, event: tk.Event) -> None:
        self._cw, self._ch = event.width, event.height

    # ── Public API (kept for compatibility with app.py) ───────────────────────

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass
