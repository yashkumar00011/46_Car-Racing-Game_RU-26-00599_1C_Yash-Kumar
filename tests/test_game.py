"""
Automated unit tests for Car Racing Game (PS No. 46).
Verifies the four required assignment test cases:
  1. Normal Input
  2. Boundary / Minimum Input
  3. Invalid Input
  4. Different Valid Scenario (Passing Obstacle & Collision Detection)
"""

import os
import sys
import unittest

# Ensure SDL video driver runs headless in automated/CI testing environments
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Add project root directory to sys.path so modules can be imported from tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from game import Game
from obstacle import Obstacle
from player import Player
from settings import (
    PLAYER_START_X,
    PLAYER_START_Y,
    MIN_PLAYER_X,
    MAX_PLAYER_X,
    SCREEN_HEIGHT,
)


class TestCarRacingGame(unittest.TestCase):
    """Test suite strictly validating assignment requirements and test cases."""

    def setUp(self):
        """Set up a fresh headless game instance before each test."""
        self.game = Game(headless=True)

    def test_case_1_normal_input(self):
        """
        TEST CASE 1: NORMAL INPUT
        Initial:
            Player X = 180
            Key = RIGHT
        Expected:
            Player X = 190
            Score = 0
            Game running.
        """
        # Initial state setup
        self.game.player.x = 180
        self.game.player._update_rect()
        self.game.score = 0
        self.game.game_over = False

        # Act: Press RIGHT key
        handled = self.game.handle_key(pygame.K_RIGHT)

        # Assertions
        self.assertTrue(handled, "Valid RIGHT key press should be handled.")
        self.assertEqual(
            self.game.player.x, 190, f"Expected Player X to be 190, got {self.game.player.x}"
        )
        self.assertEqual(
            self.game.player.rect.x, 190, f"Expected Player Rect X to be 190, got {self.game.player.rect.x}"
        )
        self.assertEqual(
            self.game.score, 0, f"Expected Score to be 0, got {self.game.score}"
        )
        self.assertFalse(
            self.game.game_over, "Game should remain running (game_over=False)."
        )
        self.assertTrue(
            self.game.is_running, "Game status is_running should be True."
        )

    def test_case_2_boundary_minimum_input(self):
        """
        TEST CASE 2: BOUNDARY / MINIMUM INPUT
        Scenario A:
            Player X = 50
            Key = LEFT
        Expected:
            Player X = 50
            No movement.

        Scenario B:
            Player X = 310
            Key = RIGHT
        Expected:
            Player X = 310
            No movement.
        """
        # ==========================================
        # Scenario A: Left Boundary Check
        # ==========================================
        self.game.player.x = 50
        self.game.player._update_rect()

        # Act: Press LEFT key at boundary X=50
        self.game.handle_key(pygame.K_LEFT)

        # Assertions for Scenario A
        self.assertEqual(
            self.game.player.x,
            50,
            f"Expected Player X to remain 50 (left boundary), got {self.game.player.x}",
        )
        self.assertEqual(
            self.game.player.rect.x,
            50,
            f"Expected Player Rect X to remain 50, got {self.game.player.rect.x}",
        )

        # ==========================================
        # Scenario B: Right Boundary Check
        # ==========================================
        self.game.player.x = 310
        self.game.player._update_rect()

        # Act: Press RIGHT key at boundary X=310
        self.game.handle_key(pygame.K_RIGHT)

        # Assertions for Scenario B
        self.assertEqual(
            self.game.player.x,
            310,
            f"Expected Player X to remain 310 (right boundary), got {self.game.player.x}",
        )
        self.assertEqual(
            self.game.player.rect.x,
            310,
            f"Expected Player Rect X to remain 310, got {self.game.player.rect.x}",
        )

    def test_case_3_invalid_input(self):
        """
        TEST CASE 3: INVALID INPUT
        Initial:
            Player X = 180
            Key = SPACE
        Expected:
            Key ignored.
            Player X = 180
            Game running.
        """
        # Initial state setup
        self.game.player.x = 180
        self.game.player._update_rect()
        initial_score = self.game.score

        # Act: Press SPACE key (invalid movement key)
        handled = self.game.handle_key(pygame.K_SPACE)

        # Assertions
        self.assertFalse(
            handled, "Invalid key (SPACE) should return False (ignored)."
        )
        self.assertEqual(
            self.game.player.x,
            180,
            f"Expected Player X to remain 180 when SPACE is pressed, got {self.game.player.x}",
        )
        self.assertEqual(
            self.game.player.rect.x,
            180,
            f"Expected Player Rect X to remain 180, got {self.game.player.rect.x}",
        )
        self.assertEqual(
            self.game.score, initial_score, "Score should not change on invalid key."
        )
        self.assertFalse(
            self.game.game_over, "Game should remain running."
        )
        self.assertTrue(
            self.game.is_running, "Game is_running should be True."
        )

    def test_case_4_different_valid_scenario(self):
        """
        TEST CASE 4: DIFFERENT VALID SCENARIO
        Scenario A:
            Starting score = 3
            Obstacle position = (300, 600)
        Expected:
            Obstacle passed.
            Score = 4.

        Scenario B:
            Player position = (180, 500)
            Obstacle position = (200, 520)
        Expected:
            Collision detected.
            Game Over.
            Final score = 4.
        """
        # ==========================================
        # Scenario A: Passing Obstacle & Score Update
        # ==========================================
        self.game.score = 3
        # Spawn obstacle at exactly (300, 600)
        obstacle_a = Obstacle(x=300, y=600)
        self.game.obstacles = [obstacle_a]

        # Verify obstacle position
        self.assertEqual(obstacle_a.x, 300)
        self.assertEqual(obstacle_a.y, 600)
        self.assertEqual(obstacle_a.rect.topleft, (300, 600))

        # Check passed condition
        self.assertTrue(
            obstacle_a.is_passed(),
            "Obstacle at Y=600 should be detected as passed (Y >= SCREEN_HEIGHT).",
        )

        # Trigger obstacle update (moves, counts score, removes passed obstacles)
        self.game.update_obstacles()

        # Assertions for Scenario A
        self.assertEqual(
            self.game.score,
            4,
            f"Expected Score to increment from 3 to 4, got {self.game.score}",
        )
        self.assertNotIn(
            obstacle_a,
            self.game.obstacles,
            "Passed obstacle should be removed from active obstacles list.",
        )

        # ==========================================
        # Scenario B: Collision Detection & Game Over
        # ==========================================
        # Player position = (180, 500)
        self.game.player.x = 180
        self.game.player.y = 500
        self.game.player._update_rect()

        # Obstacle position = (200, 520)
        # Player Rect: (180, 500, 40, 80) -> X: [180, 220], Y: [500, 580]
        # Obstacle Rect: (200, 520, 40, 80) -> X: [200, 240], Y: [520, 600]
        # Overlapping intersection: X: [200, 220], Y: [520, 580]
        obstacle_b = Obstacle(x=200, y=520)
        self.game.obstacles = [obstacle_b]

        # Verify direct Pygame Rect colliderect detection
        collided = self.game.player.rect.colliderect(obstacle_b.rect)
        self.assertTrue(
            collided,
            "player_rect.colliderect(obstacle_rect) must detect collision.",
        )

        # Trigger game collision check
        collision_result = self.game.check_collision()

        # Assertions for Scenario B
        self.assertTrue(collision_result, "check_collision() must return True.")
        self.assertTrue(self.game.game_over, "Game Over must be True on collision.")
        self.assertEqual(
            self.game.score,
            4,
            f"Final score must be preserved as 4, got {self.game.score}",
        )

    def test_additional_restart_functionality(self):
        """Verify that pressing 'R' resets the player, score, obstacles, and restarts."""
        # Put game into Game Over state with modified score and obstacle
        self.game.score = 7
        self.game.game_over = True
        self.game.player.x = 220
        self.game.player._update_rect()
        self.game.obstacles = [Obstacle(x=200, y=300)]

        # Act: Press 'R' to restart
        handled = self.game.handle_key(pygame.K_r)

        # Assertions
        self.assertTrue(handled, "Pressing R should be handled during Game Over.")
        self.assertFalse(self.game.game_over, "game_over should be reset to False.")
        self.assertEqual(self.game.score, 0, "Score should reset to 0.")
        self.assertEqual(self.game.player.x, PLAYER_START_X, "Player X should reset to 180.")
        self.assertEqual(self.game.player.y, PLAYER_START_Y, "Player Y should reset to 500.")
        self.assertEqual(len(self.game.obstacles), 0, "Obstacles list should be cleared.")


def run_formatted_tests():
    """Runs tests and outputs a structured verification report for the university assignment."""
    print("=" * 65)
    print("  CAR RACING GAME (PS No. 46) - AUTOMATED VERIFICATION REPORT")
    print("=" * 65)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestCarRacingGame)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 65)
    if result.wasSuccessful():
        print("  RESULT: ALL ASSIGNMENT TEST CASES PASSED SUCCESSFULLY (4/4)")
    else:
        print(f"  RESULT: FAILURES ENCOUNTERED ({len(result.failures)} Failures, {len(result.errors)} Errors)")
    print("=" * 65)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_formatted_tests())
