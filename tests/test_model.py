"""Tests for mustopt.model."""

import unittest

from hamcrest import assert_that, calling, equal_to, raises

from mustopt import InvalidContainerError, MustOpt


class TestMustOpt(unittest.TestCase):
    """Tests for MustOpt."""

    @staticmethod
    def test_empty_new_is_invalid():
        """Test empty new() returns invalid container."""
        assert_that(not MustOpt.new().valid())

    @staticmethod
    def test_new_from_value_is_valid():
        """Test new() with value returns valid container."""
        assert_that(MustOpt.new(1).valid())

    @staticmethod
    def test_unset_makes_container_invalid():
        """Test unset() invalidates container."""
        val = MustOpt.new(1)
        val.unset()
        assert_that(not val.valid())

    @staticmethod
    def test_set_value_makes_container_valid():
        """Test set() with non-None value makes container valid."""
        val: MustOpt[int] = MustOpt.new()
        val.set(1)
        assert_that(val.valid())

    @staticmethod
    def test_set_none_makes_container_invalid():
        """Test set() with None value makes container invalid."""
        val: MustOpt[None] = MustOpt.new()
        val.set(None)
        assert_that(not val.valid())

    @staticmethod
    def test_must_from_valid_container_works():
        """Test must() for valid container works."""
        assert_that(MustOpt.new(1).must(), equal_to(1))

    @staticmethod
    def test_must_from_invalid_container_raises_exception():
        """Test must() for invalid container fails."""
        assert_that(calling(MustOpt.must).with_args(MustOpt.new()), raises(InvalidContainerError))
