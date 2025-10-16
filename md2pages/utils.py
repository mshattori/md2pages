"""File operation utilities for md2pages."""

from pathlib import Path
from typing import List
import fnmatch
import shutil


def find_markdown_files(input_dir: Path, exclude_patterns: List[str]) -> List[Path]:
    """
    Find all Markdown files recursively in input directory.

    Args:
        input_dir: Directory to search
        exclude_patterns: List of glob patterns to exclude (e.g., [".git/**", "drafts/**"])

    Returns:
        List of Path objects for all .md files that don't match exclude patterns
    """
    markdown_files = []

    for md_file in input_dir.rglob("*.md"):
        # Get relative path for pattern matching
        try:
            relative_path = md_file.relative_to(input_dir)
        except ValueError:
            # Skip if file is not under input_dir
            continue

        # Check if file matches any exclude pattern
        excluded = False
        for pattern in exclude_patterns:
            # Use forward slash for consistent matching across platforms
            relative_str = relative_path.as_posix()

            if fnmatch.fnmatch(relative_str, pattern):
                excluded = True
                break

        if not excluded:
            markdown_files.append(md_file)

    return markdown_files


def read_file(path: Path) -> str:
    """
    Read file content as UTF-8 text.

    Args:
        path: Path to file to read

    Returns:
        File content as string

    Raises:
        FileNotFoundError: If file does not exist
        IOError: If file cannot be read
    """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(path: Path, content: str) -> None:
    """
    Write content to file as UTF-8 text.

    Creates parent directories if they don't exist.

    Args:
        path: Path to file to write
        content: Content to write

    Raises:
        IOError: If file cannot be written
    """
    # Ensure parent directory exists
    ensure_dir(path.parent)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def copy_static_assets(output_dir: Path) -> None:
    """
    Copy CSS and JavaScript files to output directory.

    Copies static/style.css and static/script.js from package directory
    to <output_dir>/static/

    Args:
        output_dir: Output directory (e.g., site/)

    Raises:
        FileNotFoundError: If static assets are not found
        IOError: If files cannot be copied
    """
    # Find package directory (parent of this module)
    package_dir = Path(__file__).parent.parent
    static_src = package_dir / "static"
    static_dst = output_dir / "static"

    # Ensure destination directory exists
    ensure_dir(static_dst)

    # Copy CSS file
    css_src = static_src / "style.css"
    if css_src.exists():
        shutil.copy2(css_src, static_dst / "style.css")

    # Copy JavaScript file
    js_src = static_src / "script.js"
    if js_src.exists():
        shutil.copy2(js_src, static_dst / "script.js")


def copy_image_assets(input_dir: Path, output_dir: Path, exclude_patterns: List[str]) -> None:
    """
    Copy image files from input directory to output directory.

    Preserves directory structure. Copies files with these extensions:
    .png, .jpg, .jpeg, .gif, .svg, .pdf

    Args:
        input_dir: Input directory containing images
        output_dir: Output directory (e.g., site/)
        exclude_patterns: List of glob patterns to exclude

    Raises:
        IOError: If files cannot be copied
    """
    # Define image extensions to copy
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf'}

    # Get output directory name for exclusion
    output_dir_name = output_dir.name

    # Find all image files
    for ext in image_extensions:
        for image_file in input_dir.rglob(f"*{ext}"):
            # Skip if not a file
            if not image_file.is_file():
                continue

            # Get relative path for pattern matching
            try:
                relative_path = image_file.relative_to(input_dir)
            except ValueError:
                # Skip if file is not under input_dir
                continue

            # Skip if file is inside output directory (prevent recursive copying)
            if relative_path.parts and relative_path.parts[0] == output_dir_name:
                continue

            # Check if file matches any exclude pattern
            excluded = False
            for pattern in exclude_patterns:
                relative_str = relative_path.as_posix()
                if fnmatch.fnmatch(relative_str, pattern):
                    excluded = True
                    break

            if not excluded:
                # Copy file to output directory with same relative path
                output_path = output_dir / relative_path
                ensure_dir(output_path.parent)
                shutil.copy2(image_file, output_path)


def ensure_dir(path: Path) -> None:
    """
    Ensure directory exists, creating it if necessary.

    Args:
        path: Directory path to ensure exists
    """
    path.mkdir(parents=True, exist_ok=True)
