import os
import math

WINDOW_WIDTH = os.environ.get("WINDOW_WIDTH", 1250)
WINDOW_HEIGHT = os.environ.get("WINDOW_HEIGHT", 720)


MAP_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "../assets/maps")
SPRITES_DIR = os.path.join(os.path.dirname(__file__), "../assets/sprites")

CELL_SIZE = 8

GRID_X_OFFSET = 700
GRID_Y_OFFSET = 200

TILE_WIDTH = 24
TILE_HEIGHT = 16

CONVERSION_FACTOR_X = 0.5
CONVERSION_FACTOR_Y = math.sqrt(3) / 2
