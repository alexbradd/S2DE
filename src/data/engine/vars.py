"""
Module containing shared game variables. Don't import using 'from ... import'
because that will create a local copy of the value, so any change will not be
seen by other modules.

All the values will be initialized by the main function at game init.

- PROGRAM_NAME: name showed in the window title;
- RUNNING: True if the main game loop is iterating, False otherwise;
- SCREEN_SIZE: size of the window in pixels;
- SCREEN: main Surface (see pygame docs for Surface), should only be read;
- FLUSH_COLOR: color with which the SCREEN is filled at refresh;
- CLOCK: the internal clock, should only be read;
- FRAME_RATE: target frame rate at which the program will run, should only be
  read;
- DELTA_TIME: time in seconds between each screen update, should only be read;
- FIRST_SCENE: name of the first scene loaded;
- current_scene: not uppercase because it's not a constant. Reference to the
  currently loaded and active Scene (see scenes module docs for Scene)
- GAME_PATH: Path object (see docs for pathlib for path) containing the path to
  the main game directory (the folder containing main.py).
- SCENE_PATH: Path object (see docs for pathlib for path) containing the path
  to the 'scenes' folder (the 'scenes' folder inside the GAME_PATH)
- CONFIG_PATH: Path object (see docs for pathlib for path) containing the path
  to the 'config.yaml' file (one of the files inside the GAME_PATH)
"""
PROGRAM_NAME = 'SE2DE Game'
RUNNING = True

SCREEN_SIZE = (600, 400)
SCREEN = None
FLUSH_COLOR = (0, 0, 0)

CLOCK = None
FRAME_RATE = 60
DELTA_TIME = 0

FIRST_SCENE = 'title_scene'
current_scene = None

GAME_PATH = None
SCENE_PATH = None
CONFIG_PATH = None
