# lib/events.py — GC-safe event handler registry (ConstraintLens landmine M-7).

import adsk.core

from . import errors

# Every event <-> handler pair lives here for the lifetime of the add-in. Fusion
# keeps only a C++ pointer to a handler, so once Python collects it, the next
# callback crashes Fusion silently.
_subscriptions: list[tuple[object, adsk.core.EventHandler]] = []


class _ActiveSelectionChangedHandler(adsk.core.ActiveSelectionEventHandler):
    def __init__(self, on_change):
        super().__init__()
        self._on_change = on_change

    def notify(self, args):
        try:
            self._on_change(args.currentSelection)
        except Exception:
            # An exception escaping into Fusion can deactivate the add-in.
            errors.report("activeSelectionChanged")


def pin(event, handler: adsk.core.EventHandler) -> None:
    """Attach a handler to a Fusion event and keep it alive (M-7)."""
    event.add(handler)
    _subscriptions.append((event, handler))


def register_selection_changed(ui: adsk.core.UserInterface, on_change) -> None:
    pin(ui.activeSelectionChanged, _ActiveSelectionChangedHandler(on_change))


def unregister_all() -> None:
    for event, handler in _subscriptions:
        try:
            event.remove(handler)
        except Exception:
            pass
    _subscriptions.clear()
