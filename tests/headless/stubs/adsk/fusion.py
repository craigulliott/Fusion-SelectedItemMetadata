"""Stub of adsk.fusion — see the package docstring.

The class chain matches Fusion's real one, which is what subject and trait
matching depend on.
"""

from .core import Base


class SketchEntity(Base):
    pass


class SketchPoint(SketchEntity):
    pass


class SketchCurve(SketchEntity):
    pass


class SketchLine(SketchCurve):
    pass


class JointOrigin(Base):
    pass


class BRepEdge(Base):
    pass
