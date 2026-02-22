from typing import List, Dict, Optional
from rich import print


class HTMLNode:
    def __init__(
            self,
            tag: Optional[str] = None,
            value: Optional[str] = None,
            children: Optional[List["HTMLNode"]] = None,
            props: Optional[Dict[str, str]] = None,
    ):
        self.tag: Optional[str] = tag
        self.value: Optional[str] = value
        self.children: Optional[List["HTMLNode"]] = children
        self.props: Optional[Dict[str, str]] = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if not self.props or self.props is None:
            return ""

        result_list = []
        for prop in self.props:
            result_list.append(f"{prop}=\"{self.props[prop]}\"")

        return " ".join(result_list)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
#
#
# obj = HTMLNode("p", "Lorem ipsum et dolore lis", [HTMLNode("a"), HTMLNode("i")], {
#     "href": "https://www.google.com",
#     "target": "_blank",
# })
#
# print(obj)
