import unittest
from rich import print

from leafnode import LeafNode


class MyTestCase(unittest.TestCase):
    def test_to_html_with_p_tag(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_div_tag(self):
        node = LeafNode(tag="div", value="Hello, world!")
        self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

    def test_to_html_without_tag_returns_raw_value(self):
        node = LeafNode("String without tag")
        self.assertEqual(node.to_html(), "String without tag")

    def test_to_html_with_none_value_raises_value_error(self):
        node = LeafNode(None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_props(self):
        node = LeafNode(tag="div", value="Hello My Name is Dominik", props={"class": "bg-red-500 text-lg"})
        self.assertEqual(node.to_html(), "<div class=\"bg-red-500 text-lg\">Hello My Name is Dominik</div>")


if __name__ == '__main__':
    unittest.main()
