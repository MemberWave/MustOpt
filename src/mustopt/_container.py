from __future__ import annotations

from typing import Generic, NoReturn, TypeVar

from mustopt._errors import InvalidContainerError, InvalidValueTypeError, TypeNotSetError, ValueNotSetError
from mustopt._meta import GenericTAccessMeta

T = TypeVar('T')

_VALUE_FIELD_NAME = '_value'


class MustOpt(Generic[T], metaclass=GenericTAccessMeta):
    """MustOpt provides robust container for handling of an optional value."""

    _t: type[T]

    def __init__(self):
        """:raise TypeNotSetError: if generic type not provided."""
        if not hasattr(self, '_t'):
            raise TypeNotSetError

        self._valid: bool = False

    @staticmethod
    def new(value: T) -> MustOpt[T]:
        """Create new container with specified value.

        Makes container valid no matter what value was set.

        :param value: a value to be stored in container.
        :return: a valid MustOpt container with set value.
        """
        res: MustOpt[T] = MustOpt[type(value)]()  # type: ignore[misc]
        res.set(value)
        return res

    def valid(self) -> bool:
        """Check whether container is valid and value could be taken.

        :return: whether container is valid.
        """
        return self._valid

    def must(self) -> T:
        """Get value from container if it's valid.

        :return: value stored in container.
        :raise InvalidContainerError: if it's not valid.
        """
        if not self._valid:
            raise InvalidContainerError

        if not hasattr(self, _VALUE_FIELD_NAME):
            raise ValueNotSetError

        return getattr(self, _VALUE_FIELD_NAME)

    # for some reason, mypy gives `Implicit return in function which does not return`
    def set(self, value: T) -> NoReturn:  # type: ignore[misc]
        """Set new value for container.

        Makes container valid no matter what value was set.

        :param value: value to be set.
        :raise InvalidValueTypeError: if value type does not match the type of container.
        """
        if not isinstance(value, self._t):
            raise InvalidValueTypeError

        setattr(self, _VALUE_FIELD_NAME, value)
        self._valid = True

    # for some reason, mypy gives `Implicit return in function which does not return`
    def unset(self) -> NoReturn:  # type: ignore[misc]
        """Invalidate container."""
        if hasattr(self, _VALUE_FIELD_NAME):
            delattr(self, _VALUE_FIELD_NAME)

        self._valid = False

    def __eq__(self, other: object) -> bool:
        # instances of different types are not equal
        if not isinstance(other, MustOpt):
            return False

        # invalid containers are equal
        if not self._valid and not other._valid:
            return True

        # valid and invalid containers are not equal
        if not self._valid or not other._valid:
            return False

        # containers of different types are not equal
        if self._t is not other._t:
            return False

        # valid containers are equal if stored values are equal
        return self.must() == other.must()

    def __hash__(self) -> int:
        sum_ = hash(self._t) + hash(self._valid)
        if hasattr(self, _VALUE_FIELD_NAME) and hasattr(getattr(self, _VALUE_FIELD_NAME), '__hash__'):
            sum_ += hash(getattr(self, _VALUE_FIELD_NAME))
        return hash(sum_)
