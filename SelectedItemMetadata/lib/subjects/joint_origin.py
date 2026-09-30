# lib/subjects/joint_origin.py — what a joint origin is: its name.

import adsk.fusion


def identity(origin: adsk.fusion.JointOrigin) -> str:
    return f"Joint origin '{origin.name}'"
