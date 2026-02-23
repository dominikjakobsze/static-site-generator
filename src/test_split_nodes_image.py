import unittest

from inline_markdown import split_nodes_image
from textnode import TextNode, TextType


class TestSplitNodesImage(unittest.TestCase):
    def test_two_images_in_middle_of_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
        )

    def test_two_images_with_trailing_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) This is awesome",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" This is awesome", TextType.TEXT),
            ],
        )

    def test_two_images_with_leading_space(self):
        node = TextNode(
            " ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) This is awesome",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode(" ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" This is awesome", TextType.TEXT),
            ],
        )

    def test_two_images_at_start_of_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) This is awesome",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" This is awesome", TextType.TEXT),
            ],
        )

    def test_two_images_in_text_node_preceded_by_other_node(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) This is awesome",
            TextType.TEXT,
        )
        node2 = TextNode("bolding", "b", TextType.BOLD)
        new_nodes = split_nodes_image([node2, node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("bolding", "b", TextType.BOLD),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" This is awesome", TextType.TEXT),
            ],
        )

    def test_two_images_in_text_node_followed_by_other_node(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) This is awesome",
            TextType.TEXT,
        )
        node2 = TextNode("bolding", "b", TextType.BOLD)
        new_nodes = split_nodes_image([node, node2])
        self.assertEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" This is awesome", TextType.TEXT),
                TextNode("bolding", "b", TextType.BOLD),
            ],
        )

    def test_two_images_in_text_node_surrounded_by_other_nodes(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) This is awesome",
            TextType.TEXT,
        )
        node2 = TextNode("bolding", "b", TextType.BOLD)
        new_nodes = split_nodes_image([node2, node, node2])
        self.assertEqual(
            new_nodes,
            [
                TextNode("bolding", "b", TextType.BOLD),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" This is awesome", TextType.TEXT),
                TextNode("bolding", "b", TextType.BOLD),
            ],
        )

    def test_no_images(self):
        node = TextNode("This is text with no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with no images.", TextType.TEXT),
            ],
        )

    def test_single_image(self):
        node = TextNode("Text before ![image](https://i.imgur.com/zjjcJKZ.png) text after.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" text after.", TextType.TEXT),
            ],
        )

    def test_only_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_empty_nodes_list(self):
        new_nodes = split_nodes_image([])
        self.assertEqual(
            new_nodes,
            [],
        )


# python3 ścieżka/do/pliku_testowego.py TestSplitNodesImage.test_split_images - Odpala jeden test
if __name__ == '__main__':
    unittest.main()
