"""Layout demonstrating input bindings configuration."""
from __future__ import annotations
import typing
import pygame

import src.settings as settings

if typing.TYPE_CHECKING:
    from src.game import Game


class Controls(pygame.sprite.Sprite):
    """Layout demonstrating input bindings configuration."""

    def __init__(self, game: Game) -> None:
        super().__init__()
        self.game = game
        self.back_clicked: bool = False

        path_page = (
            settings.GRAPHICS_DIR / "artwork" / "controls page.png"
        )
        self.image = pygame.image.load(
            str(path_page)
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=(0, 0))

        path_back = settings.GRAPHICS_DIR / "artwork" / "back.png"
        self.back = pygame.image.load(
            str(path_back)
        ).convert_alpha()

    def draw_extras(self, surface: pygame.Surface) -> None:
        """Renders overlay escape back button."""
        surface.blit(self.back, (285, 640))

    def interaction(self) -> None:
        if pygame.mouse.get_pressed(3) == (True, False, False):
            m_pos = pygame.mouse.get_pos()
            if m_pos[0] in range(285, 515) and m_pos[1] in range(640, 730):
                self.back_clicked = True

        if self.back_clicked and pygame.mouse.get_pressed(3) == (
            False, False, False
        ):
            self.game.transition_to("start")

    def update(self) -> None:
        self.interaction()
