"""Game configuration constants, layout properties, and paths."""
from pathlib import Path

# Screen resolution settings
SCREEN_WIDTH: int = 800  # pixels
SCREEN_HEIGHT: int = 800  # pixels
FPS: int = 60  # hertz

# Diagnostic configurations
SHOW_FPS: bool = False  # bool

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

# --- Dynamic Weapon & Drop Scaling Configurations ---
INITIAL_GAME_SPEED: float = 1.0  # units
SCALING_DAMPENER: float = 1.0  # ratio

# Player Weapon Base Parameters
BASE_PLAYER_LASER_SPEED: float = 420.0  # pixels/sec
BASE_PLAYER_LASER_DELAY: float = 0.420  # seconds
BASE_PLAYER_LASER_COST: int = 1  # energy points
ENERGY_SAVING_FACTOR: float = 0.5  # ratio

# Enemy Weapon Base Parameters
BASE_ENEMY_LASER_SPEED: float = 360.0  # pixels/sec
BASE_ENEMY_LASER_DELAY_MIN: float = 0.8  # seconds
BASE_ENEMY_LASER_DELAY_MAX: float = 1.8  # seconds

# Enemy Spawn Firing Cooldown Parameters
BASE_ENEMY_LASER_OCK_MIN: float = 2.0  # seconds
BASE_ENEMY_LASER_OCK_MAX: float = 4.0  # seconds

# Powerup Drop Base Parameters
BASE_POWERUP_SPAWN_RATE_MIN: int = 10000  # milliseconds
BASE_POWERUP_SPAWN_RATE_MAX: int = 22500  # milliseconds
