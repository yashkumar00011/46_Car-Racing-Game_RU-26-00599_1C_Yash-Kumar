"""
Game controller and logic module for Car Racing Game.
Separates game state and logic from Pygame rendering to enable comprehensive automated testing.
"""

import pygame
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ROAD_LEFT,
    ROAD_RIGHT,
    ROAD_WIDTH,
    ROAD_BORDER_WIDTH,
    ROAD_SCROLL_SPEED,
    LANE_MARKING_WIDTH,
    LANE_MARKING_HEIGHT,
    LANE_MARKING_GAP,
    COLOR_GRASS,
    COLOR_GRASS_DETAIL,
    COLOR_ROAD,
    COLOR_ROAD_BORDER,
    COLOR_LANE_MARKING,
    COLOR_TEXT,
    COLOR_SCORE_LABEL,
    COLOR_GAME_OVER,
    COLOR_RESTART_HINT,
    COLOR_OVERLAY,
    OBSTACLE_SPAWN_INTERVAL,
    PLAYER_START_X,
    PLAYER_START_Y,
)
from player import Player
from obstacle import Obstacle


class Game:
    """Manages game state, logic updates, collision detection, and rendering."""

    def __init__(self, headless: bool = False):
        """
        Initialize the game instance.

        Args:
            headless (bool): If True, Pygame visual rendering and fonts are disabled
                             for fast, headless unit testing.
        """
        self.headless = headless

        # Core Game Objects
        self.player = Player(PLAYER_START_X, PLAYER_START_Y)
        self.obstacles: list[Obstacle] = []

        # Game State
        self.score = 0
        self.game_over = False
        self.is_running = True
        self.spawn_timer = 0
        self.road_scroll_offset = 0

        # Fonts for rendering (only initialized if not headless)
        self.font_score = None
        self.font_game_over = None
        self.font_restart = None

        if not self.headless:
            self._init_fonts()

    def _init_fonts(self):
        """Safely initialize fonts if Pygame font module is active."""
        if not pygame.font.get_init():
            pygame.font.init()

        try:
            self.font_score = pygame.font.SysFont("Arial", 22, bold=True)
            self.font_game_over = pygame.font.SysFont("Arial", 46, bold=True)
            self.font_restart = pygame.font.SysFont("Arial", 22, bold=True)
        except Exception:
            # Fallback to default Pygame font if system fonts fail
            self.font_score = pygame.font.Font(None, 28)
            self.font_game_over = pygame.font.Font(None, 52)
            self.font_restart = pygame.font.Font(None, 28)

    def reset(self):
        """
        Reset the player, score, obstacles, and restart the game.
        Triggered when pressing 'R' after Game Over or on manual reset.
        """
        self.player.reset(PLAYER_START_X, PLAYER_START_Y)
        self.obstacles.clear()
        self.score = 0
        self.game_over = False
        self.spawn_timer = 0
        self.road_scroll_offset = 0

    def handle_key(self, key) -> bool:
        """
        Handle a key press event.

        - If Game Over: Pressing 'R' or pygame.K_r restarts the game.
        - If Game Running: LEFT / RIGHT move player; invalid keys are ignored.

        Args:
            key: Pygame key constant or string identifier ('LEFT', 'RIGHT', 'R', 'SPACE').

        Returns:
            bool: True if key triggered an action, False if ignored.
        """
        if self.game_over:
            # Check for restart key 'R'
            if key in (pygame.K_r, "R", "r"):
                self.reset()
                return True
            return False

        # If game is running, delegate movement key to player
        return self.player.handle_input(key)

    def spawn_obstacle(self, x: int = None, y: int = -80, speed: int = None) -> Obstacle:
        """
        Create and spawn a new obstacle at a valid road X position.

        Args:
            x (int, optional): Horizontal position. Defaults to random within [50, 310].
            y (int, optional): Initial vertical position.
            speed (int, optional): Downward speed.

        Returns:
            Obstacle: The newly spawned obstacle.
        """
        kwargs = {}
        if x is not None:
            kwargs["x"] = x
        if y is not None:
            kwargs["y"] = y
        if speed is not None:
            kwargs["speed"] = speed

        new_obstacle = Obstacle(**kwargs)
        self.obstacles.append(new_obstacle)
        return new_obstacle

    def check_collision(self) -> bool:
        """
        Detect collisions between the player car and any obstacle.
        Uses Pygame Rect collision: player_rect.colliderect(obstacle_rect).

        On collision:
            - Stops the game (sets game_over = True).
            - Preserves final score.

        Returns:
            bool: True if collision occurred, False otherwise.
        """
        player_rect = self.player.rect

        for obstacle in self.obstacles:
            # Specification: Detect collisions using player_rect.colliderect(obstacle_rect)
            if player_rect.colliderect(obstacle.rect):
                self.game_over = True
                return True

        return False

    def update_obstacles(self):
        """
        Update obstacle positions downwards, detect passed obstacles,
        increment score exactly once per passed obstacle, and remove passed obstacles.
        """
        for obstacle in self.obstacles:
            obstacle.update()

            # Detect when an obstacle completely passes the bottom of the screen (rect.y >= 600)
            if not obstacle.passed and obstacle.is_passed():
                obstacle.passed = True
                self.score += 1

        # Remove obstacles after they pass the screen
        self.obstacles = [obs for obs in self.obstacles if not obs.is_passed()]

    def update(self):
        """
        Primary game logic tick.
        If Game Over, updates are suspended.
        """
        if self.game_over:
            return

        # 1. Update road scrolling animation offset
        self.road_scroll_offset = (
            self.road_scroll_offset + ROAD_SCROLL_SPEED
        ) % (LANE_MARKING_HEIGHT + LANE_MARKING_GAP)

        # 2. Spawn obstacles at periodic intervals
        self.spawn_timer += 1
        if self.spawn_timer >= OBSTACLE_SPAWN_INTERVAL:
            self.spawn_timer = 0
            self.spawn_obstacle()

        # 3. Move obstacles downwards and update score for passed obstacles
        self.update_obstacles()

        # 4. Check for collision between player and any obstacle
        self.check_collision()

    def draw(self, surface: pygame.Surface):
        """
        Render all game components: roadside, road, markings, obstacles, player, HUD, and Game Over.

        Args:
            surface (pygame.Surface): The main Pygame display surface.
        """
        if self.headless:
            return

        # 1. Roadside green background
        surface.fill(COLOR_GRASS)

        # Subtle decorative roadside grass texture/curbs
        pygame.draw.rect(surface, COLOR_GRASS_DETAIL, (0, 0, ROAD_LEFT, SCREEN_HEIGHT))
        pygame.draw.rect(surface, COLOR_GRASS_DETAIL, (ROAD_RIGHT, 0, SCREEN_WIDTH - ROAD_RIGHT, SCREEN_HEIGHT))

        # 2. Dark grey road
        pygame.draw.rect(surface, COLOR_ROAD, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))

        # 3. Road boundary lines (Solid white lines at left boundary X=50 and right boundary X=350)
        pygame.draw.line(surface, COLOR_ROAD_BORDER, (ROAD_LEFT, 0), (ROAD_LEFT, SCREEN_HEIGHT), ROAD_BORDER_WIDTH)
        pygame.draw.line(surface, COLOR_ROAD_BORDER, (ROAD_RIGHT, 0), (ROAD_RIGHT, SCREEN_HEIGHT), ROAD_BORDER_WIDTH)

        # 4. Dashed lane markings
        self._draw_lane_markings(surface)

        # 5. Draw all obstacles
        for obstacle in self.obstacles:
            obstacle.draw(surface)

        # 6. Draw player car
        self.player.draw(surface)

        # 7. Draw HUD (In-game score display)
        self._draw_hud(surface)

        # 8. Draw Game Over screen overlay if game is stopped
        if self.game_over:
            self._draw_game_over(surface)

    def _draw_lane_markings(self, surface: pygame.Surface):
        """Draw animated dashed lane markings in the road lanes."""
        cycle = LANE_MARKING_HEIGHT + LANE_MARKING_GAP
        start_y = -cycle + self.road_scroll_offset

        # Dividing lines for 3 lanes: Lane 1 divider at X=150, Lane 2 divider at X=250
        divider_x_positions = [150, 250]

        for x in divider_x_positions:
            y = start_y
            while y < SCREEN_HEIGHT:
                pygame.draw.rect(
                    surface,
                    COLOR_LANE_MARKING,
                    (x - LANE_MARKING_WIDTH // 2, int(y), LANE_MARKING_WIDTH, LANE_MARKING_HEIGHT),
                    border_radius=2,
                )
                y += cycle

    def _draw_hud(self, surface: pygame.Surface):
        """Draw in-game score banner."""
        if not self.font_score:
            self._init_fonts()

        # Score display badge in top-left
        badge_rect = pygame.Rect(10, 10, 130, 36)
        # Background pill
        badge_surf = pygame.Surface((badge_rect.width, badge_rect.height), pygame.SRCALPHA)
        badge_surf.fill((20, 20, 25, 210))
        surface.blit(badge_surf, badge_rect.topleft)
        pygame.draw.rect(surface, (80, 80, 90), badge_rect, width=1, border_radius=6)

        # Score text
        score_surface = self.font_score.render(f"SCORE: {self.score}", True, COLOR_SCORE_LABEL)
        surface.blit(score_surface, (badge_rect.x + 12, badge_rect.y + 6))

    def _draw_game_over(self, surface: pygame.Surface):
        """Draw full Game Over modal overlay with final score and restart prompt."""
        if not self.font_game_over:
            self._init_fonts()

        # Semi-transparent dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        surface.blit(overlay, (0, 0))

        # Game Over dialog card
        card_w, card_h = 320, 220
        card_x = (SCREEN_WIDTH - card_w) // 2
        card_y = (SCREEN_HEIGHT - card_h) // 2 - 20
        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)

        card_surface = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
        card_surface.fill((25, 25, 30, 245))
        surface.blit(card_surface, (card_x, card_y))
        pygame.draw.rect(surface, (220, 50, 50), card_rect, width=2, border_radius=12)

        # Text 1: "GAME OVER"
        go_surf = self.font_game_over.render("GAME OVER", True, COLOR_GAME_OVER)
        go_rect = go_surf.get_rect(center=(SCREEN_WIDTH // 2, card_y + 45))
        surface.blit(go_surf, go_rect)

        # Text 2: "Final Score: X"
        score_surf = self.font_restart.render(f"Final Score: {self.score}", True, COLOR_TEXT)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, card_y + 105))
        surface.blit(score_surf, score_rect)

        # Decorative line
        pygame.draw.line(
            surface,
            (70, 70, 80),
            (card_x + 30, card_y + 135),
            (card_x + card_w - 30, card_y + 135),
            1,
        )

        # Text 3: "Press R to Restart"
        restart_surf = self.font_restart.render("Press R to Restart", True, COLOR_RESTART_HINT)
        restart_rect = restart_surf.get_rect(center=(SCREEN_WIDTH // 2, card_y + 165))
        surface.blit(restart_surf, restart_rect)
