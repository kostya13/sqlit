"""Query tab pane: one editor + one results area, mounted per query tab."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.lazy import Lazy
from textual.widgets import TabPane

from sqlit.shared.ui.widgets import (
    AutocompleteDropdown,
    InlineValueView,
    QueryTextArea,
    ResultsFilterInput,
    SqlitDataTable,
)
from sqlit.shared.ui.widgets_stacked_results import StackedResultsContainer


class QueryTabPane(TabPane):
    """A single query tab: SQL editor plus its own results area.

    One `QueryTabPane` is one tab inside `TabbedContent#query-tabs`. The
    widget IDs inside the pane (`query-input`, `results-area`, ...) are
    pane-local: with multiple tabs they repeat across panes, so callers must
    resolve widgets through the *active* pane, never with an app-wide
    `query_one("#query-input")`.
    """

    DEFAULT_CSS = """
    QueryTabPane {
        height: 1fr;
    }
    """

    def __init__(self, title: object = "query", **kwargs: object) -> None:
        super().__init__(title, **kwargs)  # type: ignore[arg-type]
        # Semantic tab name without the "[N]" position prefix; the label is
        # rebuilt by the app as "[N] <base>".
        self.title_base: str = str(title)

    def compose(self) -> ComposeResult:
        with Vertical(id="query-area"):
            yield QueryTextArea(
                "",
                language="sql",
                theme="css",
                id="query-input",
                read_only=True,
            )
            yield Lazy(AutocompleteDropdown(id="autocomplete-dropdown"))

        with Container(id="results-area"):
            yield ResultsFilterInput(id="results-filter")
            yield Lazy(SqlitDataTable(id="results-table", zebra_stripes=True, show_header=False))
            yield StackedResultsContainer(id="stacked-results")
            yield InlineValueView(id="value-view")
