from enum import Enum
from typing import List

from rich import print


def markdown_to_blocks(markdown: str):
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


def detect_complex_block_type(block: str, block_char: str, block_type: BlockType):
    for line in block.split("\n"):
        if not line.startswith(block_char):
            return BlockType.PARAGRAPH
    return block_type


def _is_ordered_list_block(block: str) -> bool:
    i = 1
    for line in block.split("\n"):
        if not line.startswith(f"{i}. "):
            return False
        i += 1
    return True


# assume all leading and trailing whitespace were already stripped
def block_to_block_type(block: str):
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    # Multiline Code blocks must start with 3 backticks and a newline, then end with 3 backticks.
    # Every line in a quote block must start with a "greater-than" character: > followed by the quote text. A space after > is allowed but not required.
    # Every line in an unordered list block must start with a - character, followed by a space.
    # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    # If none of the above conditions are met, the block is a normal paragraph.
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")): return BlockType.HEADING

    if block.startswith(("```\n")) and block.endswith(("```")): return BlockType.CODE

    if block.startswith(">"): return detect_complex_block_type(block, ">", BlockType.QUOTE)
    if block.startswith("- "): return detect_complex_block_type(block, "- ", BlockType.UNORDERED_LIST)

    if _is_ordered_list_block(block): return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
