"""
Settings and configuration constants for Car Racing Game.
Project Number: PS No. 46
Project Title: Car Racing Game
Language: Python 3
Library: Pygame
"""

# ==========================================
# 1. WINDOW AND DISPLAY SETTINGS
# ==========================================
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
WINDOW_TITLE = "Car Racing Game"

# ==========================================
# 2. ROAD SETTINGS
# ==========================================
# Left boundary at X=50, right boundary at X=350 (Width: 300px)
ROAD_LEFT = 50
ROAD_RIGHT = 350
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT  # 300 pixels
ROAD_BORDER_WIDTH = 4
ROAD_SCROLL_SPEED = 5

# Lane markings (dashed center lines)
LANE_MARKING_WIDTH = 6
LANE_MARKING_HEIGHT = 30
LANE_MARKING_GAP = 20

# ==========================================
# 3. PLAYER CAR SETTINGS
# ==========================================
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 80
PLAYER_START_X = 180
PLAYER_START_Y = 500
PLAYER_MOVE_STEP = 10

# Boundaries for the player's left coordinate
# Road spans X=50 to X=350. With player width=40:
# Min X = 50 (left edge touches road left boundary)
# Max X = 310 (right edge: 310 + 40 = 350 touches road right boundary)
MIN_PLAYER_X = 50
MAX_PLAYER_X = 310

# ==========================================
# 4. OBSTACLE SETTINGS
# ==========================================
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 80
MIN_OBSTACLE_X = 50
MAX_OBSTACLE_X = 310
DEFAULT_OBSTACLE_SPEED = 5
OBSTACLE_SPAWN_INTERVAL = 70  # Frames between obstacle spawns

# ==========================================
# 5. COLOR PALETTE
# ==========================================
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRASS = (46, 125, 50)          # Green roadside background
COLOR_GRASS_DETAIL = (56, 142, 60)   # Secondary grass detail
COLOR_ROAD = (45, 45, 48)            # Dark grey road
COLOR_ROAD_BORDER = (240, 240, 240)  # White solid road boundary lines
COLOR_LANE_MARKING = (255, 255, 255) # White dashed lane markings
COLOR_TEXT = (255, 255, 255)
COLOR_SCORE_LABEL = (255, 215, 0)    # Gold
COLOR_GAME_OVER = (235, 50, 50)      # Bright Red
COLOR_RESTART_HINT = (255, 255, 255) # White
COLOR_OVERLAY = (0, 0, 0, 190)       # Semi-transparent dark overlay

# Car Colors
COLOR_PLAYER = (220, 38, 38)         # Racing Red
COLOR_CAR_WINDOW = (30, 41, 59)      # Dark tinted windshield
COLOR_CAR_LIGHTS_FRONT = (254, 240, 138)  # Headlights (Warm Yellow)
COLOR_CAR_LIGHTS_BACK = (185, 28, 28)     # Taillights (Dark Red)
COLOR_CAR_TIRE = (20, 20, 20)        # Black tires

# Varied enemy car colors for visual appeal
OBSTACLE_COLORS = [
    (37, 99, 235),   # Blue
    (234, 179, 8),   # Yellow
    (249, 115, 22),  # Orange
    (147, 51, 234),  # Purple
    (13, 148, 136),  # Teal / Cyan
    (225, 29, 72),   # Rose
]
