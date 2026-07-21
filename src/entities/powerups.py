"""Shield, Health, and Energy logic collectibles inheriting from base class."""
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
    """Internal base class handling common movement, bounds, and animations."""

    def __init__(
        self,
        game: Game,
        folder_name: str,
        size: tuple[int, int] | None = None,
        anim_speed: float = 0.25,
    ) -> None:
        super().__init__()
        self.game = game
        self.anim_speed = anim_speed

        path = settings.GRAPHICS_DIR / "powerups" / folder_name
        self.image_list = _load_scaled_frames(path, size)
        self.image_index: float = 0.0
        self.image = self.image_list[int(self.image_index)]
        self.rect = self.image.get_rect(
            center=(randint(50, settings.SCREEN_WIDTH - 50), -50)
        )
        self.mask = pygame.mask.from_surface(self.image)

    def animation(self) -> None:
        self.image_index += self.anim_speed
        if self.image_index >= len(self.image_list):
            self.image_index = 0.0
        self.image = self.image_list[int(self.image_index)]

    def movement(self) -> None:
        self.rect.y += 5
        if self.rect.top > settings.SCREEN_HEIGHT:
            self.kill()

    def update(self) -> None:
        self.animation()
        self.movement()


class ShieldPowerup(_BasePowerup):
    """Collectible shield regeneration powerup."""

    def __init__(self, game: Game) -> None:
        super().__init__(
            game, "powerup shield", anim_speed=0.5
        )


class HealthPowerup(_BasePowerup):
    """Collectible hull repair powerup."""

    def __init__(self, game: Game) -> None:
        super().__init__(game, "powerup health")


class EnergyPowerup(_BasePowerup):
    """Collectible ammunition recharging powerup."""

    def __init__(self, game: Game) -> None:
        super().__init__(game, "powerup energy")
