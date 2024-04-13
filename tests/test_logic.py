"""Test MustOpt logic."""

import unittest

from hamcrest import assert_that, calling, equal_to, raises

from mustopt import InvalidContainerError, InvalidValueTypeError, MustOpt, TypeNotSetError, ValueNotSetError


class TestMustOptLogic(unittest.TestCase):
    """Test MustOpt logic."""

    @staticmethod
    def test_not_providing_generic_type_raises_exception():
        """Test not providing generic type raises TypeNotSetError."""
        assert_that(calling(MustOpt).with_args(), raises(TypeNotSetError))

    @staticmethod
    def test_constructor_returns_invalid_container():
        """Test MustOpt() returns invalid container."""
        assert_that(not MustOpt[int]().valid())

    @staticmethod
    def test_new_returns_valid_container():
        """Test new() returns valid container."""
        assert_that(MustOpt.new(1).valid())

    @staticmethod
    def test_unset_makes_container_invalid():
        """Test unset() invalidates container."""
        val = MustOpt.new(1)
        assert_that(val.valid())
        val.unset()
        assert_that(not val.valid())

    @staticmethod
    def test_set_makes_container_valid():
        """Test set() makes container valid."""
        val: MustOpt[int] = MustOpt[int]()
        assert_that(not val.valid())
        val.set(1)
        assert_that(val.valid())

    @staticmethod
    def test_set_with_different_type_raises_exception():
        """Test set() with value of different type raises InvalidValueTypeError."""
        assert_that(calling(MustOpt.set).with_args(MustOpt[int](), 'test'), raises(InvalidValueTypeError))

    @staticmethod
    def test_valid_container_must_works():
        """Test must() for valid container works."""
        assert_that(MustOpt.new(1).must(), equal_to(1))

    @staticmethod
    def test_invalid_container_must_raises_exception():
        """Test must() for invalid container raises InvalidContainerError."""
        assert_that(calling(MustOpt.must).with_args(MustOpt[int]()), raises(InvalidContainerError))

    @staticmethod
    def test_must_with_no_value_raises_exception():
        """Test must() for broken container raises ValueNotSetError."""
        val: MustOpt[int] = MustOpt[int]()
        assert_that(not val.valid())
        val._valid = True  # noqa: SLF001
        assert_that(val.valid())
        assert_that(calling(MustOpt.must).with_args(val), raises(ValueNotSetError))

    @staticmethod
    def test_eq_dunder_works():
        """Test __eq__ dunder works."""
        assert_that(MustOpt.new(1) != 1)
        assert_that(MustOpt[int]() == MustOpt[int]())
        assert_that(MustOpt.new(1) != MustOpt[int]())
        assert_that(MustOpt.new(1) != MustOpt.new('a'))
        assert_that(MustOpt.new(1) == MustOpt.new(1))
        assert_that(MustOpt.new(1) != MustOpt.new(2))

    @staticmethod
    def test_hash_dunder_works():
        """Test __hash__ dunder works."""
        for m in [
            MustOpt[int](),
            MustOpt.new(None),
            MustOpt.new(True),  # noqa: FBT003
            MustOpt.new(1),
            MustOpt.new(1.0),
            MustOpt.new('a'),
        ]:
            assert_that(isinstance(hash(m), int))
