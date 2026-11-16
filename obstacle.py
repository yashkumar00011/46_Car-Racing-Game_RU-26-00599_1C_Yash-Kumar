"""
Obstacle (enemy car) module for Car Racing Game.
Handles obstacle generation, downward movement, pass detection, and rendering.
"""

import random
import pygame
from settings import (
    OBSTACLE_WIDTH,
    OBSTACLE_HEIGHT,
    MIN_OBSTACLE_X,
    MAX_OBSTACLE_X,
    DEFAULT_OBSTACLE_SPEED,
    SCREEN_HEIGHT,
    OBSTACLE_COLORS,
    COLOR_CAR_TIRE,
    COLOR_CAR_WINDOW,
    COLOR_CAR_LIGHTS_FRONT,
    COLOR_CAR_LIGHTS_BACK,
)


class Obstacle:
    """Represents an oncoming obstacle car on the road."""

    def __init__(
        self,
        x: int = None,
        y: int = -OBSTACLE_HEIGHT,
        speed: int = DEFAULT_OBSTACLE_SPEED,
        color=None,
    ):
        """
        Initialize an obstacle car.

        Args:
            x (int, optional): Horizontal position. If None, chosen randomly within [MIN_OBSTACLE_X, MAX_OBSTACLE_X].
            y (int, optional): Vertical position. Defaults to -OBSTACLE_HEIGHT (-80).
            speed (int, optional): Downward speed in pixels per frame. Defaults to DEFAULT_OBSTACLE_SPEED.
            color (tuple, optional): RGB color for the car. Defaults to random selection from OBSTACLE_COLORS.
        """
        self.width = OBSTACLE_WIDTH
        self.height = OBSTACLE_HEIGHT

        # Ensure random valid X position within road boundaries [50, 310]
        if x is None:
            self.x = random.randint(MIN_OBSTACLE_X, MAX_OBSTACLE_X)
        else:
            self.x = x

        self.y = y
        self.speed = speed
        self.color = color if color is not None else random.choice(OBSTACLE_COLORS)

        # Flag to ensure score increases only once per obstacle
        self.passed = False

        # Pygame Rect object for positioning and collision detection
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        """Move the obstacle downwards by its speed."""
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def is_passed(self) -> bool:
        """
        Check if the obstacle has completely passed the bottom of the screen.
        Screen height is 600. When rect.y >= SCREEN_HEIGHT (600), the obstacle
        has reached or passed the bottom boundary.

        Returns:
            bool: True if the obstacle is at or past the bottom of the screen.
        """
        return self.rect.y >= SCREEN_HEIGHT

    def draw(self, surface: pygame.Surface):
        """
        Draw the obstacle car facing downwards towards the player.

        Args:
            surface (pygame.Surface): The Pygame surface to render onto.
        """
        rx, ry = self.rect.x, self.rect.y
        w, h = self.width, self.height

        # 1. Tires (4 black rectangles slightly peeking from sides)
        tire_w, tire_h = 6, 16
        # Top Left Tire
        pygame.draw.rect(surface, COLOR_CAR_TIRE, (rx - 2, ry + 10, tire_w, tire_h), border_radius=2)
        # Top Right Tire
        pygame.draw.rect(surface, COLOR_CAR_TIRE, (rx + w - 4, ry + 10, tire_w, tire_h), border_radius=2)
        # Bottom Left Tire
        pygame.draw.rect(surface, COLOR_CAR_TIRE, (rx - 2, ry + h - 26, tire_w, tire_h), border_radius=2)
        # Bottom Right Tire
        pygame.draw.rect(surface, COLOR_CAR_TIRE, (rx + w - 4, ry + h - 26, tire_w, tire_h), border_radius=2)

        # 2. Main Car Body (Smooth rounded rectangle)
        pygame.draw.rect(surface, self.color, (rx, ry, w, h), border_radius=6)

        # 3. Rear Window (At the top, since car travels downwards)
        rear_window_rect = pygame.Rect(rx + 8, ry + 14, w - 16, 10)
        pygame.draw.rect(surface, COLOR_CAR_WINDOW, rear_window_rect, border_radius=2)

        # 4. Front Windshield (At the lower part, facing downwards)
        windshield_rect = pygame.Rect(rx + 6, ry + h - 36, w - 12, 14)
        pygame.draw.rect(surface, COLOR_CAR_WINDOW, windshield_rect, border_radius=3)

        # 5. Taillights (At the top)
        taillight_w, taillight_h = 7, 4
        pygame.draw.rect(surface, COLOR_CAR_LIGHTS_BACK, (rx + 4, ry + 2, taillight_w, taillight_h), border_radius=1)
        pygame.draw.rect(surface, COLOR_CAR_LIGHTS_BACK, (rx + w - 11, ry + 2, taillight_w, taillight_h), border_radius=1)

        # 6. Headlights (At the bottom front, pointing towards player)
        headlight_w, headlight_h = 7, 5
        pygame.draw.rect(surface, COLOR_CAR_LIGHTS_FRONT, (rx + 4, ry + h - 7, headlight_w, headlight_h), border_radius=2)
        pygame.draw.rect(surface, COLOR_CAR_LIGHTS_FRONT, (rx + w - 11, ry + h - 7, headlight_w, headlight_h), border_radius=2)
