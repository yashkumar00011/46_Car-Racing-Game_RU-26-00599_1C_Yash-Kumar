"""
Main entry point for Car Racing Game.
Project Number: PS No. 46
Project Title: Car Racing Game
Language: Python 3
Library: Pygame
"""

import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WINDOW_TITLE
from game import Game


def main():
    """Initialize Pygame and run the primary game loop."""
    # Initialize Pygame core and font modules
    pygame.init()
    pygame.font.init()

    # Create display window of exactly 400x600 pixels
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    # Clock to regulate frame rate at 60 FPS
    clock = pygame.time.Clock()

    # Create game instance
    game = Game()

    running = True
    while running:
        # Event Handling Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Escape key exits the game cleanly
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    # Pass key event to game controller (moves car or restarts if Game Over)
                    game.handle_key(event.key)

        # Update game logic
        game.update()

        # Render graphics to screen
        game.draw(screen)

        # Flip display buffer
        pygame.display.flip()

        # Regulate game speed to 60 FPS
        clock.tick(FPS)

    # Clean shutdown
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
