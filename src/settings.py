"""Game configuration constants, layout properties, and paths."""
from pathlib import Path

# Screen resolution settings
SCREEN_WIDTH: int = 800  # pixels
SCREEN_HEIGHT: int = 800  # pixels
FPS: int = 60  # hertz

# Diagnostic configurations
SHOW_FPS: bool = True  # bool

# Difficulty score target constants
DIFFICULTY_EASY: int = 1000  # points
DIFFICULTY_MEDIUM: int = 500  # points
DIFFICULTY_HARD: int = 200  # points

# Character limits and parameters
MAX_NAME_LENGTH: int = 10  # characters

# Allowed characters for score submissions
LEGAL_LETTERS: tuple[str, ...] = (
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
    "Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P",
    "A", "S", "D", "F", "G", "H", "J", "K", "L",
    "Y", "X", "C", "V", "B", "N", "M"
)

# Relative directory paths
BASE_DIR: Path = Path(__file__).resolve().parent.parent
GRAPHICS_DIR: Path = BASE_DIR / "graphics"
SOUND_DIR: Path = BASE_DIR / "sound"
HIGHSCORES_DIR: Path = BASE_DIR / "highscores"
