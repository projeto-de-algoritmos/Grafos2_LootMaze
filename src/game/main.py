from src.config import WINDOW_WIDTH, WINDOW_HEIGHT
import pygame
import sys


if __name__ == '__main__':
    # Initialize Pygame
    pygame.init()

    # Set up the game window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill the window with red
        window.fill((255, 0, 0))

        # Update the display
        pygame.display.flip()
