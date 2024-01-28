from game_windows.start_window import start_starting_window
from game_windows.game import start_the_game
import pygame


def main():
    try:
        print("Starting the game...")
        game_running = start_starting_window()
        while game_running:
            start_the_game()
    except pygame.error:
        pass


if __name__ == "__main__":
    main()
