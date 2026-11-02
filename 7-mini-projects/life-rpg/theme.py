import customtkinter as ctk

# ── Background ──────────────────────────────────────────────────────────────
BG          = "#0d0d0d"   # root window
BG_PANEL    = "#0a0a0a"   # section content area
BG_CARD     = "#141414"   # standard card / panel
BG_CARD_ALT = "#1a1a1a"   # alternate card
BG_NAVBAR   = "#080808"   # top navigation bar
BG_TITLE    = "#101010"   # section-title strip below navbar

# ── Greyscale accent palette ─────────────────────────────────────────────────
GREEN_PRIMARY = "#b0b0b0"   # mid silver
GREEN_DARK    = "#3c3c3c"   # dark grey
GREEN_HOVER   = "#606060"   # hover grey
GREEN_BRIGHT  = "#e8e8e8"   # near-white accent
GREEN_DIM     = "#1e1e1e"   # dark button background
GREEN_FAINT   = "#0c0c0c"   # subtle background tint

# ── Text ─────────────────────────────────────────────────────────────────────
TEXT        = "#f0f0f0"   # near-white
TEXT_MUTED  = "#909090"   # muted grey
TEXT_DIM    = "#606060"   # dim grey
TEXT_DIMMER = "#383838"   # dimmer grey

# ── Misc ─────────────────────────────────────────────────────────────────────
BORDER    = "#2a2a2a"
RED_DIM   = "#1e1414"
RED_HOVER = "#2e1e1e"


def setup() -> None:
    """Apply global CustomTkinter theme settings."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
