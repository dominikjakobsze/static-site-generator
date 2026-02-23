from typing import Optional, Dict
from rich import print

from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
            self,
            value: str,
            tag: Optional[str] = None,
            props: Optional[Dict[str, str]] = None
    ):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError()
        if not self.tag:
            return self.value

        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"
