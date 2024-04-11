"""MustOpt model."""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar('T')


class MustOpt(Generic[T]):
    """MustOpt provides robust container for handling of an optional value."""

    def __init__(self):
        self._value: T | None = None
        self._valid: bool = False

    @staticmethod
    def new(value: T | None = None) -> MustOpt[T]:
        """Create new container."""
        res: MustOpt[T] = MustOpt()
        res.set(value)
        return res

    def valid(self) -> bool:
        """Check whether the container is valid and value could be taken."""
        return self._valid

    def must(self) -> T | None:
        """Get value from container if it's valid.

        Otherwise, raises a ValueIsNotValidError.
        """
        if not self._valid:
            raise InvalidContainerError

        return self._value

    def set(self, value: T | None) -> None:
        """Set new value for container.

        Makes it valid if value is not None.
        """
        self._value = value
        self._valid = self._value is not None

    def unset(self) -> None:
        """Invalidate container."""
        self._value = None
        self._valid = False


class InvalidContainerError(RuntimeError):
    """Value is tried to be got from an invalid container."""

    def __init__(self):
        super().__init__('Value is tried to be got from an invalid container')
