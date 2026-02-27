import unittest
from rich import print

from src.generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_h1_simple(self):
        md = """
# New York Times
"""
        self.assertEqual(extract_title(md), "New York Times")

    def test_extract_h1_between_blocks(self):
        md = """
> Test1
> Test2
> Test 3

# New York Times

- Hello
"""
        self.assertEqual(extract_title(md), "New York Times")

    def test_extract_h1_with_other_headers(self):
        md = """
### Fake New York Times

# New York Times

- Hello
"""
        self.assertEqual(extract_title(md), "New York Times")

    def test_no_h1_raises_exception(self):
        md = """
### Fake New York Times

## New York Times

- Hello
"""
        with self.assertRaises(ValueError):
            extract_title(md)


if __name__ == '__main__':
    unittest.main()
