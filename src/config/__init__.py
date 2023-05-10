import os

WINDOW_WIDTH = os.environ.get('WINDOW_WIDTH', 1250)
WINDOW_HEIGHT = os.environ.get('WINDOW_HEIGHT', 720)


MAP_ASSETS_DIR = os.path.join(os.path.dirname(__file__), '../assets/maps')
SPRITES_DIR = os.path.join(os.path.dirname(__file__), '../assets/sprites')