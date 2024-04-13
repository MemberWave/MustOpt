import types
from typing import ClassVar


class GenericTAccessMeta(type):
    """A hack metaclass to get access to the underlying type of generic T.

    Solution is taken from https://stackoverflow.com/a/75395800
    """

    __concrete__: ClassVar = {}

    def __getitem__(cls, key_t: type) -> type:
        cache = cls.__concrete__

        c = cache.get(key_t, None)
        if c is not None:
            return c

        cache[key_t] = c = types.new_class(
            f'{cls.__name__}[{key_t.__name__}]',
            (cls,),
            {},
            lambda ns: ns.update(_t=key_t),
        )

        return c
