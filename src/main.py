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
    # shutil.copytree(src, dst, dirs_exist_ok=True)
    for file in src.iterdir():
        if file.is_file():
            shutil.copy2(file, dst)
        if file.is_dir():
            (dst / file.name).resolve().mkdir(parents=True, exist_ok=True)
            _copy_file_to_dir(file, (dst / file.name).resolve())


def static_to_public():
    ROOT_DIR = Path(__file__).parent.parent.resolve()
    _delete_files_in_dir((ROOT_DIR / "public").resolve())
    _copy_file_to_dir((ROOT_DIR / "static").resolve(), (ROOT_DIR / "public").resolve())


main()
