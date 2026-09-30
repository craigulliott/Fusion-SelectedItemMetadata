"""Fake Fusion objects, shaped like the ones the add-in reads.

Deliberately dumb: attributes only. The one behaviour they copy from Fusion is
referencedEntity raising where Fusion raises, because the projection trait
has to survive it.
"""

import _bootstrap  # noqa: F401  (sys.path side effect)

import adsk.fusion


class FakeSketch:
    def __init__(self, name):
        self.name = name


class _FakeSketchEntity:
    """A sketch entity; `source` is what it was projected from.

    Fusion's referencedEntity raises instead of returning None both for an
    entity that is not a reference and for one it cannot resolve, such as the
    endpoints it adds along with a projected curve. unresolvable=True is the
    second case.
    """

    def __init__(self, sketch, source=None, unresolvable=False):
        self.parentSketch = sketch
        self.isReference = source is not None or unresolvable
        self._source = source

    @property
    def referencedEntity(self):
        if self._source is None:
            raise RuntimeError("2 : InternalValidationError : res")
        return self._source


class FakeSketchPoint(_FakeSketchEntity, adsk.fusion.SketchPoint):
    pass


class FakeSketchLine(_FakeSketchEntity, adsk.fusion.SketchLine):
    pass


class FakeDesign:
    def __init__(self, name="(Unsaved)"):
        # Fusion names the root component after the document.
        self.rootComponent = FakeComponent(name, self)


class FakeComponent:
    def __init__(self, name, design):
        self.name = name
        self.parentDesign = design


class FakeJointOrigin(adsk.fusion.JointOrigin):
    def __init__(self, name, component):
        self.name = name
        self.parentComponent = component


class FakeUI:
    """The status line, counting writes so a test can assert there were none."""

    def __init__(self, status_message=""):
        self._status_message = status_message
        self.writes = 0

    @property
    def statusMessage(self):
        return self._status_message

    @statusMessage.setter
    def statusMessage(self, value):
        self._status_message = value
        self.writes += 1
