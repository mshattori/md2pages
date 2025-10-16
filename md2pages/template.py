"""Template rendering for md2pages."""

from dataclasses import dataclass
from pathlib import Path
from typing import List
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, TemplateNotFound


@dataclass
class PageInfo:
    """Page information for index generation."""
    title: str
    relative_path: str


class TemplateRenderer:
    """Jinja2 template renderer."""

    def __init__(self, template_dir: Path = None):
        """
        Initialize template renderer.

        Args:
            template_dir: Directory containing templates. If None, uses package templates/.
        """
        if template_dir is None:
            # Use package templates directory
            package_dir = Path(__file__).parent.parent
            template_dir = package_dir / "templates"

        try:
            self.env = Environment(loader=FileSystemLoader(str(template_dir)))
        except Exception as e:
            raise RuntimeError(f"Failed to initialize template environment: {e}")

    def render_page(self, content: str, title: str, site_title: str, base_url: str) -> str:
        """
        Render a page using page.html template.

        Args:
            content: HTML content to render
            title: Page title
            site_title: Site title
            base_url: Base URL for links

        Returns:
            Rendered HTML string

        Raises:
            TemplateNotFound: If page.html template is missing
            Exception: If rendering fails
        """
        try:
            template = self.env.get_template("page.html")
        except TemplateNotFound:
            raise TemplateNotFound("Template file not found: page.html")

        year = datetime.now().year

        return template.render(
            content=content,
            title=title,
            site_title=site_title,
            base_url=base_url,
            year=year
        )

    def render_index(self, pages: List[PageInfo], site_title: str, base_url: str) -> str:
        """
        Render index page using index.html template.

        Args:
            pages: List of PageInfo objects
            site_title: Site title
            base_url: Base URL for links

        Returns:
            Rendered HTML string

        Raises:
            TemplateNotFound: If index.html template is missing
            Exception: If rendering fails
        """
        try:
            template = self.env.get_template("index.html")
        except TemplateNotFound:
            raise TemplateNotFound("Template file not found: index.html")

        year = datetime.now().year

        return template.render(
            pages=pages,
            title="Index",
            site_title=site_title,
            base_url=base_url,
            year=year
        )
