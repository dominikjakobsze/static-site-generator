from rich import print


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is missing")
        if not self.children:
            raise ValueError("children is missing")

        # zaimplementowac rekurencyjnie
        children_html = ""
        for child in self.children:
            if isinstance(child, HTMLNode):
                children_html += child.to_html()
        if not self.props:
            return f"<{self.tag}>{children_html}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}></{self.tag}>"


node = ParentNode(
    "div",
    [
        LeafNode("h1", "Heading!"),
        LeafNode("h2", "New York Times"),
        ParentNode(
            "span",
            [
                LeafNode("b", "grandchild")
            ]
        ),
        LeafNode("p", "Hello World")
    ]
)

print(node.to_html())
