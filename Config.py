from pathlib import Path

BASE_DIR = Path(__file__).parent

DATA_FOLDER = BASE_DIR / "data"

SP500_FILE = DATA_FOLDER / "SP500.csv"

DEFAULT_THEME = "plotly_dark"

REFRESH_SECONDS = 30
