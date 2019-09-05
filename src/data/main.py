"""
Main module of the application. If the file is executed directly the main
function is called, else it has to be called manually.
"""
from ruamel.yaml import YAML
import pygame
import pathlib
import traceback

import engine


def main():
    """
    Main function. Firstly init the shared variables and then load the first
    scene. Then start the main game loop.

    In the main game loop first flushes the screen, then GameEvents are
    launched and finally the screen and clock are updated.
    """
    # Init pygame
    pygame.init()
    init(__file__)
    load_config()
    pygame.display.set_caption(engine.vars.PROGRAM_NAME)
    engine.sceneloader.load_scene(engine.vars.FIRST_SCENE)
    # Main loop
    while engine.vars.RUNNING:
        call_event_loop()
        update()
    quit()


def flush_screen(screen, color):
    """Fill the 'screen' Surface with a solid color 'color'."""
    screen.fill(color)


def init(main_path):
    """Init global paths, variables and other stuff"""
    engine.vars.GAME_PATH = pathlib.Path(main_path.replace('main.py', ''))
    engine.vars.CONFIG_PATH = engine.vars.GAME_PATH.joinpath('config.yaml')
    engine.vars.SCENE_PATH = engine.vars.GAME_PATH.joinpath('scenes')
    engine.vars.SCREEN = pygame.display.set_mode(engine.vars.SCREEN_SIZE)
    engine.vars.CLOCK = pygame.time.Clock()
    
    del_eh = engine.eventsys.EventHandler(engine.sceneloader.destroy_current)
    type_id = engine.eventsys.GameEventListener.QUIT
    engine.eventsys.GameEventListener(del_eh, type_id).listen()


def load_config():
    """
    Load engine.vars values from 'config.yaml'. If the value is not defined,
    the default values are used instead.

    For info about the variables that can be modified see the docs inside the
    config.yaml file.
    """
    data = YAML().load(engine.vars.CONFIG_PATH)
    if data is None:
        return
    for key in data.keys():
        if key == 'program_name':
            engine.vars.PROGRAM_NAME = data[key]
        elif key == 'screen_size':
            engine.vars.SCREEN_SIZE = data[key]
        elif key == 'flush_color':
            engine.vars.FLUSH_COLOR = data[key]
        elif key == 'frame_rate':
            engine.vars.FRAME_RATE = data[key]
        elif key == 'first_scene':
            engine.vars.FIRST_SCENE = data[key]
        else:
            raise ValueError(f'Invalid key {key} in config file')


def call_event_loop():
    """
    The GameEvent loop: goes through all the events launched by pygame
    and relaunches them as GameEvents
    """
    for event in pygame.event.get():
        data = None
        key = None
        if event.type == pygame.KEYDOWN:
            key = engine.eventsys.GameEventListener.KEYDOWN
            data = engine.eventsys.EventData(unicode=event.unicode,
                                             key=event.key,
                                             mod=event.mod)
        if event.type == pygame.KEYUP:
            key = engine.eventsys.GameEventListener.KEYUP
            data = engine.eventsys.EventData(key=event.key, mod=event.mod)
        if event.type == pygame.MOUSEBUTTONDOWN:
            key = engine.eventsys.GameEventListener.CLICKDOWN
            data = engine.eventsys.EventData(pos=event.pos,
                                             button=event.button)
        if event.type == pygame.MOUSEBUTTONUP:
            key = engine.eventsys.GameEventListener.CLICKUP
            data = engine.eventsys.EventData(pos=event.pos,
                                             button=event.button)
        if event.type == pygame.MOUSEMOTION:
            key = engine.eventsys.GameEventListener.MOUSEMOTION
            data = engine.eventsys.EventData(pos=event.pos, rel=event.rel,
                                             buttons=event.buttons)
        if event.type == pygame.ACTIVEEVENT:
            key = engine.eventsys.GameEventListener.ACTIVE
            data = engine.eventsys.EventData(gain=event.gain,
                                             state=event.state)
        if event.type == pygame.QUIT:
            key = engine.eventsys.GameEventListener.QUIT
            engine.vars.RUNNING = False
        if key is not None:
            engine.eventsys.source.launch(key,
                                          engine.eventsys.GameEventListener,
                                          data)


def update():
    """Updates the contents of the window if a scene exists"""
    flush_screen(engine.vars.SCREEN, engine.vars.FLUSH_COLOR)
    try:
        engine.vars.current_scene.update()
        pygame.display.update()
        engine.vars.DELTA_TIME = engine.vars.CLOCK.get_time() / 1000
        engine.vars.CLOCK.tick(engine.vars.FRAME_RATE)
    except AttributeError:
        return
    
    
def quit():
    """Clean stuff up before exiting"""
    del_eh = engine.eventsys.EventHandler(engine.sceneloader.destroy_current)
    type_id = engine.eventsys.GameEventListener.QUIT
    engine.eventsys.GameEventListener(del_eh, type_id).ignore()
    pygame.quit()

# If executed directly, call the main function
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(130)
    except SystemExit:
        exit(0)
    except engine.InvalidSceneData as e:
        print(str(e))
        exit(1)
    except engine.ComponentError as e:
        print(str(e))
        exit(1)
    except Exception:
        print(f'An internal error has occurred! Here is the stacktrace for '
              f'the error. Use this to get help:\n\n {traceback.format_exc()}')
        exit(1)
