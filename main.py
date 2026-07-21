"""Application entry point initializing the game context and loop."""
from src.game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
