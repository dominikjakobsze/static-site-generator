import shutil
from pathlib import Path
from rich import print
from typing import Dict, Any

from src.generate_page import generate_page, generate_pages_recursive


def _recreate_directory(target_dir: Path) -> None:
    """
    Deletes a directory and all its contents if it exists,
    then recreates it as an empty directory.
    """
    # print(f"Recreating directory: {target_dir}")
    if target_dir.exists():
        shutil.rmtree(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)


def _copy_recursive(source: Path, destination: Path) -> None:
    """
    Recursively copies contents from a source to a destination directory.
    """
    # shutil.copytree(source, destination, dirs_exist_ok=True)
    for item in source.iterdir():
        destination_item = destination / item.name
        if item.is_file():
            # print(f"  - Copying file: {item} -> {destination_item}")
            shutil.copy2(item, destination_item)
        elif item.is_dir():
            destination_item.mkdir(parents=True, exist_ok=True)
            _copy_recursive(item, destination_item)


def sync_static_to_public() -> None:
    """
    Coordinates the process of syncing the 'static' directory to the 'public' directory.
    """
    root_dir = Path(__file__).parent.parent.resolve()
    static_dir = root_dir / "static"
    public_dir = root_dir / "public"

    _recreate_directory(public_dir)
    _copy_recursive(static_dir, public_dir)


def main(config: Dict[str, Any] = None) -> None:
    """
    Main entry point for the script.
    """
    sync_static_to_public()
    root_dir = (Path(__file__).parent.parent).resolve()
    generate_pages_recursive(root_dir / "content", root_dir / "template.html", root_dir / "public")


if __name__ == "__main__":
    main()
