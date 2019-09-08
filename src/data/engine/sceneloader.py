"""
Useful docs to read for more information:
 - engine.gameobject module

Module containing functions responsible for loading and activating new Scenes
from disk.

Loaded scenes are cached in an OrderedDict with size '_cache_size'. The scene
data is stored from older (first in dict) to newer (last in dict).

Scene data is loaded using a YAML loader. The "typ='unsafe'" enables custom
object tags (see ruamel.yaml docs). These tags are needed by the
to properly parse GameObject Component data (see gameobject module docs)
"""
from collections import OrderedDict
import ruamel.yaml

from engine.scene import Scene
from engine.gameobject import GameObject
import engine.vars as gvars


class SceneCache:
    """Static class that handles the scene cache"""

    cache = OrderedDict()
    cache_size = 10

    @classmethod
    def extract(cls, name):
        """
        Get a copy of the data from cache, move it to the last place and return
        it.
        """
        data = cls.cache[name]
        cls.move_to_end(name)
        return data

    @classmethod
    def move_to_end(cls, name):
        """Move scene data to the last place in the dictionary"""
        cls.cache.move_to_end(name)

    @classmethod
    def add(cls, name, data):
        """Add a copy of 'data' with key 'name' to the cache and trim it"""
        cls.cache[name] = data
        cls.trim_cache()

    @classmethod
    def trim_cache(cls):
        """
        Remove every item from older to newer until cache is of 'cache_size'
        """
        while True:
            if len(cls.cache) > cls.cache_size:
                cls.cache.popitem(last=False)
            else:
                break


def load_scene(name):
    """
    Load data from cache/disk, parse it and create a new scene deactivated
    empty scene and reference it . Then parse all the gameobjects using
    GameObjectLoader (see the gameobjects docs), add them. Finally activate
    the scene and spawn the GameObjects.

    The name of the scene is the filename of the scene data file without
    the extension.
    """
    destroy_current()
    gvars.current_scene = Scene(name)
    gos = _load_gameobjects(load_raw_data(name))
    _spawn_gameobjects(gos)
    gvars.current_scene.activate()


def load_raw_data(name):
    """
    Load the raw scene data. If the scene exists in the '_cache' dict the
    data stored inside the cache is used, else new data is loaded from disk
    and stored in '_cache'
    """
    if name in SceneCache.cache:
        return SceneCache.extract(name)
    try:
        data = ruamel.yaml.YAML(typ='unsafe')\
            .load(gvars.SCENE_PATH.joinpath(f'{name}.yaml'))
    except ruamel.yaml.YAMLError:
        raise InvalidSceneData("Malformed YAML file.")
    SceneCache.add(name, data)
    return data


def _load_gameobjects(raw_data):
    """Return the list of GameObjects read from raw_data"""
    return [parse_gameobject(raw_go) for raw_go in raw_data]


def _spawn_gameobjects(gos):
    """For each GameObject in the current scene, call the spawn method"""
    for go_data in gos:
        if go_data[1]:
            go_data[0].spawn()


def destroy_current():
    """Destroy the currently loaded Scene."""
    if gvars.current_scene is not None:
        gvars.current_scene.destroy()
    gvars.current_scene = None


def parse_gameobject(raw_go_data):
    """Parse GameObject from 'raw_go_data'"""
    go_name = _parse_name(raw_go_data)
    go_spawned = _parse_spawned(raw_go_data)
    go_comps = _parse_components(raw_go_data)
    return GameObject(go_name, go_comps), go_spawned


def _parse_name(raw_go_data):
    """Parse the 'name' attribute from 'raw_go_data'"""
    name_key = 'name'
    try:
        name = raw_go_data[name_key]
    except KeyError:
        raise InvalidSceneData(f'{name_key} is not present in a GameObject')
    if not isinstance(name, str):
        raise InvalidSceneData(f'{name_key} attribute is not a string')
    return name


def _parse_spawned(raw_go_data):
    """Parse the 'spawned' attribute from 'raw_go_data'"""
    spawned_key = 'spawned'
    try:
        spawned = raw_go_data[spawned_key]
    except KeyError:
        raise InvalidSceneData(f'{spawned_key} is not present in a GameObject')
    if not isinstance(spawned, bool):
        raise InvalidSceneData(f'"{spawned_key}" attribute is not a bool')
    return spawned


def _parse_components(raw_go_data):
    """Parse every Component from 'raw_go_data' and return it into a list"""
    comps_key = 'components'
    try:
        return [_parse_component(c_data) for c_data in raw_go_data[comps_key]]
    except KeyError:
        raise InvalidSceneData(f'{comps_key} is not present in a GameObject')
    except (TypeError, AttributeError):
        raise InvalidSceneData(f'{comps_key} does not contain the proper '
                               'value')


def _parse_component(raw_comp_data):
    """Parse a Component object from 'raw_comp_data'"""
    type_key = 'type'
    try:
        typ = raw_comp_data.pop(type_key)
        return typ(**raw_comp_data)
    except KeyError:
        raise InvalidSceneData("Component is missing the 'type' key")


class InvalidSceneData(Exception):
    """
    Exception for errors occurring while parsing scene data form YAML.

    Caught in main.main(): call __str__() and then exit with errno 1.
    """

    def __init__(self, message, scene_name=""):
        """
        Constructor for InvalidSceneData. It takes 'message', a string that is
        the error message, a optionally the name 'scene_name' whose data caused
        the error.
        """
        super().__init__()
        self.message = message
        self.scene_name = scene_name

    def __str__(self):
        """
        Return a formatted string containing the error message. If 'scene_name'
        is an empty string, then the current scene's name is used.
        """
        if self.scene_name:
            return f'Invalid data in scene file {self.scene_name}.yaml: ' \
                f'{self.message}'
        return f'Invalid data in scene file {gvars.current_scene.name}.yaml' \
            f': {self.message}'
