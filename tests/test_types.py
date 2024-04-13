"""Test MustOpt types support."""

from queue import Queue
import unittest

from hamcrest import assert_that, equal_to

from mustopt import MustOpt


class TestMustOptTypes(unittest.TestCase):
    """Test MustOpt types support."""

    @staticmethod
    def test_none_type_works():
        """Test None value type is supported."""
        assert_that(MustOpt.new(None).must(), equal_to(None))

    @staticmethod
    def test_bool_type_works():
        """Test bool value type is supported."""
        assert_that(MustOpt.new(True).must(), equal_to(True))  # noqa:FBT003

    @staticmethod
    def test_numeric_types_work():
        """Test numeric value types are supported."""
        for val in [
            1,
            1.0,
            1 + 2j,
            0b01,
            0o7,
            0xA,
        ]:
            assert_that(MustOpt.new(val).must(), equal_to(val))

    @staticmethod
    def test_string_types_work():
        """Test string value types are supported."""
        for val in [
            'test',
            r'test',
            b'test',
        ]:
            assert_that(MustOpt.new(val).must(), equal_to(val))

    @staticmethod
    def test_collections_work():
        """Test collection value types are supported."""
        for val in [[1, 2, 3, 4], (1, 2, 3, 4), {1, 2, 3, 4}, {1: 2, 3: 4}]:
            assert_that(MustOpt.new(val).must(), equal_to(val))

    @staticmethod
    def test_data_type_works():
        """Test non-primitive value type is supported."""
        q: Queue[int] = Queue()
        for i in range(10):
            q.put(i)
        assert_that(MustOpt.new(q).must(), equal_to(q))
