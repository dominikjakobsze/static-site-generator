from enum import Enum
from typing import List
from rich import print

from src.htmlnode import ParentNode, LeafNode, HTMLNode
from src.inline_markdown import text_to_textnodes
from src.textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_blocks(markdown: str) -> List[str]:
    result_list: List[str] = []

    for line in markdown.split("\n\n"):
        if line.strip():
            result_list.append(line.strip())

    return result_list


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


# assume all leading and trailing whitespace were already stripped
def block_to_block_type(block: str) -> BlockType:
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # Multiline Code blocks must start with 3 backticks and a newline, then end with 3 backticks.
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    # Every line in a quote block must start with a ">" character.
    if all(line.startswith(">") for line in lines): return BlockType.QUOTE

    # Every line in an unordered list block must start with a "- " character.
    if all(line.startswith("- ") for line in lines): return BlockType.UNORDERED_LIST

    # Every line in an ordered list block must start with a number followed by a ". " character.
    # The number must start at 1 and increment by 1 for each line.
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, 1)): return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text: str) -> List[HTMLNode]:
    children: List[HTMLNode] = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    block_nodes: List[HTMLNode] = []
    for block in blocks:
        html_node = block_to_html_node(block)
        block_nodes.append(html_node)
    return ParentNode("div", block_nodes)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return heading_to_node(block)
    if block_type == BlockType.CODE:
        return code_to_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_node(block)
    return paragraph_to_node(block)


def paragraph_to_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_node(block: str) -> ParentNode:
    level = len(block) - len(block.lstrip("#"))
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block.strip("`")
    code_node = text_node_to_html_node(TextNode(text, TextType.CODE))
    return ParentNode("pre", [code_node])


def quote_to_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def unordered_list_to_node(block: str) -> ParentNode:
    items = block.split("\n")
    li_nodes: List[HTMLNode] = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ul", li_nodes)


def ordered_list_to_node(block: str) -> ParentNode:
    items = block.split("\n")
    li_nodes: List[HTMLNode] = []
    for item in items:
        text = item[item.find(". ") + 2:]
        children = text_to_children(text)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ol", li_nodes)
