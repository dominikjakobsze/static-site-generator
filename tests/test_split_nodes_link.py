import unittest

from src.inline_markdown import split_nodes_link
from src.textnode import TextNode, TextType


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_split_links_at_start(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_split_links_at_start_and_trailing(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) visist me!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" visist me!", TextType.TEXT),
            ],
        )

    def test_image_skipped_at_start(self):
        node = TextNode(
            "![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) visist me!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("![to boot dev](https://www.boot.dev) and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" visist me!", TextType.TEXT),
            ],
        )

    def test_image_skipped_in_middle(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) visist me!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ![to youtube](https://www.youtube.com/@bootdotdev) visist me!", TextType.TEXT),
            ],
        )

    def test_only_images_skipped(self):
        node = TextNode(
            "![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) visist me!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) visist me!",
                    TextType.TEXT,
                ),
            ],
        )

    def test_no_links_no_images(self):
        node = TextNode(
            "and visist me!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("and visist me!", TextType.TEXT),
            ],
        )

    def test_split_links_with_trailing_text(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) visit me",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" visit me", TextType.TEXT),
            ],
        )

    def test_split_links_with_image_mixed(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) visit me",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ![to boot dev](https://www.boot.dev) and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" visit me", TextType.TEXT),
            ],
        )

    def test_text_only(self):
        node = TextNode(
            "Hello World",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Hello World", TextType.TEXT),
            ],
        )

    def test_empty_string(self):
        node = TextNode(
            "",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),
            ],
        )

    def test_empty_list(self):
        new_nodes = split_nodes_link([])
        self.assertEqual(new_nodes, [])

    def test_single_link_only(self):
        node = TextNode(
            "[to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_link_followed_by_identical_image(self):
        node = TextNode(
            "[to youtube](https://www.youtube.com/@bootdotdev) ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" ![to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
            ],
        )

    def test_link_concatenated_with_text(self):
        node = TextNode(
            "concat[to youtube](https://www.youtube.com/@bootdotdev)concat",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("concat", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode("concat", TextType.TEXT),
            ],
        )

    def test_multiple_nodes_split(self):
        node = TextNode(
            "Before [to youtube](https://www.youtube.com/@bootdotdev) After",
            TextType.TEXT,
        )
        node2 = TextNode("bolder!", TextType.BOLD)
        new_nodes = split_nodes_link([node, node2])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" After", TextType.TEXT),
                TextNode("bolder!", TextType.BOLD),
            ],
        )

    def test_multiple_nodes_reverse_order(self):
        node = TextNode(
            "Before [to youtube](https://www.youtube.com/@bootdotdev) After",
            TextType.TEXT,
        )
        node2 = TextNode("bolder!", TextType.BOLD)
        new_nodes = split_nodes_link([node2, node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("bolder!", TextType.BOLD),
                TextNode("Before ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" After", TextType.TEXT),
            ],
        )

    def test_multiple_nodes_surrounded(self):
        node = TextNode(
            "Before [to youtube](https://www.youtube.com/@bootdotdev) After",
            TextType.TEXT,
        )
        node2 = TextNode("bolder!", TextType.BOLD)
        new_nodes = split_nodes_link([node2, node, node2])
        self.assertEqual(
            new_nodes,
            [
                TextNode("bolder!", TextType.BOLD),
                TextNode("Before ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" After", TextType.TEXT),
                TextNode("bolder!", TextType.BOLD),
            ],
        )


if __name__ == '__main__':
    unittest.main()
