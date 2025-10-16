"""Command-line interface for md2pages."""

import argparse
import sys
from pathlib import Path

from .config import load_config
from .generator import generate_site


def main() -> int:
    """
    Main CLI entry point.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to responsive HTML static site"
    )
    parser.add_argument(
        "input_dir",
        type=str,
        help="Input directory containing Markdown files"
    )

    args = parser.parse_args()

    # Convert to Path and validate
    input_dir = Path(args.input_dir)

    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}", file=sys.stderr)
        return 1

    if not input_dir.is_dir():
        print(f"Error: Input path is not a directory: {input_dir}", file=sys.stderr)
        return 1

    try:
        # Load configuration
        config = load_config(input_dir)

        # Generate site
        result = generate_site(input_dir, config)

        # Report results
        if result.success_count == 0 and result.failure_count == 0:
            print("Warning: No Markdown files found to convert.")
            return 0

        print(f"Conversion completed: {result.success_count} success, {result.failure_count} failures")

        # Report errors if any
        if result.errors:
            print("\nErrors encountered:", file=sys.stderr)
            for path, error in result.errors:
                print(f"  {path}: {error}", file=sys.stderr)

        # Return error code if there were failures
        if result.failure_count > 0:
            return 1

        return 0

    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
