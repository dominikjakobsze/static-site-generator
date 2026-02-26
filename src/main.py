from textwrap import fill

from src.textnode import TextNode, TextType
from pathlib import Path
from rich import print
import shutil


def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    static_to_public()


def _delete_files_in_dir(target: Path):
    if target.exists():
        shutil.rmtree(target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)


def _copy_file_to_dir(src: Path, dst: Path):
    shutil.copytree(src, dst, dirs_exist_ok=True)


def static_to_public():
    ROOT_DIR = Path(__file__).parent.parent.resolve()
    _delete_files_in_dir((ROOT_DIR / "public").resolve())
    _copy_file_to_dir((ROOT_DIR / "static").resolve(), (ROOT_DIR / "public").resolve())


# Write a recursive function that copies all the contents from a source directory to a destination directory (in our case, static to public)
# It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
# It should copy all files and subdirectories, nested files, etc.
# I recommend logging the path of each file you copy, so you can see what's happening as you run and debug your code.

main()
