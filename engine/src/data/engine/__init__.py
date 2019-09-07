"""
Package containing all the logic to make the game work. This includes:
- global variables (engine.vars);
- event system (engine.eventsys);
- scene system (engine.scene);
- scene loading (engine.scene_loader);
- gameobject system (engine.gameobject)
- component system (engine.basecomponents)

For more in depth documentation, read the docs for each of the
module/subpackage.

For easier access, all important classes have been exposed and won't require
typing their module. For example, to use the GameObject class you can write
'engine.GameObject' instead of 'engine.gameobject.GameObject'
"""

# Modules
import engine.vars
import engine.sceneloader

# Subpackages
import engine.eventsys

# Expose useful classes
from engine.sceneloader import InvalidSceneData
from engine.basecomponents import ComponentError
from engine.basecomponents import Component
from engine.basecomponents import Behaviour
from engine.gameobject import GameObject
from engine.scene import Scene
