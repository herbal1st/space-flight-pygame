"""Space rocks, meteors, and tumbling hazard entities."""
from __future__ import annotations
import typing
from random import randint, uniform
import pygame

import src.settings as settings
from src.entities.explosion import Explosion

if typing.TYPE_CHECKING:
    from src.game import Game


class Obstacle(pygame.sprite.Sprite):
    """The falling hazard space rocks/asteroids."""

    def __init__(self, game: Game) -> None:
        super().__init__()
        self.game = game
        self.speed_x: float = float(randint(0, 5)) * self.game.game_speed
        self.speed_y: float = float(randint(2, 5)) * self.game.game_speed
        self.direction_x: int = randint(0, 1)
        self.turn_direction: int = randint(0, 1)
        self.turn_speed: float = uniform(0.5, 1.0)

        path = settings.GRAPHICS_DIR / "obstacles" / "rock"
        obstacle_images = [
            pygame.image.load(str(p)) for p in sorted(path.glob("*.png"))
        ]
        self.obstacle_list = [
            pygame.transform.scale(img, (78, 78)).convert_alpha()
            for img in obstacle_images
        ]
        self.obstacle_index: float = 0.0
        self.image = self.obstacle_list[int(self.obstacle_index)]
        self.rect = self.image.get_rect(
            center=(randint(-100, settings.SCREEN_WIDTH + 100), -50)
        )
        self.mask = pygame.mask.from_surface(self.image)

    def animation(self) -> None:
        if self.turn_direction:
            self.obstacle_index += self.turn_speed
            if self.obstacle_index >= len(self.obstacle_list):
                self.obstacle_index = 0.0
            self.image = self.obstacle_list[int(self.obstacle_index)]
        else:
            self.obstacle_index -= self.turn_speed
            if self.obstacle_index <= 0:
                self.obstacle_index = float(len(self.obstacle_list) - 1)
            self.image = self.obstacle_list[int(self.obstacle_index)]

    def movement(self) -> None:
        if self.direction_x:
            self.rect.x += int(self.speed_x)
        else:
            self.rect.x -= int(self.speed_x)
        self.rect.y += int(self.speed_y)
        if (
            self.rect.right >= settings.SCREEN_WIDTH + 150
            or self.rect.x <= -150
        ):
            self.speed_x = float(randint(2, 5)) * self.game.game_speed
            self.speed_y = float(randint(2, 5)) * self.game.game_speed
            self.direction_x = not self.direction_x
        if self.rect.top > settings.SCREEN_HEIGHT:
            self.kill()

    def collision(self) -> None:
        for laser_beam in self.game.player_shots:
            if pygame.sprite.collide_rect(self, laser_beam):
                if pygame.sprite.collide_mask(self, laser_beam):
                    self.game.score += 10
                    laser_beam.kill()
                    self.game.sound_rock_explosion.play()
                    self.game.sound_rock_explosion.set_volume(0.2)
                    self.game.explosions.add(
                        Explosion(
                            self.game,
                            [self.rect.x, self.rect.right],
                            [self.rect.y, self.rect.bottom],
                            True,
                        )
                    )
                    self.kill()

    def update(self) -> None:
        self.animation()
        self.movement()
        self.collision()
