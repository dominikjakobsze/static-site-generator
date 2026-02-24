from typing import List

from rich import print


def markdown_to_blocks(markdown: str):
    result_list: List[str] = []

    for line in markdown.split("\n\n"):
        if line.strip():
            result_list.append(line.strip())

    return result_list
