"""Configuration management for md2pages."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List
import warnings

import yaml


@dataclass
class SiteConfig:
    """Site configuration."""
    output_dir: str = "site"
    exclude: List[str] = field(default_factory=lambda: [".git/**"])
    site_title: str = "Site"
    base_url: str = "/"


def load_config(input_dir: Path) -> SiteConfig:
    """
    Load configuration from .site.yml in input directory.

    Args:
        input_dir: Path to input directory

    Returns:
        SiteConfig instance with merged configuration

    Note:
        If .site.yml is invalid or missing, returns default configuration
        with a warning.
    """
    config_file = input_dir / ".site.yml"

    # Start with default config
    config = SiteConfig()

    if not config_file.exists():
        return config

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)

        if yaml_data is None:
            return config

        # Merge configuration
        if 'output_dir' in yaml_data:
            config.output_dir = yaml_data['output_dir']

        if 'exclude' in yaml_data:
            exclude = yaml_data['exclude']
            if isinstance(exclude, list) and all(isinstance(x, str) for x in exclude):
                config.exclude = exclude
            else:
                warnings.warn(
                    f"Invalid 'exclude' in .site.yml (must be list of strings). "
                    f"Using defaults."
                )

        if 'site' in yaml_data and isinstance(yaml_data['site'], dict):
            site_data = yaml_data['site']
            if 'title' in site_data:
                config.site_title = site_data['title']
            if 'base_url' in site_data:
                config.base_url = site_data['base_url']

        return config

    except yaml.YAMLError as e:
        warnings.warn(
            f"Failed to parse .site.yml: {e}. Using default configuration."
        )
        return config
    except Exception as e:
        warnings.warn(
            f"Error reading .site.yml: {e}. Using default configuration."
        )
        return config
