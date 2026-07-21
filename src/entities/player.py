"""Player controlled spaceship sprite and secondary player weapons/shields."""
from __future__ import annotations
from pathlib import Path
import typing
import pygame

import src.settings as settings
from src.entities.explosion import Explosion

if typing.TYPE_CHECKING:
    from src.game import Game


def _load_scaled_frames(
    path: Path, size: tuple[int, int]
) -> list[pygame.Surface]:
    """Helper to load, scale, and convert animations from a folder."""
    if not path.exists():
        return []
    return [
        pygame.transform.scale(
            pygame.image.load(str(p)), size
        ).convert_alpha()
        for p in sorted(path.glob("*.png"))
    ]


class PlayerShip(pygame.sprite.Sprite):
    """The player controlled spaceship sprite."""

    def __init__(self, game: Game) -> None:
        super().__init__()
        self.game = game
        self.score: int = 0
        self.movement_speed: int = 10
        self.laser_cooldown: int = 0
        self.trigger_laser_fire: int = 0
        self.use_mouse: bool = True
        self.activate_shield: bool = True
        self.health: int = 10
        self.energy: int = 200

        # Load base graphic
        img_path = settings.GRAPHICS_DIR / "ship" / "ship 33x33.png"
        img = pygame.image.load(str(img_path))
        self.image = pygame.transform.scale(img, (66, 66)).convert_alpha()
        self.rect = self.image.get_rect(
            midtop=(
                settings.SCREEN_WIDTH // 2,
                settings.SCREEN_HEIGHT - 200,
            )
        )
        self.mask = pygame.mask.from_surface(self.image)

        # Load animation asset sequences via module helper
        self.lights_list = _load_scaled_frames(
            settings.GRAPHICS_DIR / "ship" / "lights", (42, 14)
        )
        self.lights_index: float = 0.0

        self.exhaust_list = _load_scaled_frames(
            settings.GRAPHICS_DIR / "ship" / "exhaust", (66, 66)
        )
        self.exhaust_index: float = 0.0

        self.laser_gun_list = _load_scaled_frames(
            settings.GRAPHICS_DIR / "ship" / "laser gun", (66, 66)
        )
        self.laser_gun_index: float = 0.0

    def health_func(self) -> None:
        if self.health <= 0:
            self.use_mouse = False
            self.game.trigger_game_over()

    def controls(self) -> None:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_k]:
            self.use_mouse = False
        if pressed[pygame.K_m]:
            self.use_mouse = True

        # Keyboard mode movement controls
        if not self.use_mouse:
            pygame.mouse.set_visible(True)
            if pressed[pygame.K_LEFT]:
                self.rect.x -= self.movement_speed
            if pressed[pygame.K_RIGHT]:
                self.rect.x += self.movement_speed
            if pressed[pygame.K_UP]:
                self.rect.y -= self.movement_speed
            if pressed[pygame.K_DOWN]:
                self.rect.y += self.movement_speed

            # Sprite coordinate boundaries clamping
            self.rect.left = max(25, self.rect.left)
            self.rect.right = min(
                settings.SCREEN_WIDTH - 25, self.rect.right
            )
            self.rect.top = max(settings.SCREEN_HEIGHT // 2, self.rect.top)
            self.rect.bottom = min(
                settings.SCREEN_HEIGHT - 50, self.rect.bottom
            )

        # Mouse mode movement controls with cursor locking
        if self.use_mouse:
            pygame.mouse.set_visible(False)
            m_x, m_y = pygame.mouse.get_pos()

            # Clamp coordinates to ship flight corridor
            clamped_x = max(25, min(settings.SCREEN_WIDTH - 25, m_x))
            clamped_y = max(
                settings.SCREEN_HEIGHT // 2,
                min(settings.SCREEN_HEIGHT - 50, m_y),
            )

            # Warp OS cursor to prevent coordinate drift
            if m_x != clamped_x or m_y != clamped_y:
                pygame.mouse.set_pos((clamped_x, clamped_y))

            self.rect.center = (clamped_x, clamped_y)

        # Weapon loading and firing
        if self.laser_cooldown < 25:
            self.laser_cooldown += 1
        if self.energy > 0:
            firing_input = (
                pressed[pygame.K_SPACE]
                or pygame.mouse.get_pressed(3) == (True, False, False)
            )
            if firing_input and self.laser_cooldown >= 25:
                self.trigger_laser_fire = 1
            if self.trigger_laser_fire and int(self.laser_gun_index) == 4:
                self.game.player_shots.add(PlayerLaserBeam(self.game))
                self.energy -= 1
                self.laser_cooldown = 0
                self.game.sound_player_laser_shot.play()
                self.game.sound_player_laser_shot.set_volume(0.2)

    def _resolve_collision(
        self,
        group: pygame.sprite.Group,
        kill_target: bool,
        damage: int,
        sound: pygame.mixer.Sound,
        vol: float,
        is_major: bool,
    ) -> None:
        """Handles collision, damage, audio triggers, and explosion bursts."""
        for target in group:
            if pygame.sprite.collide_rect(self, target):
                if pygame.sprite.collide_mask(self, target):
                    if kill_target:
                        target.kill()
                    self.health = max(0, self.health - damage)
                    sound.play()
                    sound.set_volume(vol)
                    self.game.explosions.add(
                        Explosion(
                            self.game,
                            [target.rect.x, target.rect.right],
                            [target.rect.y, target.rect.bottom],
                            is_major,
                        )
                    )

    def collision(self) -> None:
        # Check enemy shot hits
        self._resolve_collision(
            self.game.enemy_shots,
            True,
            1,
            self.game.sound_ufo_laser_hit,
            0.1,
            False,
        )
        # Check enemy ufo body crashes
        self._resolve_collision(
            self.game.enemies,
            True,
            1,
            self.game.sound_ufo_explosion,
            0.2,
            True,
        )
        # Check asteroid crashes
        self._resolve_collision(
            self.game.obstacles,
            True,
            1,
            self.game.sound_rock_explosion,
            0.2,
            True,
        )

        # Pick up floating powerups
        from src.entities.powerups import (
            ShieldPowerup, HealthPowerup, EnergyPowerup
        )
        for powerup in self.game.powerups:
            if pygame.sprite.collide_rect(self, powerup):
                if pygame.sprite.collide_mask(self, powerup):
                    self.game.sound_powerup.play()
                    self.game.sound_powerup.set_volume(0.2)
                    if isinstance(powerup, ShieldPowerup):
                        powerup.kill()
                        self.game.player_shield.add(
                            PlayerShield(self.game)
                        )
                    elif isinstance(powerup, HealthPowerup):
                        powerup.kill()
                        self.health = min(10, self.health + 5)
                    elif isinstance(powerup, EnergyPowerup):
                        powerup.kill()
                        self.energy = min(200, self.energy + 100)

    def _draw_hud_gauge(
        self,
        surface: pygame.Surface,
        x_bg: int,
        border_color: tuple[int, int, int],
        start_x: float,
        end_x: float,
        color_channel: int,
    ) -> None:
        """Renders vector glowing indicators for health or energy gauges."""
        pygame.draw.rect(surface, border_color, (x_bg, 11, 256, 29), 2)
        for i in range(1, 6):
            color = (
                (0, 130 + i * 25, 0)
                if color_channel == 1
                else (0, 0, 130 + i * 25)
            )
            pygame.draw.line(
                surface,
                color,
                (int(start_x), 25),
                (int(end_x), 25),
                30 - i * 5,
            )

    def draw_extras(self, surface: pygame.Surface) -> None:
        """Draws layered composite ship decorations and health overlays."""
        # Render score HUD
        score_str = str(self.game.score)
        score_surface = self.game.font_2.render(
            score_str, True, (255, 255, 255)
        )
        x_pos = (
            settings.SCREEN_WIDTH // 2 - len(score_str) * 12
        )
        surface.blit(score_surface, (x_pos, 0))

        # Ship lighting layer
        lights_img = self.lights_list[int(self.lights_index)]
        surface.blit(
            lights_img, (self.rect.x + 12, self.rect.y + 38)
        )

        # Rocket engine exhaust layer
        exhaust_img = self.exhaust_list[int(self.exhaust_index)]
        surface.blit(
            exhaust_img, (self.rect.x, self.rect.y + 50)
        )

        # Firing weapon muzzle animations
        if self.energy > 0 and self.trigger_laser_fire:
            gun_img = self.laser_gun_list[int(self.laser_gun_index)]
            surface.blit(gun_img, (self.rect.x, self.rect.y - 42))

        # Draw glowing status indicators (Health Left / Energy Right)
        self._draw_hud_gauge(
            surface, 8, (0, 130, 0), 10, 11 + self.health * 25, 1
        )
        self._draw_hud_gauge(
            surface,
            settings.SCREEN_WIDTH - 263,
            (0, 0, 130),
            settings.SCREEN_WIDTH - 11 - self.energy * 1.25,
            settings.SCREEN_WIDTH - 10,
            2,
        )

    def update(self) -> None:
        self.health_func()
        self.controls()

        # Update tick counters (Logic)
        self.lights_index += 1.0
        if self.lights_index >= len(self.lights_list):
            self.lights_index = 0.0

        self.exhaust_index += 0.5
        if self.exhaust_index >= len(self.exhaust_list):
            self.exhaust_index = 0.0

        if self.energy > 0 and self.trigger_laser_fire:
            self.laser_gun_index += 1.0
            if self.laser_gun_index >= len(self.laser_gun_list):
                self.laser_gun_index = 0.0
                self.trigger_laser_fire = 0

        self.collision()


class PlayerLaserBeam(pygame.sprite.Sprite):
    """The player fired laser projectile."""

    def __init__(self, game: Game) -> None:
        super().__init__()
        self.game = game
        self.laser_beam_list = _load_scaled_frames(
            settings.GRAPHICS_DIR / "ship" / "laser beam", (14, 22)
        )
        self.laser_beam_index: float = 0.0
        self.image = self.laser_beam_list[int(self.laser_beam_index)]
        self.rect = self.image.get_rect(
            midbottom=self.game.ship.sprite.rect.midtop
        )
        self.mask = pygame.mask.from_surface(self.image, threshold=1)

    def animations(self) -> None:
        self.laser_beam_index += 1.0
        if self.laser_beam_index >= len(self.laser_beam_list):
            self.laser_beam_index = 0.0
        self.image = self.laser_beam_list[int(self.laser_beam_index)]

    def movement(self) -> None:
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

    def update(self) -> None:
        self.animations()
        self.movement()


class PlayerShield(pygame.sprite.Sprite):
    """Energy barrier defending the player."""

    def __init__(self, game: Game) -> None:
        super().__init__()
        self.game = game
        self.shield_health: int = 5

        self.image_list = _load_scaled_frames(
            settings.GRAPHICS_DIR / "ship" / "shield", (98, 98)
        )
        self.image_index: float = 0.0
        self.image = self.image_list[int(self.image_index)]
        self.rect = self.image.get_rect(
            center=(
                self.game.ship.sprite.rect.centerx,
                self.game.ship.sprite.rect.centery + 9,
            )
        )
        self.mask = pygame.mask.from_surface(self.image, threshold=1)

    def animation(self) -> None:
        self.rect = self.image.get_rect(
            center=(
                self.game.ship.sprite.rect.centerx,
                self.game.ship.sprite.rect.centery + 9,
            )
        )
        self.image_index += 0.1
        if self.image_index >= len(self.image_list):
            self.image_index = 0.0
        self.image = self.image_list[int(self.image_index)]

    def _resolve_collision(
        self,
        group: pygame.sprite.Group,
        damage: int,
        sound: pygame.mixer.Sound,
        vol: float,
        is_major: bool,
    ) -> None:
        """Handles shield impacts and integrity reduction."""
        for target in group:
            if pygame.sprite.collide_rect(self, target):
                if pygame.sprite.collide_mask(self, target):
                    target.kill()
                    self.shield_health -= damage
                    sound.play()
                    sound.set_volume(vol)
                    self.game.explosions.add(
                        Explosion(
                            self.game,
                            [target.rect.x, target.rect.right],
                            [target.rect.y, target.rect.bottom],
                            is_major,
                        )
                    )

    def collision(self) -> None:
        # Check shield enemy projectile absorptions
        self._resolve_collision(
            self.game.enemy_shots,
            1,
            self.game.sound_ufo_laser_hit,
            0.1,
            False,
        )
        # Check shield enemy body absorptions
        self._resolve_collision(
            self.game.enemies,
            1,
            self.game.sound_ufo_explosion,
            0.2,
            True,
        )
        # Check shield obstacle absorptions
        self._resolve_collision(
            self.game.obstacles,
            1,
            self.game.sound_rock_explosion,
            0.2,
            True,
        )

        if self.shield_health <= 0:
            self.kill()

    def update(self) -> None:
        self.animation()
        self.collision()
