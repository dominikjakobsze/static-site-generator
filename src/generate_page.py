from pathlib import Path

from src.block_markdown import markdown_to_blocks, markdown_to_html_node
from rich import print


def extract_title(markdown: str) -> None | str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.lstrip("#").strip()
    raise ValueError("No <h1> tag!")


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_content = from_path.read_text()
    template_content = template_path.read_text()

    html_output = markdown_to_html_node(markdown_content).to_html()
    website_title = extract_title(markdown_content)

    modified_template = template_content.replace("{{ Content }}", html_output).replace("{{ Title }}", website_title)

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    dest_path.write_text(modified_template)


def generate_pages_recursive(dir_path_content: Path, template_path: Path, dest_dir_path: Path):
    for entry in dir_path_content.iterdir():
        if entry.is_dir():
            generate_pages_recursive(
                entry,
                template_path,
                dest_dir_path / entry.name
            )
        elif entry.name.endswith(".md"):
            output_file_path = dest_dir_path / f"{entry.stem}.html"
            generate_page(
                entry,
                template_path,
                output_file_path
            )
