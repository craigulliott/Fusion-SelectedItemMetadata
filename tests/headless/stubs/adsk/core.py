"""Stub of adsk.core — see the package docstring."""


class Base:
    """Root of the Fusion object hierarchy. Fakes subclass it."""


class UserInterface(Base):
    pass


class Application(Base):
    # Every message the add-in logs, so a test can assert a failure was reported.
    logged: list[str] = []

    @staticmethod
    def log(message: str) -> None:
        Application.logged.append(message)
