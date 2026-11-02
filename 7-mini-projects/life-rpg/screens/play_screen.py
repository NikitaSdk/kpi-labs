from __future__ import annotations

import tkinter as tk
from datetime import date, timedelta

import customtkinter as ctk
import theme
from screens.base_screen import BaseScreen


_DAY_SHORT = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_DAY_NAMES = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday",
]


def _week_start(d: date) -> date:
    return d - timedelta(days=d.weekday())


def _week_key(d: date) -> str:
    return d.strftime("%G-W%V")


def _month_key(d: date) -> str:
    return d.strftime("%Y-%m")


def _fmt(d: date) -> str:
    return d.strftime("%d %b %Y")


class PlayScreen(BaseScreen):
    """
    Make a Plan screen — two tabs:
      • New Task  — form: description + assign to day / week / month
      • My Plans  — view all saved plans (by day or week/month)
    """

    def __init__(self, parent: ctk.CTkFrame, app, **kwargs) -> None:
        super().__init__(parent, app, current_screen="play", **kwargs)

        # New Task state
        self._picker_offset: int = 0
        self._selected_date: str | None = None
        self._assign_mode = tk.StringVar(value="Specific Day")

        # My Plans state
        self._plans_view = tk.StringVar(value="By Day")
        self._week_offset: int = 0
        self._week_label_var = tk.StringVar()
        self._day_scroll: ctk.CTkScrollableFrame | None = None
        self._overview_scroll: ctk.CTkScrollableFrame | None = None

        self._build_content()

    # ── Root tabview ──────────────────────────────────────────────────────────

    def _build_content(self) -> None:
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self._tabs = ctk.CTkTabview(
            self.content,
            fg_color=theme.BG_PANEL,
            segmented_button_fg_color=theme.BG_NAVBAR,
            segmented_button_selected_color=theme.GREEN_DIM,
            segmented_button_selected_hover_color=theme.GREEN_DARK,
            segmented_button_unselected_color=theme.BG_NAVBAR,
            segmented_button_unselected_hover_color=theme.GREEN_DIM,
            text_color=theme.TEXT,
            text_color_disabled=theme.TEXT_DIM,
            corner_radius=10,
        )
        self._tabs.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        self._tabs.add("New Task")
        self._tabs.add("My Plans")

        self._build_new_task_tab(self._tabs.tab("New Task"))
        self._build_my_plans_tab(self._tabs.tab("My Plans"))

    # ══════════════════════════════════════════════════════════════════════════
    # Tab 1 – New Task
    # ══════════════════════════════════════════════════════════════════════════

    def _build_new_task_tab(self, parent: ctk.CTkFrame) -> None:
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Scrollable outer so form is never clipped
        outer = ctk.CTkScrollableFrame(
            parent, fg_color="transparent",
            scrollbar_button_color=theme.GREEN_DIM,
            scrollbar_button_hover_color=theme.GREEN_HOVER,
        )
        outer.grid(row=0, column=0, sticky="nsew")
        outer.grid_columnconfigure(0, weight=1)
        outer.grid_columnconfigure(2, weight=1)

        panel = ctk.CTkFrame(outer, fg_color=theme.BG_CARD, corner_radius=18)
        panel.grid(row=0, column=1, sticky="ew", pady=20, ipadx=4)
        panel.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(
            panel, text="New Task",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=theme.GREEN_BRIGHT,
        ).pack(anchor="w", padx=28, pady=(28, 0))

        # Description
        ctk.CTkLabel(
            panel, text="Description",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=theme.TEXT_DIM,
        ).pack(anchor="w", padx=28, pady=(16, 2))

        self._task_entry = ctk.CTkTextbox(
            panel, height=90,
            fg_color=theme.BG_CARD_ALT,
            text_color=theme.TEXT,
            border_color=theme.BORDER,
            border_width=1,
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=13),
        )
        self._task_entry.pack(fill="x", padx=28)

        # Assign to
        ctk.CTkLabel(
            panel, text="Assign to",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=theme.TEXT_DIM,
        ).pack(anchor="w", padx=28, pady=(18, 2))

        ctk.CTkSegmentedButton(
            panel,
            values=["Specific Day", "This Week", "This Month"],
            variable=self._assign_mode,
            fg_color=theme.BG_CARD_ALT,
            selected_color=theme.GREEN_DIM,
            selected_hover_color=theme.GREEN_DARK,
            unselected_color=theme.BG_CARD_ALT,
            unselected_hover_color=theme.GREEN_DIM,
            text_color=theme.TEXT_MUTED,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            command=self._on_mode_change,
        ).pack(fill="x", padx=28, pady=(0, 6))

        # Day picker host
        self._picker_host = ctk.CTkFrame(panel, fg_color="transparent")
        self._picker_host.pack(fill="x", padx=28, pady=(4, 0))
        self._picker_host.grid_columnconfigure(0, weight=1)
        self._rebuild_picker()

        # Feedback label
        self._msg_lbl = ctk.CTkLabel(
            panel, text="",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=theme.GREEN_PRIMARY,
        )
        self._msg_lbl.pack(pady=(8, 0))

        # Save button
        ctk.CTkButton(
            panel,
            text="Save to My Plans",
            height=48, corner_radius=10,
            fg_color=theme.GREEN_DIM,
            hover_color=theme.GREEN_DARK,
            text_color=theme.GREEN_BRIGHT,
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            command=self._create_task,
        ).pack(fill="x", padx=28, pady=(12, 28))

    # ── Mode / picker ─────────────────────────────────────────────────────────

    def _on_mode_change(self, _value: str) -> None:
        for w in self._picker_host.winfo_children():
            w.destroy()
        if self._assign_mode.get() == "Specific Day":
            self._rebuild_picker()

    def _rebuild_picker(self) -> None:
        for w in self._picker_host.winfo_children():
            w.destroy()

        ws = _week_start(date.today()) + timedelta(weeks=self._picker_offset)
        we = ws + timedelta(days=6)
        today = date.today()

        nav = ctk.CTkFrame(self._picker_host, fg_color="transparent")
        nav.grid(row=0, column=0, sticky="ew")
        nav.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            nav, text="←", width=30, height=26,
            fg_color=theme.GREEN_DIM, hover_color=theme.GREEN_DARK,
            text_color=theme.TEXT_MUTED, font=ctk.CTkFont(size=13),
            corner_radius=5, command=self._picker_prev,
        ).grid(row=0, column=0, padx=(0, 6))

        ctk.CTkLabel(
            nav, text=f"{ws.strftime('%d %b')} – {we.strftime('%d %b %Y')}",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=theme.TEXT_DIM,
        ).grid(row=0, column=1)

        ctk.CTkButton(
            nav, text="→", width=30, height=26,
            fg_color=theme.GREEN_DIM, hover_color=theme.GREEN_DARK,
            text_color=theme.TEXT_MUTED, font=ctk.CTkFont(size=13),
            corner_radius=5, command=self._picker_next,
        ).grid(row=0, column=2, padx=(6, 0))

        tiles = ctk.CTkFrame(self._picker_host, fg_color="transparent")
        tiles.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        for i in range(7):
            tiles.grid_columnconfigure(i, weight=1)

        for i in range(7):
            d = ws + timedelta(days=i)
            ds = d.strftime("%Y-%m-%d")
            selected = (ds == self._selected_date)
            is_today = (d == today)

            if selected:
                fg, tc = theme.GREEN_DARK, theme.GREEN_BRIGHT
            elif is_today:
                fg, tc = theme.GREEN_DIM, theme.TEXT_MUTED
            else:
                fg, tc = theme.BG_CARD_ALT, theme.TEXT_DIMMER

            ctk.CTkButton(
                tiles,
                text=f"{_DAY_SHORT[i]}\n{d.strftime('%d')}",
                height=50, fg_color=fg,
                hover_color=theme.GREEN_HOVER, text_color=tc,
                font=ctk.CTkFont(family="Segoe UI", size=10),
                corner_radius=7,
                command=lambda ds=ds: self._pick_day(ds),
            ).grid(row=0, column=i, padx=2, sticky="ew")

    def _pick_day(self, date_str: str) -> None:
        self._selected_date = date_str
        self._rebuild_picker()

    def _picker_prev(self) -> None:
        self._picker_offset -= 1
        self._rebuild_picker()

    def _picker_next(self) -> None:
        self._picker_offset += 1
        self._rebuild_picker()

    # ── Save ──────────────────────────────────────────────────────────────────

    def _create_task(self) -> None:
        text = self._task_entry.get("1.0", "end").strip()
        if not text:
            self._flash("Please enter a description.", error=True)
            return

        mode = self._assign_mode.get()
        dm = self._app.dm
        today = date.today()

        if mode == "Specific Day":
            ds = self._selected_date or today.strftime("%Y-%m-%d")
            dm.data["plans"]["daily"].setdefault(ds, []).append(
                {"text": text, "done": False}
            )
        elif mode == "This Week":
            dm.data["plans"]["weekly"].append(
                {"text": text, "done": False, "key": _week_key(today)}
            )
        else:
            dm.data["plans"]["monthly"].append(
                {"text": text, "done": False, "key": _month_key(today)}
            )

        dm.save()
        self._task_entry.delete("1.0", "end")
        self._selected_date = None
        if mode == "Specific Day":
            self._rebuild_picker()
        self._flash("Saved!")

        # Refresh My Plans view if it has been built
        if self._day_scroll is not None:
            self._refresh_day_view()
        if self._overview_scroll is not None:
            self._refresh_overview()

    def _flash(self, msg: str, error: bool = False) -> None:
        color = theme.TEXT_DIM if error else theme.GREEN_PRIMARY
        self._msg_lbl.configure(text=msg, text_color=color)
        self._msg_lbl.after(2200, lambda: self._msg_lbl.configure(text=""))

    # ══════════════════════════════════════════════════════════════════════════
    # Tab 2 – My Plans
    # ══════════════════════════════════════════════════════════════════════════

    def _build_my_plans_tab(self, parent: ctk.CTkFrame) -> None:
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Sub-view selector
        seg = ctk.CTkSegmentedButton(
            parent,
            values=["By Day", "Week / Month"],
            variable=self._plans_view,
            fg_color=theme.BG_NAVBAR,
            selected_color=theme.GREEN_DIM,
            selected_hover_color=theme.GREEN_DARK,
            unselected_color=theme.BG_NAVBAR,
            unselected_hover_color=theme.GREEN_DIM,
            text_color=theme.TEXT_MUTED,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            command=self._switch_plans_view,
        )
        seg.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 8))

        # Host frame — swaps content
        self._plans_host = ctk.CTkFrame(parent, fg_color="transparent")
        self._plans_host.grid(row=1, column=0, sticky="nsew")
        self._plans_host.grid_rowconfigure(0, weight=1)
        self._plans_host.grid_columnconfigure(0, weight=1)

        self._build_by_day_view()

    def _switch_plans_view(self, value: str) -> None:
        for w in self._plans_host.winfo_children():
            w.destroy()
        self._day_scroll = None
        self._overview_scroll = None
        if value == "By Day":
            self._build_by_day_view()
        else:
            self._build_overview_view()

    # ── By Day view ───────────────────────────────────────────────────────────

    def _build_by_day_view(self) -> None:
        host = self._plans_host
        host.grid_rowconfigure(1, weight=1)
        host.grid_columnconfigure(0, weight=1)

        nav = ctk.CTkFrame(host, fg_color="transparent")
        nav.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        nav.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            nav, text="← Prev", width=80, height=30,
            fg_color=theme.GREEN_DIM, hover_color=theme.GREEN_DARK,
            text_color=theme.TEXT_MUTED,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            corner_radius=6, command=self._prev_week,
        ).grid(row=0, column=0, padx=(0, 8))

        ctk.CTkLabel(
            nav, textvariable=self._week_label_var,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=theme.TEXT,
        ).grid(row=0, column=1)

        ctk.CTkButton(
            nav, text="Next →", width=80, height=30,
            fg_color=theme.GREEN_DIM, hover_color=theme.GREEN_DARK,
            text_color=theme.TEXT_MUTED,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            corner_radius=6, command=self._next_week,
        ).grid(row=0, column=2, padx=(8, 0))

        self._day_scroll = ctk.CTkScrollableFrame(
            host, fg_color="transparent",
            scrollbar_button_color=theme.GREEN_DIM,
            scrollbar_button_hover_color=theme.GREEN_HOVER,
        )
        self._day_scroll.grid(row=1, column=0, sticky="nsew")
        self._day_scroll.grid_columnconfigure(0, weight=1)

        self._refresh_day_view()

    def _refresh_day_view(self) -> None:
        if self._day_scroll is None:
            return
        for w in self._day_scroll.winfo_children():
            w.destroy()

        ws = _week_start(date.today()) + timedelta(weeks=self._week_offset)
        we = ws + timedelta(days=6)
        self._week_label_var.set(f"{_fmt(ws)}  –  {_fmt(we)}")

        today = date.today()
        dm = self._app.dm

        for i in range(7):
            day = ws + timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d")
            is_today = (day == today)
            tasks = dm.data["plans"]["daily"].get(date_str, [])
            done_count = sum(1 for t in tasks if t.get("done"))
            total = len(tasks)

            card = ctk.CTkFrame(
                self._day_scroll,
                fg_color=theme.BG_CARD_ALT if is_today else theme.BG_CARD,
                corner_radius=12, border_width=1,
                border_color=theme.GREEN_PRIMARY if is_today else theme.BORDER,
            )
            card.grid(row=i, column=0, sticky="ew", pady=(0, 8), padx=2)
            card.grid_columnconfigure(0, weight=1)

            # Header
            hdr = ctk.CTkFrame(card, fg_color="transparent")
            hdr.grid(row=0, column=0, sticky="ew", padx=14, pady=(10, 4))
            hdr.grid_columnconfigure(0, weight=1)

            day_label = f"{_DAY_NAMES[i]}  ·  {day.strftime('%d %b %Y')}"
            if is_today:
                day_label += "  · today"

            ctk.CTkLabel(
                hdr, text=day_label,
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                text_color=theme.GREEN_BRIGHT if is_today else theme.TEXT_MUTED,
            ).grid(row=0, column=0, sticky="w")

            badge_text = f"{done_count}/{total}" if total else "—"
            badge_color = (
                theme.GREEN_PRIMARY if (total and done_count == total)
                else theme.TEXT_DIMMER
            )
            ctk.CTkLabel(
                hdr, text=badge_text,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                text_color=badge_color,
            ).grid(row=0, column=1, padx=(0, 6))

            # Progress bar
            if total > 0:
                pb = ctk.CTkProgressBar(
                    card, height=3, corner_radius=2,
                    fg_color=theme.BORDER, progress_color=theme.GREEN_PRIMARY,
                )
                pb.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 4))
                pb.set(done_count / total)

            # Tasks
            tf = ctk.CTkFrame(card, fg_color="transparent")
            tf.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 10))

            if not tasks:
                ctk.CTkLabel(
                    tf, text="No tasks",
                    font=ctk.CTkFont(family="Segoe UI", size=11),
                    text_color=theme.TEXT_DIMMER,
                ).pack(anchor="w")
            else:
                for idx, task in enumerate(tasks):
                    self._render_row(
                        tf, task,
                        on_toggle=lambda ds=date_str, ix=idx: self._toggle_day(ds, ix),
                        on_delete=lambda ds=date_str, ix=idx: self._delete_day(ds, ix),
                    )

    def _toggle_day(self, date_str: str, idx: int) -> None:
        tasks = self._app.dm.data["plans"]["daily"].get(date_str, [])
        if 0 <= idx < len(tasks):
            tasks[idx]["done"] = not tasks[idx].get("done", False)
            self._app.dm.save()
            self._refresh_day_view()

    def _delete_day(self, date_str: str, idx: int) -> None:
        tasks = self._app.dm.data["plans"]["daily"].get(date_str, [])
        if 0 <= idx < len(tasks):
            tasks.pop(idx)
            self._app.dm.save()
            self._refresh_day_view()

    def _prev_week(self) -> None:
        self._week_offset -= 1
        self._refresh_day_view()

    def _next_week(self) -> None:
        self._week_offset += 1
        self._refresh_day_view()

    # ── Week / Month view ─────────────────────────────────────────────────────

    def _build_overview_view(self) -> None:
        host = self._plans_host
        host.grid_rowconfigure(0, weight=1)
        host.grid_columnconfigure(0, weight=1)

        self._overview_scroll = ctk.CTkScrollableFrame(
            host, fg_color="transparent",
            scrollbar_button_color=theme.GREEN_DIM,
            scrollbar_button_hover_color=theme.GREEN_HOVER,
        )
        self._overview_scroll.grid(row=0, column=0, sticky="nsew")
        self._overview_scroll.grid_columnconfigure(0, weight=1)

        self._refresh_overview()

    def _refresh_overview(self) -> None:
        if self._overview_scroll is None:
            return
        for w in self._overview_scroll.winfo_children():
            w.destroy()

        today = date.today()
        ws = _week_start(today)
        we = ws + timedelta(days=6)
        iso_week = today.isocalendar()[1]

        self._build_overview_card(
            row=0,
            title=f"THIS WEEK  ·  Week {iso_week}  ({_fmt(ws)} – {_fmt(we)})",
            key=_week_key(today), kind="weekly",
        )
        ctk.CTkFrame(
            self._overview_scroll, fg_color="transparent", height=14,
        ).grid(row=1, column=0)
        self._build_overview_card(
            row=2,
            title=f"THIS MONTH  ·  {today.strftime('%B %Y')}",
            key=_month_key(today), kind="monthly",
        )

    def _build_overview_card(self, row: int, title: str, key: str, kind: str) -> None:
        dm = self._app.dm
        all_tasks: list[dict] = dm.data["plans"][kind]
        matching = [(i, t) for i, t in enumerate(all_tasks) if t.get("key") == key]
        total = len(matching)
        done_count = sum(1 for _, t in matching if t.get("done"))

        card = ctk.CTkFrame(
            self._overview_scroll,
            fg_color=theme.BG_CARD, corner_radius=12,
            border_width=1, border_color=theme.BORDER,
        )
        card.grid(row=row, column=0, sticky="ew", padx=2, pady=4)
        card.grid_columnconfigure(0, weight=1)

        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 4))
        hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            hdr, text=title,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=theme.TEXT_MUTED,
        ).grid(row=0, column=0, sticky="w")

        badge_text = f"{done_count}/{total}" if total else "—"
        badge_color = (
            theme.GREEN_PRIMARY if (total and done_count == total)
            else theme.TEXT_DIMMER
        )
        ctk.CTkLabel(
            hdr, text=badge_text,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=badge_color,
        ).grid(row=0, column=1, padx=(0, 6))

        if total > 0:
            pb = ctk.CTkProgressBar(
                card, height=3, corner_radius=2,
                fg_color=theme.BORDER, progress_color=theme.GREEN_PRIMARY,
            )
            pb.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 4))
            pb.set(done_count / total)

        tf = ctk.CTkFrame(card, fg_color="transparent")
        tf.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 12))

        if not matching:
            ctk.CTkLabel(
                tf, text="No plans yet",
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=theme.TEXT_DIMMER,
            ).pack(anchor="w")
        else:
            for idx, task in matching:
                self._render_row(
                    tf, task,
                    on_toggle=lambda ix=idx, k=kind: self._toggle_overview(k, ix),
                    on_delete=lambda ix=idx, k=kind: self._delete_overview(k, ix),
                )

    def _toggle_overview(self, kind: str, idx: int) -> None:
        tasks = self._app.dm.data["plans"][kind]
        if 0 <= idx < len(tasks):
            tasks[idx]["done"] = not tasks[idx].get("done", False)
            self._app.dm.save()
            self._refresh_overview()

    def _delete_overview(self, kind: str, idx: int) -> None:
        tasks = self._app.dm.data["plans"][kind]
        if 0 <= idx < len(tasks):
            tasks.pop(idx)
            self._app.dm.save()
            self._refresh_overview()

    # ── Shared task row ───────────────────────────────────────────────────────

    @staticmethod
    def _render_row(
        parent: ctk.CTkFrame,
        task: dict,
        on_toggle,
        on_delete,
    ) -> None:
        done = task.get("done", False)
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=2)

        ctk.CTkButton(
            row,
            text="✓" if done else "○",
            width=26, height=22,
            fg_color="transparent",
            hover_color=theme.GREEN_DIM,
            text_color=theme.TEXT_DIM if done else theme.GREEN_PRIMARY,
            font=ctk.CTkFont(size=12),
            corner_radius=4,
            command=on_toggle,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            row,
            text=task.get("text", ""),
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=theme.TEXT_DIMMER if done else theme.TEXT,
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            row,
            text="✕",
            width=22, height=22,
            fg_color="transparent",
            hover_color=theme.RED_HOVER,
            text_color=theme.TEXT_DIMMER,
            font=ctk.CTkFont(size=10),
            corner_radius=3,
            command=on_delete,
        ).pack(side="right")
