"""Application entry point initializing the game context and loop."""
from src.game import Game


def main() -> None:
    """Instantiate and run the master game application."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
