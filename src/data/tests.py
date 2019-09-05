"""
Module containing some helper methods that help testing the engine without
the main loop running.

Left kind of barren because this is a module that most likely the user will
expand to add his own tests.
"""
import engine
import components
# import behaviours


def load_dummy_env():
    """
    Loads a dummy environment containing one Scene called 'Dummy' with one
    spawned GameObject called 'Test1'
    """
    engine.vars.current_scene = engine.scene.Scene('Dummy')
    create_dummy_go('Test1', True)


def create_dummy_go(name, spawn):
    """
    Create a dummy GameObject with name 'name'. This GameObject will have
    only a Transform and the 'spawn' bool decides whether it will be spawned or
    not.
    """
    go = engine.gameobject.GameObject(name, [components.Transform()])
    if spawn:
        go.spawn()
