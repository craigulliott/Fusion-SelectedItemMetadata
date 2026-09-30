# lib/status.py — owns Fusion's status line, the readout in the lower right of
# the view.
#
# Two facts verified in Fusion (see CLAUDE.md) make this work:
# reading ui.statusMessage returns Fusion's own selection readout
# ('1 Edge | Length : 30.00 mm'), and Fusion has already written it by the time
# activeSelectionChanged fires. So one handler can read the readout and write
# readout + our text.

import adsk.core

# The separator Fusion uses inside its own readout, so our text reads as part of it.
SEPARATOR = " | "

# The readout our last message was built on, and that message. While the status
# line still shows _written, Fusion has not written since we did: the line holds
# our text, not a readout, and the readout is still _readout.
_readout = ""
_written: str | None = None


def show(ui: adsk.core.UserInterface, fragments: list[str]) -> None:
    """Show Fusion's current readout followed by fragments.

    With no fragments this puts the bare readout back, which also clears our
    text from a previous selection. The line is only written when it changes,
    so a selection with nothing to add leaves Fusion's readout untouched.
    """
    global _readout, _written
    current = ui.statusMessage
    if current != _written:
        _readout = current
    message = SEPARATOR.join(part for part in (_readout, *fragments) if part)
    if message != current:
        ui.statusMessage = message
    _written = message


def restore(ui: adsk.core.UserInterface) -> None:
    """Put Fusion's readout back if our text is still showing, and forget both.

    Fusion keeps the module loaded across stop and run, so the state has to be
    reset here or the next run would start from this run's text.
    """
    global _readout, _written
    if ui.statusMessage == _written:
        ui.statusMessage = _readout
    _readout, _written = "", None
