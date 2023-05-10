import os

WINDOW_WIDTH = os.environ.get('WINDOW_WIDTH', 800)
WINDOW_HEIGHT = os.environ.get('WINDOW_HEIGHT', 600)


ASSETS_DIR = os.path.join(os.path.dirname(__file__), '../assets/maps')