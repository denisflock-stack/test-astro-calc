# tests/conftest.py
from pathlib import Path
import sys

# корень = папка, где лежат astrocore/ и tests/
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
