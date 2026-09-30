# lib/traits/component.py — the component an entity lives in, when that is not
# the root component.
#
# The root component is named after the document ('(Unsaved)' until it is
# saved), which tells the user nothing, so it is left out.

import adsk.core


def is_in_subcomponent(entity: adsk.core.Base) -> bool:
    component = entity.parentComponent
    return component != component.parentDesign.rootComponent


def owner(entity: adsk.core.Base) -> str:
    return f"in component '{entity.parentComponent.name}'"
