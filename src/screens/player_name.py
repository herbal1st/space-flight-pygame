"""Accepts alphabetical entries upon securing a highscore place."""
from __future__ import annotations
import typing
import pygame

import src.settings as settings

if typing.TYPE_CHECKING:
    from src.game import Game


class PlayerName(pygame.sprite.Sprite):
    """Accepts alphabetical entries upon securing a highscore place."""

    def __init__(self, game: Game) -> None:
        super().__init__()
        self.game = game
        self.submit_clicked: bool = False
        self.player_name: str = ""

        over_p = settings.GRAPHICS_DIR / "artwork" / "game over.png"
        self.image = pygame.image.load(
            str(over_p)
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=(0, 100))

        hs_p = (
            settings.GRAPHICS_DIR / "artwork" / "new highscore.png"
        )
        self.new_highscore = pygame.image.load(
            str(hs_p)
        ).convert_alpha()

        ent_n_p = (
            settings.GRAPHICS_DIR / "artwork" / "enter name.png"
        )
        self.enter_name = pygame.image.load(
            str(ent_n_p)
        ).convert_alpha()

        ent_p = settings.GRAPHICS_DIR / "artwork" / "enter.png"
        self.enter = pygame.image.load(
            str(ent_p)
        ).convert_alpha()

    def draw_extras(self, surface: pygame.Surface) -> None:
        """Renders overlay key input letters and verification interfaces."""
        surface.blit(self.new_highscore, (35, 260))
        surface.blit(self.enter_name, (25, 360))
        surface.blit(self.enter, (250, 640))

        render_name = self.game.font_3.render(
            self.game.player_name, True, (140, 255, 251)
        )
        x_pos = settings.SCREEN_WIDTH / 2 - render_name.get_width() / 2
        surface.blit(render_name, (x_pos, 495))
        pygame.draw.rect(
            surface, (140, 255, 251), (175, 493, 454, 94), 2
        )

    def interaction(self) -> None:
        if pygame.mouse.get_pressed(3) == (True, False, False):
            m_pos = pygame.mouse.get_pos()
            if m_pos[0] in range(285, 515) and m_pos[1] in range(640, 730):
                self.submit_clicked = True

        if self.submit_clicked and pygame.mouse.get_pressed(3) == (
            False, False, False
        ):
            self.game.place_highscore(
                self.game.player_name, self.game.score, self.game.difficulty
            )
            self.game.transition_to("start")

    def update(self) -> None:
        self.interaction()
