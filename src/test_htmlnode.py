import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_raises_not_implemented_error(self):
        obj = HTMLNode()
        with self.assertRaises(NotImplementedError):
            obj.to_html()

    def test_props_to_html_with_none_props(self):
        obj = HTMLNode()
        self.assertEqual("", obj.props_to_html())

    def test_props_to_html_with_empty_props(self):
        obj = HTMLNode(props={})
        self.assertEqual("", obj.props_to_html())

    def test_repr_produces_correct_string(self):
        node = HTMLNode("div", "Hello World", [HTMLNode("span")], {"id": "main"})
        expected_repr = "HTMLNode(div, Hello World, children: [HTMLNode(span, None, children: None, None)], {'id': 'main'})"
        self.assertEqual(expected_repr, repr(node))


if __name__ == '__main__':
    unittest.main()
