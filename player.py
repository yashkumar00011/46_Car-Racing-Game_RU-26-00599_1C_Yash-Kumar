"""
Player car module for Car Racing Game.
Handles player state, movement boundaries, input handling, and rendering.
"""

import pygame
from settings import (
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_START_X,
    PLAYER_START_Y,
    PLAYER_MOVE_STEP,
    MIN_PLAYER_X,
    MAX_PLAYER_X,
    COLOR_PLAYER,
    COLOR_CAR_WINDOW,
    COLOR_CAR_LIGHTS_FRONT,
    COLOR_CAR_LIGHTS_BACK,
    COLOR_CAR_TIRE,
    COLOR_WHITE,
)


class Player:
    """Represents the player's racing car."""

    def __init__(self, x: int = PLAYER_START_X, y: int = PLAYER_START_Y):
        """
        Initialize the player car.

        Args:
            x (int): Initial horizontal position. Defaults to PLAYER_START_X (180).
            y (int): Initial vertical position. Defaults to PLAYER_START_Y (500).
        """
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = x
        self.y = y
        # Pygame Rect object for positioning and collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_left(self) -> bool:
        """
        Move the car 10 pixels to the left, bounded by MIN_PLAYER_X (50).

        Returns:
            bool: True if the car moved, False if blocked by boundary.
        """
        if self.x > MIN_PLAYER_X:
            # Move exactly 10 pixels left, but not beyond MIN_PLAYER_X
            self.x = max(MIN_PLAYER_X, self.x - PLAYER_MOVE_STEP)
            self._update_rect()
            return True
        return False

    def move_right(self) -> bool:
        """
        Move the car 10 pixels to the right, bounded by MAX_PLAYER_X (310).

        Returns:
            bool: True if the car moved, False if blocked by boundary.
        """
        if self.x < MAX_PLAYER_X:
            # Move exactly 10 pixels right, but not beyond MAX_PLAYER_X
            self.x = min(MAX_PLAYER_X, self.x + PLAYER_MOVE_STEP)
            self._update_rect()
            return True
        return False

    def handle_input(self, key) -> bool:
        """
        Handle a key press event. Only LEFT and RIGHT arrows are valid.
        All other keys (e.g. SPACE, UP, DOWN) are strictly ignored.
        The player must never move vertically.

        Args:
            key: pygame key code or string ('LEFT', 'RIGHT', 'SPACE').

        Returns:
            bool: True if a valid key was handled, False if ignored.
        """
        if key in (pygame.K_LEFT, "LEFT"):
            self.move_left()
            return True
        elif key in (pygame.K_RIGHT, "RIGHT"):
            self.move_right()
            return True
        else:
            # Strictly ignore all invalid keys
            return False

    def reset(self, x: int = PLAYER_START_X, y: int = PLAYER_START_Y):
        """
        Reset the player car to its initial position.

        Args:
            x (int): Horizontal position to reset to. Defaults to PLAYER_START_X (180).
            y (int): Vertical position to reset to. Defaults to PLAYER_START_Y (500).
        """
        self.x = x
        self.y = y
        self._update_rect()

    def _update_rect(self):
        """Keep the internal Pygame Rect synchronized with (x, y)."""
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface: pygame.Surface):
        """
        Draw the player car with visual details (body, wheels, windows, lights).

        Args:
            surface (pygame.Surface): The Pygame surface to render onto.
        """
        rx, ry = self.rect.x, self.rect.y
        w, h = self.width, self.height

        # 1. Tires (4 black rectangles slightly peeking from sides)
        tire_w, tire_h = 6, 16
        # Front Left Tire
        pygame.draw.rect(surface, COLOR_CAR_TIRE, (rx - 2, ry + 10, tire_w, tire_h), border_radius=2)
        # Front Right Tire
        pygame.draw.rect(surface, COLOR_CAR_TIRE, (rx + w - 4, ry + 10, tire_w, tire_h), border_radius=2)
        # Rear Left Tire
        pygame.draw.rect(surface, COLOR_CAR_TIRE, (rx - 2, ry + h - 26, tire_w, tire_h), border_radius=2)
        # Rear Right Tire
        pygame.draw.rect(surface, COLOR_CAR_TIRE, (rx + w - 4, ry + h - 26, tire_w, tire_h), border_radius=2)

        # 2. Main Car Body (Smooth rounded rectangle)
        pygame.draw.rect(surface, COLOR_PLAYER, (rx, ry, w, h), border_radius=6)

        # 3. Racing Stripes (Dual white center stripes)
        pygame.draw.line(surface, COLOR_WHITE, (rx + w // 2 - 2, ry + 4), (rx + w // 2 - 2, ry + h - 6), 2)
        pygame.draw.line(surface, COLOR_WHITE, (rx + w // 2 + 2, ry + 4), (rx + w // 2 + 2, ry + h - 6), 2)

        # 4. Front Windshield (Dark tinted glass, curved)
        windshield_rect = pygame.Rect(rx + 6, ry + 22, w - 12, 14)
        pygame.draw.rect(surface, COLOR_CAR_WINDOW, windshield_rect, border_radius=3)

        # 5. Rear Window
        rear_window_rect = pygame.Rect(rx + 8, ry + h - 26, w - 16, 10)
        pygame.draw.rect(surface, COLOR_CAR_WINDOW, rear_window_rect, border_radius=2)

        # 6. Roof Cabin Outline
        roof_rect = pygame.Rect(rx + 8, ry + 36, w - 16, 16)
        pygame.draw.rect(surface, (180, 20, 20), roof_rect, border_radius=2)

        # 7. Headlights (Bright warm yellow at the top front)
        headlight_w, headlight_h = 7, 5
        pygame.draw.rect(surface, COLOR_CAR_LIGHTS_FRONT, (rx + 4, ry + 2, headlight_w, headlight_h), border_radius=2)
        pygame.draw.rect(surface, COLOR_CAR_LIGHTS_FRONT, (rx + w - 11, ry + 2, headlight_w, headlight_h), border_radius=2)

        # 8. Taillights (Red/Orange at the rear bottom)
        taillight_w, taillight_h = 7, 4
        pygame.draw.rect(surface, COLOR_CAR_LIGHTS_BACK, (rx + 4, ry + h - 6, taillight_w, taillight_h), border_radius=1)
        pygame.draw.rect(surface, COLOR_CAR_LIGHTS_BACK, (rx + w - 11, ry + h - 6, taillight_w, taillight_h), border_radius=1)
