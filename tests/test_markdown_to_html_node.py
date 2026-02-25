import unittest

from src.block_markdown import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_markdown_to_html_node_full_example(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

#### Dominik

```
coding block
```

> Dominik1 **jest**
> Dominik2
> Dominik3

- Dominik1 **jest**
- Dominik2
- Dominik3

1. Pierwszy element
2. Drugi element z **pogrubieniem**
3. Trzeci element

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        # Sprawdzamy czy kluczowe elementy znajdują się w wygenerowanym HTML
        self.assertIn("<div>", html)
        self.assertIn("<p>This is <b>bolded</b> paragraph text in a p tag here</p>", html)
        self.assertIn("<h4>Dominik</h4>", html)
        self.assertIn("<pre><code>\ncoding block\n</code></pre>", html)
        self.assertIn("<blockquote>Dominik1 <b>jest</b> Dominik2 Dominik3</blockquote>", html)
        self.assertIn("<ul><li>Dominik1 <b>jest</b></li><li>Dominik2</li><li>Dominik3</li></ul>", html)
        self.assertIn("<ol><li>Pierwszy element</li><li>Drugi element z <b>pogrubieniem</b></li><li>Trzeci element</li></ol>", html)
        self.assertIn("<p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p>", html)

    def test_paragraph(self):
        md = "To jest zwykły paragraf z **pogrubieniem**."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>To jest zwykły paragraf z <b>pogrubieniem</b>.</p></div>"
        )

    def test_headings(self):
        md = """
# Nagłówek 1

### Nagłówek 3

###### Nagłówek 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Nagłówek 1</h1><h3>Nagłówek 3</h3><h6>Nagłówek 6</h6></div>"
        )

    def test_quote(self):
        md = """
> To jest cytat
> w wielu liniach
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>To jest cytat w wielu liniach</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- Pierwszy
- Drugi z **boldem**
- Trzeci
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Pierwszy</li><li>Drugi z <b>boldem</b></li><li>Trzeci</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. Pierwszy
2. Drugi
3. Trzeci
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Pierwszy</li><li>Drugi</li><li>Trzeci</li></ol></div>"
        )


if __name__ == '__main__':
    unittest.main()
