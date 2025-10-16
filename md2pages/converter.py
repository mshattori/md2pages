"""Markdown conversion engine for md2pages."""

from pathlib import Path
import re
import markdown


def convert_markdown(md_content: str, fallback_title: str = "Untitled") -> tuple[str, str]:
    """
    Convert Markdown content to HTML and extract title.

    Removes frontmatter before conversion. Extracts title from frontmatter
    if available, otherwise uses fallback. Converts .md links to .html.

    Args:
        md_content: Markdown text to convert
        fallback_title: Title to use if no title in frontmatter

    Returns:
        Tuple of (html_content, title)
    """
    # Extract frontmatter and get title
    content_without_frontmatter, frontmatter_title = extract_frontmatter(md_content)

    # Use frontmatter title if available, otherwise fallback
    title = frontmatter_title if frontmatter_title else fallback_title

    # Convert .md links to .html before Markdown conversion
    content_with_fixed_links = convert_md_links_to_html(content_without_frontmatter)

    # Convert Markdown to HTML with extensions
    md = markdown.Markdown(extensions=['fenced_code', 'tables', 'toc'])
    html_content = md.convert(content_with_fixed_links)

    return html_content, title


def convert_md_links_to_html(md_content: str) -> str:
    """
    Convert .md links to .html links in Markdown content.

    Converts both [text](file.md) and [text](path/to/file.md) format links.

    Args:
        md_content: Markdown text with potential .md links

    Returns:
        Markdown text with .md links converted to .html
    """
    # Pattern to match Markdown links: [text](url.md)
    # Captures: [anything](path/to/file.md) and converts to [anything](path/to/file.html)
    pattern = r'\[([^\]]+)\]\(([^\)]+)\.md\)'
    replacement = r'[\1](\2.html)'

    return re.sub(pattern, replacement, md_content)


def extract_frontmatter(md_content: str) -> tuple[str, str | None]:
    """
    Extract and remove YAML frontmatter from Markdown content.

    Args:
        md_content: Markdown text potentially containing frontmatter

    Returns:
        Tuple of (content_without_frontmatter, title_from_frontmatter)
        title_from_frontmatter is None if no title found
    """
    # Pattern to match YAML frontmatter
    # Starts with ---, contains YAML, ends with ---
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'

    match = re.match(frontmatter_pattern, md_content, re.DOTALL)

    if not match:
        # No frontmatter found
        return md_content, None

    # Extract frontmatter content
    frontmatter_content = match.group(1)

    # Remove frontmatter from markdown content
    content_without_frontmatter = md_content[match.end():]

    # Try to extract title from frontmatter
    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', frontmatter_content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else None

    return content_without_frontmatter, title


def extract_title(md_content: str, fallback: str) -> str:
    """
    Extract the first level-1 heading from Markdown content.

    Args:
        md_content: Markdown text to search
        fallback: Title to return if no heading found

    Returns:
        First # heading text, or fallback if none found
    """
    # Match first level-1 heading (# Title)
    # Pattern: optional whitespace, #, one space, capture title text
    pattern = r'^\s*#\s+(.+?)(?:\s*\{[^}]*\})?\s*$'

    for line in md_content.split('\n'):
        match = re.match(pattern, line)
        if match:
            # Return the captured title text, stripped of extra whitespace
            return match.group(1).strip()

    # No heading found, return fallback
    return fallback
