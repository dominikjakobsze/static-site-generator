import unittest

from block_markdown import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    # HEADING TESTS
    def test_heading_valid_h1(self):
        result = block_to_block_type("# This is a heading")
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_valid_h6(self):
        result = block_to_block_type("###### This is a level 6 heading")
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_invalid_no_space(self):
        result = block_to_block_type("#This is not a heading (missing space)")
        self.assertEqual(result, BlockType.PARAGRAPH)

    # CODE TESTS
    def test_code_valid(self):
        result = block_to_block_type("```\n<p>Hello World</p>\n```")
        self.assertEqual(result, BlockType.CODE)

    def test_code_invalid_closing(self):
        result = block_to_block_type("```\nMissing third backtick\n``")
        self.assertEqual(result, BlockType.PARAGRAPH)

    # QUOTE TESTS
    def test_quote_valid_multiline(self):
        result = block_to_block_type(">First line\n>Second line\n>Third line")
        self.assertEqual(result, BlockType.QUOTE)

    def test_quote_invalid_missing_prefix(self):
        result = block_to_block_type(">First line\nMissing prefix\n>Third line")
        self.assertEqual(result, BlockType.PARAGRAPH)

    # UNORDERED LIST TESTS
    def test_unordered_list_valid(self):
        result = block_to_block_type("- Item 1\n- Item 2\n- Item 3")
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid_missing_dash(self):
        result = block_to_block_type("- Item 1\nItem 2 without dash\n- Item 3")
        self.assertEqual(result, BlockType.PARAGRAPH)

    # ORDERED LIST TESTS
    def test_ordered_list_valid(self):
        result = block_to_block_type("1. First item\n2. Second item\n3. Third item")
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_sequence(self):
        result = block_to_block_type("1. First item\n3. Wrong number\n2. Out of order")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_ordered_list_invalid_start_number(self):
        result = block_to_block_type("2. Should start with 1\n3. Next item")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_ordered_list_invalid_missing_dot(self):
        result = block_to_block_type("1. Item 1\n2 Item 2 (no dot)\n3. Item 3")
        self.assertEqual(result, BlockType.PARAGRAPH)

    # PARAGRAPH TESTS
    def test_paragraph_simple(self):
        result = block_to_block_type("This is just a simple paragraph of text.")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_almost_heading(self):
        result = block_to_block_type("####### Too many hashes")
        self.assertEqual(result, BlockType.PARAGRAPH)


if __name__ == '__main__':
    unittest.main()
