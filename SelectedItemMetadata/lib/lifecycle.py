# lib/lifecycle.py — add-in start/stop and the selection handler.

import adsk.core

from . import events, status
from .describe import describe


def start() -> None:
    ui = adsk.core.Application.get().userInterface
    events.register_selection_changed(ui, _on_selection_changed)


def stop() -> None:
    events.unregister_all()
    status.restore(adsk.core.Application.get().userInterface)


def _on_selection_changed(selections: list[adsk.core.Selection]) -> None:
    # Only a single selection is described. For several, Fusion's own readout
    # ('2 Edges | ...') stands alone.
    fragments = describe(selections[0].entity) if len(selections) == 1 else []
    status.show(adsk.core.Application.get().userInterface, fragments)
