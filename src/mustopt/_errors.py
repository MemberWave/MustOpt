class TypeNotSetError(TypeError):
    """Generic type not provided."""

    def __init__(self):
        super().__init__('Generic type not provided')


class InvalidContainerError(RuntimeError):
    """Value is tried to be got from an invalid container."""

    def __init__(self):
        super().__init__('Value is tried to be got from an invalid container')


class InvalidValueTypeError(TypeError):
    """Value type does not match the underlying type of container."""

    def __init__(self):
        super().__init__('Value type does not match the underlying type of container')


class ValueNotSetError(RuntimeError):
    """Underlying value is not set.

    This error should not appear without intervention to MustOpt internals.
    """

    def __init__(self):
        super().__init__('Underlying value is not set')
