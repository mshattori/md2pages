"""Enable execution as python -m md2pages."""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
