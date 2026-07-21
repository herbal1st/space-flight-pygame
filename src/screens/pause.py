"""Suspend execution displaying resume option buttons."""
from __future__ import annotations
import typing
import pygame

if typing.TYPE_CHECKING:
    from src.game import Game


class PauseScreen(pygame.sprite.Sprite):
    """Suspend execution displaying resume option buttons."""

    def __init__(self, game: Game) -> None:
        super().__init__()
        self.game = game
        self.back_clicked: bool = False

        back_p = self.game.sound_ufo_laser_shot.sound # Using safe references
        # Load background graphic
        path_back = self.game.sound_menu_music.sound
        import src.settings as settings
        back_p = settings.GRAPHICS_DIR / "artwork" / "back.png"
        self.image = pygame.image.load(str(back_p)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(285, 355))

    def interaction(self) -> None:
        pygame.mouse.set_visible(True)

        if pygame.mouse.get_pressed(3) == (True, False, False):
            m_pos = pygame.mouse.get_pos()
            if m_pos[0] in range(285, 515) and m_pos[1] in range(355, 445):
                self.back_clicked = True

        if self.back_clicked and pygame.mouse.get_pressed(3) == (
            False, False, False
        ):
            self.game.resume_game()

    def update(self) -> None:
        self.interaction()
