"""Root state definitions."""

from __future__ import annotations

from sqlit.core.input_context import InputContext
from sqlit.core.state_base import State


class RootState(State):
    """Root state - minimal actions available everywhere."""

    help_category = "General"
    keymap_context = "global"

    def _setup_actions(self) -> None:
        self.allows("quit", help="Quit")
        self.allows("show_help", help="Show this help")
        self.allows("leader_key", help="Commands menu")
        self.allows("new_query", key="f4", label="New tab", help="New query tab")
        self.allows("rename_query_tab", key="f5", label="Rename tab", help="Rename query tab")
        self.allows("previous_query_tab", key="f2", label="Prev tab", help="Previous query tab")
        self.allows("next_query_tab", key="f3", label="Next tab", help="Next query tab")
        self.allows("close_query_tab", key="f8", label="Close tab", help="Close query tab")
        self.allows(
            "cancel_operation",
            guard=lambda app: app.query_executing,
            key="escape",
            label="Cancel",
            help="Cancel query",
        )

    def is_active(self, app: InputContext) -> bool:
        return True
