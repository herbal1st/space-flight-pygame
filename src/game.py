"""Orchestrator context coordinating subsystems, loaders, and event loops."""
import sys
from random import choice, randint
from pathlib import Path
import pygame

import src.settings as settings
from src.screens.menu import StartingScreen
from src.screens.pause import PauseScreen
from src.screens.game_over import GameOver
from src.screens.player_name import PlayerName
from src.screens.options import Options
from src.screens.controls import Controls
from src.screens.highscores import Highscores

from src.entities.player import PlayerShip
from src.entities.star import Star
from src.entities.enemy import Enemy
from src.entities.obstacle import Obstacle
from src.entities.powerups import (
    ShieldPowerup, HealthPowerup, EnergyPowerup
)
from src.entities.explosion import Explosion


class SafeSound:
    """Wrapper to prevent audio channel saturation and volume clipping."""

    def __init__(self, path: Path, max_overlap: int = 3) -> None:
        self.sound = pygame.mixer.Sound(str(path))
        self.max_overlap = max_overlap

    def play(self, loops: int = 0, fade_ms: int = 0) -> None:
        if self.sound.get_num_channels() < self.max_overlap:
            self.sound.play(loops=loops, fade_ms=fade_ms)

    def set_volume(self, value: float) -> None:
        self.sound.set_volume(value)

    def fadeout(self, time: int) -> None:
        self.sound.fadeout(time)


