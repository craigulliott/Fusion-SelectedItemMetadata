# lib/describe.py — turns one selected entity into the text shown after
# Fusion's readout.
#
# Two tables, because there are two kinds of fact:
#
#   SUBJECTS  what the entity is. At most one applies: the entry for the most
#             specific class in the entity's class chain. Most types need none,
#             because Fusion's readout already names them ('1 Sketch Point').
#   TRAITS    what is true about it. Every trait whose class matches and whose
#             condition holds adds its text, in table order. Traits cut across
#             types (projection applies to every kind of sketch entity; the
#             owning component to types that share no class but Base), which is
#             why they are separate from subjects.
#
# To add a fact: write its function(s) in subjects/ or traits/, then add one
# line to a table below. To have one trait replace another rather than add to
# it, give the two conditions that cannot both hold.

from collections.abc import Callable
from dataclasses import dataclass

import adsk.core
import adsk.fusion

from . import errors
from .subjects import joint_origin
from .traits import component, projection

Text = Callable[[adsk.core.Base], str]
Condition = Callable[[adsk.core.Base], bool]


@dataclass(frozen=True)
class Trait:
    applies_to: type | tuple[type, ...]   # matched with isinstance, so subclasses count
    when: Condition
    text: Text


SUBJECTS: dict[type, Text] = {
    adsk.fusion.JointOrigin: joint_origin.identity,
}

TRAITS: list[Trait] = [
    Trait(adsk.fusion.SketchEntity, projection.is_from_sketch, projection.source_sketch),
    Trait(adsk.fusion.JointOrigin, component.is_in_subcomponent, component.owner),
]


def describe(entity: adsk.core.Base) -> list[str]:
    """The text fragments for one selected entity: its subject, then its traits."""
    subject = _subject_of(entity)
    parts = [] if subject is None else [subject]
    parts += [trait.text for trait in TRAITS if _applies(trait, entity)]
    return [text for text in (_guarded(part, entity) for part in parts) if text]


def _subject_of(entity: adsk.core.Base) -> Text | None:
    """The subject registered for the most specific class the entity is."""
    for cls in type(entity).__mro__:
        if cls in SUBJECTS:
            return SUBJECTS[cls]
    return None


def _applies(trait: Trait, entity: adsk.core.Base) -> bool:
    return isinstance(entity, trait.applies_to) and bool(_guarded(trait.when, entity))


def _guarded(part: Text | Condition, entity: adsk.core.Base):
    """Call one subject, trait text or condition. A failure is reported and
    costs only that part: every other fragment is still shown."""
    try:
        return part(entity)
    except Exception:
        errors.report(f"{part.__module__}.{part.__name__}")
        return None
