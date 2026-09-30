"""Minimal stand-in for the Fusion `adsk` package.

Only exists so SelectedItemMetadata/lib can be imported outside Fusion and its
logic unit-tested. It implements what the tested modules touch — the classes
they use in isinstance checks and annotations, and Application.log — and
nothing else. It is NOT a simulation of Fusion: behaviour of real Fusion
objects still has to be checked in Fusion.

Never shipped: this lives under tests/ and is not part of the add-in.
"""

from . import core, fusion  # noqa: F401  (imported for `import adsk.core` to work)
