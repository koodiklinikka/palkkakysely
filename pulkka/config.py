import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))
OUT_DIR = Path(os.environ.get("OUT_DIR", "out"))
YEAR = str(os.environ["YEAR"])
