"""Parallax scrolling star background element rendering layers."""
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


class Star(pygame.sprite.Sprite):
    """Parallax scrolling star for the simulated depth background."""

    # Static data table mapping distance values to pixel sizes
    SCALES: tuple[tuple[int, int], ...] = (
        (5, 13),
        (10, 26),
        (14, 39),
        (17, 52),
        (19, 89),
        (20, 117),
    )

    def __init__(self, game: Game, y_pos: int = -50) -> None:
        super().__init__()
        self.game = game
        self.star_distance: int = randint(0, 20)

        # Resolve scale size via data lookup
        scale_size = 13
        for limit, size in self.SCALES:
            if self.star_distance <= limit:
                scale_size = size
                break

        # Compile background star arrays using optimized direct scale load
        self.all_stars_list: list[list[pygame.Surface]] = []
        for num in range(1, 5):
            path = settings.GRAPHICS_DIR / "bg" / f"star {num}"
            star_imgs = _load_scaled_frames(path, (scale_size, scale_size))
            self.all_stars_list.append(star_imgs)

        self.star_index: float = float(
            randint(0, len(self.all_stars_list[0]) - 1)
        )
        self.all_stars_index: int = randint(0, len(self.all_stars_list) - 1)

        self.image = self.all_stars_list[self.all_stars_index][
            int(self.star_index)
        ]
        self.rect = self.image.get_rect(
            center=(randint(-25, settings.SCREEN_WIDTH + 25), y_pos)
        )

    def animation(self) -> None:
        self.star_index += 0.5
        if self.star_index >= len(self.all_stars_list[self.all_stars_index]):
            self.star_index = 0.0
        self.image = self.all_stars_list[self.all_stars_index][
            int(self.star_index)
        ]

    def movement(self) -> None:
        if self.star_distance in (0, 1, 2, 3, 4, 5):
            self.rect.y += int(1.0 * self.game.game_speed)
        elif self.star_distance in (6, 7, 8, 9, 10):
            self.rect.y += int(2.0 * self.game.game_speed)
        elif self.star_distance in (11, 12, 13, 14):
            self.rect.y += int(3.0 * self.game.game_speed)
        elif self.star_distance in (15, 16, 17):
            self.rect.y += int(4.0 * self.game.game_speed)
        elif self.star_distance in (18, 19):
            self.rect.y += int(5.0 * self.game.game_speed)
        else:
            self.rect.y += int(6.0 * self.game.game_speed)
        if self.rect.top > settings.SCREEN_HEIGHT:
            self.kill()

    def update(self) -> None:
        self.animation()
        self.movement()
