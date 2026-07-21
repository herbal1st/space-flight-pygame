"""Visual explosive special effects triggered during entity collisions."""
from __future__ import annotations
import typing
from random import randint
import pygame

import src.settings as settings

if typing.TYPE_CHECKING:
    from src.game import Game


class Explosion(pygame.sprite.Sprite):
    """The visual animated explosion visual effect."""

    def __init__(
        self,
        game: Game,
        pos_x: list[int],
        pos_y: list[int],
        original: bool = False,
    ) -> None:
        super().__init__()
        self.game = game
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rand_pos_x: int = randint(pos_x[0], pos_x[1])
        self.rand_pos_y: int = randint(pos_y[0], pos_y[1])
        self.original = original

        path = settings.GRAPHICS_DIR / "explosion"
        explosion_images = [
            pygame.image.load(str(p)) for p in sorted(path.glob("*.png"))
        ]
        self.explosion_list = [
            pygame.transform.scale(img, (50, 50)).convert_alpha()
            for img in explosion_images
        ]
        self.explosion_index: float = 0.0
        self.image = self.explosion_list[int(self.explosion_index)]
        self.rect = self.image.get_rect(
            center=(self.rand_pos_x, self.rand_pos_y)
        )
        self.mask = pygame.mask.from_surface(self.image)

    def animation(self) -> None:
        self.explosion_index += 1.0
        if self.explosion_index >= len(self.explosion_list):
            self.explosion_index = float(len(self.explosion_list) - 1)
            self.kill()
        self.image = self.explosion_list[int(self.explosion_index)]

        if self.original:
            self.game.explosions.add(
                Explosion(self.game, self.pos_x, self.pos_y)
            )

    def update(self) -> None:
        self.animation()
