"""Shield, Health, and Energy collectibles."""
from __future__ import annotations
from pathlib import Path
import typing
from random import randint
import pygame

import src.settings as settings

if typing.TYPE_CHECKING:
    from src.game import Game


def _load_scaled_frames(
    path: Path, size: tuple[int, int] | None = None
) -> list[pygame.Surface]:
    """Helper to load, scale, and convert animations from a folder."""
    if not path.exists():
        return []
    frames = []
    for p in sorted(path.glob("*.png")):
        img = pygame.image.load(str(p))
        if size is not None:
            img = pygame.transform.scale(img, size)
        frames.append(img.convert_alpha())
    return frames


class _BasePowerup(pygame.sprite.Sprite):
    """Internal base class handling movement, bounds, and animations."""

    def __init__(
        self,
        game: Game,
        folder_name: str,
        size: tuple[int, int] | None = None,
        anim_speed: float = 15.0,
    ) -> None:
        """Initialize generic bounding parameters and frame folders."""
        super().__init__()
        self.game: Game = game
        self.anim_speed: float = anim_speed

        path: Path = settings.GRAPHICS_DIR / "powerups" / folder_name
        self.image_list: list[pygame.Surface] = _load_scaled_frames(
            path, size
        )
        self.image_index: float = 0.0
        self.image: pygame.Surface = self.image_list[int(self.image_index)]
        self.rect: pygame.Rect = self.image.get_rect(
            center=(randint(50, settings.SCREEN_WIDTH - 50), -50)
        )
        self.mask: pygame.Mask = pygame.mask.from_surface(self.image)

        self.pos_x: float = float(self.rect.x)
        self.pos_y: float = float(self.rect.y)

    def animation(self, dt: float) -> None:
        """Compute dynamic animation ticks."""
        self.image_index += self.anim_speed * dt
        if self.image_index >= len(self.image_list):
            self.image_index = 0.0
        self.image = self.image_list[int(self.image_index)]

    def movement(self, dt: float) -> None:
        """Update forward vertical translation vector."""
        self.pos_y += 300.0 * dt
        self.rect.y = int(self.pos_y)
        if self.rect.top > settings.SCREEN_HEIGHT:
            self.kill()

    def update(self, dt: float) -> None:
        """Process animation indexes and linear translation."""
        self.animation(dt)
        self.movement(dt)


class ShieldPowerup(_BasePowerup):
    """Collectible shield regeneration powerup."""

    def __init__(self, game: Game) -> None:
        """Construct active shield powerup indicators."""
        super().__init__(
            game, "powerup shield", anim_speed=30.0
        )


class HealthPowerup(_BasePowerup):
    """Collectible hull repair powerup."""

    def __init__(self, game: Game) -> None:
        """Construct repair indicators."""
        super().__init__(game, "powerup health")


class EnergyPowerup(_BasePowerup):
    """Collectible ammunition recharging powerup."""

    def __init__(self, game: Game) -> None:
        """Construct reload indicators."""
        super().__init__(game, "powerup energy")
