# SelectedItemMetadata — Fusion add-in entry point.
#
# Owns only run(context) / stop(context). All logic lives under ./lib.
#
# The import is relative, unlike ConstraintLens's sys.path insert followed by
# `from lib import ...`. Every add-in runs in the same Python interpreter, so a
# second top-level package named `lib` would resolve to whichever add-in loaded
# first. Fusion loads the add-in folder as a package, which is what makes the
# relative import work.

import traceback

import adsk.core

from .lib import lifecycle


def run(context):
    try:
        lifecycle.start()
    except Exception:
        ui = adsk.core.Application.get().userInterface
        if ui:
            ui.messageBox("SelectedItemMetadata failed to start:\n" + traceback.format_exc())


def stop(context):
    try:
        lifecycle.stop()
    except Exception:
        ui = adsk.core.Application.get().userInterface
        if ui:
            ui.messageBox("SelectedItemMetadata failed to stop cleanly:\n" + traceback.format_exc())
