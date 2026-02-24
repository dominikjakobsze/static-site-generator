import unittest

from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_multiple_bold(self):
        nodes = text_to_textnodes(
            "This is **bold** and **another bold**"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another bold", TextType.BOLD),
            ],
            nodes,
        )

    def test_text_to_textnodes_italic_and_code(self):
        nodes = text_to_textnodes(
            "Some _italic_ and `some code` here"
        )
        self.assertListEqual(
            [
                TextNode("Some ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("some code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_plain(self):
        nodes = text_to_textnodes(
            "This is just plain text"
        )
        self.assertListEqual(
            [
                TextNode("This is just plain text", TextType.TEXT),
            ],
            nodes,
        )

    def test_text_to_textnodes_mixed(self):
        nodes = text_to_textnodes(
            "![image](url) [link](url) **bold** _italic_ `code`"
        )
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "url"),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            nodes,
        )


if __name__ == '__main__':
    unittest.main()