class Game:
    """The master game manager class encapsulating active session state."""

    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Space Flight")

        icon_path = settings.GRAPHICS_DIR / "artwork" / "joe mini logo.png"
        if icon_path.exists():
            icon = pygame.image.load(str(icon_path)).convert_alpha()
            pygame.display.set_icon(icon)

        # Ensure directory persistence
        self._ensure_highscore_files()

        # Engine states
        self.game_init: bool = True
        self.game_state: str = "start"
        self.game_speed: float = 1.0
        self.score: int = 0
        self.difficulty: int = settings.DIFFICULTY_MEDIUM
        self.player_name: str = ""

        # UI Font registry with safe cross-platform fallback options
        font_fallbacks = ["Agency FB", "Century Gothic", "Arial", "sans-serif"]
        self.font_1 = pygame.font.SysFont(font_fallbacks, 20)
        self.font_2 = pygame.font.SysFont(font_fallbacks, 48)
        self.font_3 = pygame.font.SysFont(font_fallbacks, 72)

        # Load Audio Sound Systems
        self.sound_menu_music = self._load_sound("menu music.mp3")
        self.sound_menu_music.set_volume(0.1)
        self.sound_game_music = self._load_sound("game music.mp3")
        self.sound_game_music.set_volume(0.1)
        self.sound_player_laser_shot = self._load_sound(
            "player laser shot.wav"
        )
        self.sound_ufo_laser_hit = self._load_sound("ufo laser hit.wav")
        self.sound_powerup = self._load_sound("powerup.wav")
        self.sound_ufo_explosion = self._load_sound("ufo explosion.wav")
        self.sound_rock_explosion = self._load_sound("rock explosion.wav")
        self.sound_ufo_laser_shot = self._load_sound("ufo laser shot.wav")

        self.clock = pygame.time.Clock()

        # Internal Timers Definition
        self.enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, 2000)

        self.obstacle_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.obstacle_timer, randint(1000, 2500))

        self.powerup_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(self.powerup_timer, randint(10000, 25000))

        # Organize Sprite Group Entities
        self.start_menu = pygame.sprite.GroupSingle(StartingScreen(self))
        self.options = pygame.sprite.GroupSingle()
        self.controls = pygame.sprite.GroupSingle()
        self.highscores = pygame.sprite.GroupSingle()
        self.game_over = pygame.sprite.GroupSingle()
        self.input_name = pygame.sprite.GroupSingle()
        self.pause = pygame.sprite.GroupSingle()

        self.ship = pygame.sprite.GroupSingle()
        self.player_shots = pygame.sprite.Group()
        self.player_shield = pygame.sprite.GroupSingle()

        self.enemies = pygame.sprite.Group()
        self.enemy_shots = pygame.sprite.Group()

        self.obstacles = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

    def _load_sound(self, filename: str) -> SafeSound:
        path = settings.SOUND_DIR / filename
        if path.exists():
            return SafeSound(path)
        # Empty fallback logic handled by wrapper
        return SafeSound(settings.SOUND_DIR / filename)

    def _ensure_highscore_files(self) -> None:
        """Autocreates empty database files to prevent execution crash."""
        settings.HIGHSCORES_DIR.mkdir(parents=True, exist_ok=True)
        for diff in ("easy", "medium", "hard"):
            n_file = settings.HIGHSCORES_DIR / f"{diff} names.txt"
            s_file = settings.HIGHSCORES_DIR / f"{diff} scores.txt"
            if not n_file.exists():
                with open(n_file, "w") as f:
                    f.write(
                        "UNUSED\n"
                        + "\n".join(["--empty--"] * 10)
                        + "\n"
                    )
            if not s_file.exists():
                with open(s_file, "w") as f:
                    f.write(
                        "999999999\n"
                        + "\n".join([str(10 - i) for i in range(10)])
                        + "\n"
                    )

    def test_highscore(self, score: int, difficulty_setting: int) -> bool:
        diff = self.get_difficulty_name(difficulty_setting)
        score_path = settings.HIGHSCORES_DIR / f"{diff} scores.txt"
        with open(score_path, "r") as f:
            board_scores = f.readlines()
        return score > int(board_scores[10].strip())

    def place_highscore(
        self, name: str, score: int, difficulty_setting: int
    ) -> None:
        diff = self.get_difficulty_name(difficulty_setting)
        score_path = settings.HIGHSCORES_DIR / f"{diff} scores.txt"
        name_path = settings.HIGHSCORES_DIR / f"{diff} names.txt"

        with open(score_path, "r") as f:
            board_scores = f.readlines()
        with open(name_path, "r") as f:
            board_names = f.readlines()

        for i in range(10, 0, -1):
            if int(board_scores[i].strip()) < score <= int(
                board_scores[i - 1].strip()
            ):
                board_scores.insert(i, f"{score}\n")
                board_scores.pop()
                board_names.insert(i, f"{name}\n")
                board_names.pop()

        with open(score_path, "w") as f:
            f.writelines(board_scores)
        with open(name_path, "w") as f:
            f.writelines(board_names)

    def get_difficulty_name(self, value: int) -> str:
        if value == settings.DIFFICULTY_EASY:
            return "easy"
        if value == settings.DIFFICULTY_MEDIUM:
            return "medium"
        return "hard"

    def transition_to(self, state: str) -> None:
        """Transitions game state and handles centralized routing."""
        self.start_menu.empty()
        self.options.empty()
        self.controls.empty()
        self.highscores.empty()
        self.game_over.empty()
        self.input_name.empty()
        self.pause.empty()

        self.game_state = state

        # Handle mouse grabbing and visibility based on active gameplay state
        if state == "game":
            pygame.event.set_grab(True)
        else:
            pygame.event.set_grab(False)
            pygame.mouse.set_visible(True)

        if state == "start":
            self.start_menu.add(StartingScreen(self))
        elif state == "options":
            self.options.add(Options(self))
        elif state == "controls":
            self.controls.add(Controls(self))
        elif state == "highscores":
            self.highscores.add(Highscores(self))
        elif state == "pause":
            self.pause.add(PauseScreen(self))
        elif state == "game over":
            self.game_over.add(GameOver(self))
        elif state == "input name":
            self.input_name.add(PlayerName(self))

    def start_game(self) -> None:
        self.sound_menu_music.fadeout(2000)
        self.sound_game_music.play(loops=-1, fade_ms=2000)
        self.transition_to("game")
        self.ship.add(PlayerShip(self))
        pygame.mouse.set_pos(self.ship.sprite.rect.center)

    def trigger_pause(self) -> None:
        self.transition_to("pause")

    def resume_game(self) -> None:
        self.transition_to("game")
        pygame.mouse.set_pos(self.ship.sprite.rect.center)

    def trigger_game_over(self) -> None:
        self.ship.empty()
        self.player_shield.empty()
        self.player_shots.empty()
        self.powerups.empty()
        self.enemies.empty()
        self.enemy_shots.empty()
        self.obstacles.empty()
        self.explosions.empty()
        self.transition_to("game over")

    def update_enemy_timer(self) -> None:
        pygame.time.set_timer(self.enemy_timer, int(2000 / self.game_speed))

    def update_obstacle_timer(self) -> None:
        pygame.time.set_timer(
            self.obstacle_timer,
            randint(
                int(1000 / self.game_speed), int(3000 / self.game_speed)
            ),
        )

    def shutdown(self) -> None:
        pygame.quit()
        sys.exit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shutdown()

            # Window focus loss auto-pause handler (focus safety)
            is_focus_lost = False
            if event.type == pygame.ACTIVEEVENT:
                if hasattr(event, "gain") and event.gain == 0:
                    if hasattr(event, "state") and event.state == 2:
                        is_focus_lost = True
            elif event.type == pygame.WINDOWFOCUSLOST:
                is_focus_lost = True

            if is_focus_lost and self.game_state == "game":
                self.trigger_pause()

            # Centralized Single-Frame Keydown Router (prevents key conflicts)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "game":
                        self.trigger_pause()
                    elif self.game_state == "pause":
                        self.resume_game()

            if self.game_state == "game":
                if event.type == self.enemy_timer:
                    self.enemies.add(Enemy(self))
                    self.update_enemy_timer()

                if event.type == self.obstacle_timer:
                    self.obstacles.add(Obstacle(self))
                    self.update_obstacle_timer()

                if event.type == self.powerup_timer:
                    choice_pow = choice(
                        [
                            ShieldPowerup(self),
                            HealthPowerup(self),
                            EnergyPowerup(self),
                        ]
                    )
                    self.powerups.add(choice_pow)

            if self.game_state == "input name":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.place_highscore(
                            self.player_name, self.score, self.difficulty
                        )
                        self.transition_to("start")
                    else:
                        if len(self.player_name) <= settings.MAX_NAME_LENGTH:
                            char = event.unicode.upper()
                            if char in settings.LEGAL_LETTERS:
                                self.player_name += char

    def update(self) -> None:
        # Background management
        if self.game_init:
            self.sound_menu_music.play(loops=-1)
            for _ in range(35):
                self.stars.add(
                    Star(self, y_pos=randint(-25, settings.SCREEN_HEIGHT + 25))
                )
            self.game_init = False

        if len(self.stars) <= 35:
            self.stars.add(Star(self))

        self.stars.update()

        # Logic calculations cycle
        if self.game_state == "start":
            self.player_name = ""
            self.start_menu.update()
        elif self.game_state == "options":
            self.options.update()
        elif self.game_state == "controls":
            self.controls.update()
        elif self.game_state == "highscores":
            self.highscores.update()
        elif self.game_state == "pause":
            self.pause.update()
        elif self.game_state == "game":
            if self.score > self.difficulty:
                self.game_speed = 1.0 + self.score / self.difficulty / 25.0

            self.explosions.update()
            self.obstacles.update()
            self.enemies.update()
            self.enemy_shots.update()
            self.player_shots.update()
            self.powerups.update()
            self.ship.update()
            self.player_shield.update()
        elif self.game_state == "game over":
            self.game_over.update()
        elif self.game_state == "input name":
            self.input_name.update()

    def draw(self) -> None:
        """Drawing cycle with correct overlay layers rendering."""
        self.screen.fill((0, 0, 0))
        self.stars.draw(self.screen)

        if self.game_state == "start":
            self.start_menu.draw(self.screen)
            if self.start_menu.sprite:
                self.start_menu.sprite.draw_extras(self.screen)
        elif self.game_state == "options":
            self.options.draw(self.screen)
            if self.options.sprite:
                self.options.sprite.draw_extras(self.screen)
        elif self.game_state == "controls":
            self.controls.draw(self.screen)
            if self.controls.sprite:
                self.controls.sprite.draw_extras(self.screen)
        elif self.game_state == "highscores":
            self.highscores.draw(self.screen)
            if self.highscores.sprite:
                self.highscores.sprite.draw_extras(self.screen)
        elif self.game_state == "pause":
            self.pause.draw(self.screen)
        elif self.game_state == "game":
            self.explosions.draw(self.screen)
            self.obstacles.draw(self.screen)
            self.enemies.draw(self.screen)

            # Draw UFO rotating lights and extra layers
            for enemy in self.enemies:
                enemy.draw_extras(self.screen)

            self.enemy_shots.draw(self.screen)
            self.player_shots.draw(self.screen)
            self.powerups.draw(self.screen)
            self.ship.draw(self.screen)

            # Draw Ship extra overlays (exhaust, HUD, bars)
            if self.ship.sprite:
                self.ship.sprite.draw_extras(self.screen)

            self.player_shield.draw(self.screen)
        elif self.game_state == "game over":
            self.game_over.draw(self.screen)
            if self.game_over.sprite:
                self.game_over.sprite.draw_extras(self.screen)
        elif self.game_state == "input name":
            self.input_name.draw(self.screen)
            if self.input_name.sprite:
                self.input_name.sprite.draw_extras(self.screen)

        pygame.display.update()

    def run(self) -> None:
        """Main game control loop."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)
