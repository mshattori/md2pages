"""Configuration management for md2pages."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List
import warnings

import yaml


@dataclass
class SiteConfig:
    """Site configuration."""
    output_dir: str = "site"
    exclude: List[str] = field(default_factory=list)
    site_title: str = "Site"
    base_url: str = "/"
    respect_gitignore: bool = True


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
    exclude_patterns: List[str] = []

    if not config_file.exists():
        return _finalize_config(config, input_dir, exclude_patterns)

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)

        if yaml_data is None:
            return _finalize_config(config, input_dir, exclude_patterns)

        # Merge configuration
        if 'output_dir' in yaml_data:
            config.output_dir = yaml_data['output_dir']

        if 'exclude' in yaml_data:
            exclude = yaml_data['exclude']
            if isinstance(exclude, list) and all(isinstance(x, str) for x in exclude):
                _extend_unique(exclude_patterns, exclude)
            else:
                warnings.warn(
                    "Invalid 'exclude' in .site.yml (must be list of strings). "
                    "Using defaults."
                )

        if 'respect_gitignore' in yaml_data:
            value = yaml_data['respect_gitignore']
            if isinstance(value, bool):
                config.respect_gitignore = value
            else:
                warnings.warn(
                    "Invalid 'respect_gitignore' in .site.yml (must be boolean). "
                    "Using default of True."
                )

        if 'site' in yaml_data and isinstance(yaml_data['site'], dict):
            site_data = yaml_data['site']
            if 'title' in site_data:
                config.site_title = site_data['title']
            if 'base_url' in site_data:
                config.base_url = site_data['base_url']

        return _finalize_config(config, input_dir, exclude_patterns)

    except yaml.YAMLError as e:
        warnings.warn(
            f"Failed to parse .site.yml: {e}. Using default configuration."
        )
        return _finalize_config(config, input_dir, exclude_patterns)
    except Exception as e:
        warnings.warn(
            f"Error reading .site.yml: {e}. Using default configuration."
        )
        return _finalize_config(config, input_dir, exclude_patterns)


def _finalize_config(config: SiteConfig, input_dir: Path, exclude_patterns: List[str]) -> SiteConfig:
    """
    Finalize configuration by applying .gitignore patterns if enabled.
    """
    if config.respect_gitignore:
        gitignore_patterns = _load_gitignore_patterns(input_dir)
        _extend_unique(exclude_patterns, gitignore_patterns)

    config.exclude = exclude_patterns
    return config


def _extend_unique(target: List[str], items: Iterable[str]) -> None:
    """
    Extend a list with items, avoiding duplicates while preserving order.
    """
    existing = set(target)
    for item in items:
        if item not in existing:
            target.append(item)
            existing.add(item)


def _load_gitignore_patterns(input_dir: Path) -> List[str]:
    """
    Load glob-style patterns derived from .gitignore entries.
    """
    gitignore = input_dir / ".gitignore"
    if not gitignore.exists():
        return []

    patterns: List[str] = []

    try:
        lines = gitignore.read_text(encoding='utf-8').splitlines()
    except OSError as e:
        warnings.warn(f"Failed to read .gitignore: {e}")
        return []

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("!"):
            # md2pages currently does not support negative patterns
            continue

        if line.startswith("/"):
            line = line[1:]

        if not line:
            continue

        if line.endswith("/"):
            line = f"{line.rstrip('/')}/**"

        # Treat plain directory names as both exact and recursive matches
        if "/" not in line and not any(ch in line for ch in ["*", "?", "["]):
            candidates = [line, f"{line}/**"]
        else:
            candidates = [line]

        for candidate in candidates:
            if candidate not in patterns:
                patterns.append(candidate)

    return patterns
