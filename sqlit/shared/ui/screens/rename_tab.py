"""Rename dialog for the active query tab."""

from __future__ import annotations

from typing import Any

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Input, Static

from sqlit.shared.ui.widgets import Dialog


class RenameTabScreen(ModalScreen):
    """Modal input for renaming the active query tab."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel", priority=True),
        Binding("enter", "submit", "Save", show=False),
    ]

    CSS = """
    RenameTabScreen {
        align: center middle;
        background: transparent;
    }

    #rename-tab-dialog {
        width: 50;
        height: auto;
        max-height: 10;
    }

    #rename-tab-container {
        height: 3;
        border: solid $panel;
        background: $surface;
        padding: 0 1;
    }

    #rename-tab-container.focused {
        border: solid $primary;
    }

    #rename-tab-container Input {
        border: none;
        height: 1;
        padding: 0;
        background: $surface;
    }
    """

    def __init__(self, current_value: str = "") -> None:
        super().__init__()
        self._current_value = current_value

    def compose(self) -> ComposeResult:
        shortcuts: list[tuple[str, str]] = [("Save", "<enter>"), ("Cancel", "<esc>")]
        with Dialog(id="rename-tab-dialog", title="Rename Tab", shortcuts=shortcuts):
            yield Static("New tab name:", id="rename-tab-description")
            container = Container(id="rename-tab-container")
            with container:
                yield Input(value=self._current_value, id="rename-tab-input")

    def on_mount(self) -> None:
        inp = self.query_one("#rename-tab-input", Input)
        inp.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "rename-tab-input":
            self.dismiss(event.value)

    def on_descendant_focus(self, event: Any) -> None:
        try:
            self.query_one("#rename-tab-container").add_class("focused")
        except Exception:
            pass

    def on_descendant_blur(self, event: Any) -> None:
        try:
            self.query_one("#rename-tab-container").remove_class("focused")
        except Exception:
            pass

    def action_submit(self) -> None:
        self.dismiss(self.query_one("#rename-tab-input", Input).value)

    def action_cancel(self) -> None:
        self.dismiss(None)

    def check_action(self, action: str, parameters: tuple) -> bool | None:
        if self.app.screen is not self:
            return False
        return super().check_action(action, parameters)
