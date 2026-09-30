# lib/errors.py — makes failures visible without interrupting the user.

import traceback

import adsk.core


def report(context: str) -> None:
    """Write the exception being handled to Fusion's TEXT COMMANDS window.

    Used instead of a message box because it runs on every selection change,
    where a dialog would make Fusion unusable. Never raises: it is called from
    inside event handlers.
    """
    try:
        adsk.core.Application.log(f"SelectedItemMetadata — {context} failed:\n{traceback.format_exc()}")
    except Exception:
        pass
