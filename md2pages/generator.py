"""Site generation orchestration for md2pages."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from .config import SiteConfig
from .converter import convert_markdown
from .template import TemplateRenderer, PageInfo
from .utils import find_markdown_files, read_file, write_file, copy_static_assets, copy_image_assets


@dataclass
class GenerationResult:
    """Result of site generation."""
    success_count: int
    failure_count: int
    errors: List[Tuple[Path, Exception]]


def generate_site(input_dir: Path, config: SiteConfig) -> GenerationResult:
    """
    Generate static site from Markdown files.

    Args:
        input_dir: Directory containing Markdown files
        config: Site configuration

    Returns:
        GenerationResult with statistics

    Raises:
        FileNotFoundError: If input directory doesn't exist
        RuntimeError: If templates are missing or output directory cannot be created
    """
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    # Initialize output directory
    output_dir = input_dir / config.output_dir

    # Find all Markdown files
    md_files = find_markdown_files(input_dir, config.exclude)

    if not md_files:
        # Return empty result if no files found
        return GenerationResult(success_count=0, failure_count=0, errors=[])

    # Initialize template renderer
    renderer = TemplateRenderer()

    # Track results
    success_count = 0
    failure_count = 0
    errors: List[Tuple[Path, Exception]] = []
    pages: List[PageInfo] = []
    has_user_index = False  # Track if user provided index.md

    # Process each Markdown file
    for md_file in md_files:
        try:
            # Read Markdown content
            md_content = read_file(md_file)

            # Get relative path for output
            relative_path = md_file.relative_to(input_dir)

            # Convert to HTML path
            html_path = relative_path.with_suffix('.html')

            # Normalize index.md (case-insensitive) to lowercase index.html
            if html_path.name.lower() == "index.html":
                html_path = html_path.parent / "index.html"

            # Extract fallback title from filename
            fallback_title = md_file.stem

            # Convert Markdown to HTML
            html_content, title = convert_markdown(md_content, fallback_title)

            # Render page
            rendered_html = renderer.render_page(
                content=html_content,
                title=title,
                site_title=config.site_title,
                base_url=config.base_url
            )

            # Write output file
            output_path = output_dir / html_path
            write_file(output_path, rendered_html)

            # Check if this is a user-provided index.md (case-insensitive)
            if html_path.name.lower() == "index.html":
                has_user_index = True

            # Track page for index (exclude user's index.md from the list)
            if html_path.name.lower() != "index.html":
                pages.append(PageInfo(
                    title=title,
                    relative_path=html_path.as_posix()
                ))

            success_count += 1

        except Exception as e:
            # Log error but continue processing
            errors.append((md_file, e))
            failure_count += 1

    # Sort pages by relative path for consistent index
    pages.sort(key=lambda p: p.relative_path)

    # Generate auto index page only if user didn't provide index.md
    if pages and not has_user_index:
        try:
            index_html = renderer.render_index(
                pages=pages,
                site_title=config.site_title,
                base_url=config.base_url
            )
            write_file(output_dir / "index.html", index_html)
        except Exception as e:
            errors.append((Path("index.html"), e))
            failure_count += 1

    # Copy static assets (CSS/JS)
    try:
        copy_static_assets(output_dir)
    except Exception as e:
        errors.append((Path("static assets"), e))
        # Don't increment failure_count for static assets

    # Copy image assets (preserving directory structure)
    try:
        copy_image_assets(input_dir, output_dir, config.exclude)
    except Exception as e:
        errors.append((Path("image assets"), e))
        # Don't increment failure_count for image assets

    return GenerationResult(
        success_count=success_count,
        failure_count=failure_count,
        errors=errors
    )
