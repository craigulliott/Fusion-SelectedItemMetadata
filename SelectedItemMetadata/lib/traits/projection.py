# lib/traits/projection.py — a sketch entity projected from another sketch.

import adsk.fusion


def is_from_sketch(entity: adsk.fusion.SketchEntity) -> bool:
    return entity.isReference and isinstance(_source(entity), adsk.fusion.SketchEntity)


def source_sketch(entity: adsk.fusion.SketchEntity) -> str:
    return f"projected from sketch '{_source(entity).parentSketch.name}'"


def _source(entity: adsk.fusion.SketchEntity):
    """The entity this one was projected from, or None when Fusion cannot say.

    referencedEntity raises (InternalValidationError) rather than returning
    None for the endpoints Fusion adds along with a projected curve, and for
    included, intersected and unlinked geometry. That is an answer, not a
    failure, so it is not reported.
    """
    try:
        return entity.referencedEntity
    except RuntimeError:
        return None
