import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_simple(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks,
        )

    def test_markdown_to_blocks_extra_newlines(self):
        md = """
Block 1



Block 2
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(["Block 1", "Block 2"], blocks)

    def test_markdown_to_blocks_with_whitespace(self):
        md = "  \n\n  block 1 \n\n block 2 \n\n  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(["block 1", "block 2"], blocks)


if __name__ == "__main__":
    unittest.main()
