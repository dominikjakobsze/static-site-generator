from enum import Enum
from typing import List


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
