# md2pages

Markdown to responsive HTML converter for static sites.

## Description

md2pages converts directory-based Markdown documentation into responsive, mobile-friendly static websites. Designed for GitHub Pages hosting but works with any static site hosting.

## Features

- Converts `.md` files to responsive HTML
- Automatic index page generation
- Configurable file exclusion patterns
- Scroll position preservation
- Clean, centered layout (max-width 800px)
- Mobile and desktop responsive design

## Installation

```bash
# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

## Usage

```bash
uv run md2pages <INPUT_DIR>

# Example
uv run md2pages ~/Notes/
```

## Configuration

Create a `.site.yml` file in your input directory to customize the site generation.

### Configuration Options

```yaml
# Output directory name (default: "site")
output_dir: site

# Files to exclude from conversion (glob patterns)
# Default: [".git/**"]
exclude:
  - ".git/**"      # Exclude git directory
  - "drafts/**"    # Exclude drafts folder
  - "README.md"    # Exclude specific file
  - "*.tmp"        # Exclude by extension

# Site metadata
site:
  # Site title shown in header and page titles (default: "Site")
  title: "My Notes"

  # Base URL for links (default: "/")
  # Use "/" for GitHub Pages with custom domain
  # Use "" (empty) for local testing
  # Use "/repo-name/" for GitHub Pages project sites
  base_url: "/"
```

### Configuration Examples

**Example 1: GitHub Pages with custom domain**
```yaml
output_dir: site
exclude:
  - ".git/**"
  - "README.md"
site:
  title: "My Documentation"
  base_url: "/"
```

**Example 2: GitHub Pages project site**
```yaml
output_dir: docs  # GitHub Pages can use /docs folder
exclude:
  - ".git/**"
  - "README.md"
  - "drafts/**"
site:
  title: "Project Wiki"
  base_url: "/my-project/"  # Replace with your repo name
```

**Example 3: Local development**
```yaml
output_dir: site
exclude:
  - ".git/**"
  - "README.md"
site:
  title: "Local Notes"
  base_url: ""  # Empty for local file:// or simple HTTP server
```

### Frontmatter Support

md2pages supports YAML frontmatter in Markdown files. The frontmatter is removed from the HTML output, but the `title` field is used for the page title.

**Example Markdown file:**
```markdown
---
title: "My Custom Page Title"
date: 2024-01-01
tags: ["example", "documentation"]
---

# Content starts here

Your markdown content...
```

**Title Priority:**
1. Frontmatter `title` field (if present)
2. Filename without extension (fallback)

The frontmatter will not appear in the generated HTML output.

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run the tool
uv run md2pages <INPUT_DIR>
```

## License

MIT
