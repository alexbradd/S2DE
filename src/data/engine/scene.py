"""
Module containing the Scene class. For info on how a Scene works, check the
docs for the engine.scene.Scene class.
"""
import copy
from collections import OrderedDict

import engine.eventsys as ev


class Scene:
    """
    Useful docs to read for more information:
    - engine.eventsys package
    - engine.gameobject module

    A Scene is basically what the game is displaying. It can be created,
    activated, updated and destroyed. It holds a dictionary that maps each
    loaded GameObject to its corresponding ID.

    Under the hood each scene does nothing but hold a reference to all the
    currently created GameObjects and launch SceneEvents.

    External code should never interact directly with the scene system (calling
    methods or instantiating a new Scene) but should use the SceneLoader and
    the relative events as an interface.

    Life cycle of Scene more in depth:
    - A deactivated Scene is created, but no event is launched.
    - ACTIVATE: Scene is now considered active and can be updated. GameObject
      are guaranteed to exist;
    - UPDATE: Every GameObject in the Scene is updated. Update is called
      directly by the main function at every game loop iteration;
    - DESTROY: Scene is deactivated, ready to be replaced by a new one.

    Every step of the life cycle (except creation) is an event that other 
    objects can listen to. The listener for these events is the 
    SceneEventListener.
    """

    _listener = ev.SceneEventListener
    _gev_listener = ev.GameEventListener

    def __init__(self, name):
        """
        Scene constructor. Create a new deactivated Scene with name 'name'
        and 'gameobjects' gameobjects.
        """
        self.name = name
        self.gameobjects = OrderedDict()
        self.active = False

        # self._gev_listener(ev.EventHandler(self.destroy),
        #                    self._gev_listener.QUIT).listen()
        # Removed because unreachable
        # ev.source.launch(self._listener.CREATE, self._listener)

    def activate(self):
        """
        Set the scene active and launches the ACTIVATE SceneEvent.
        """
        if self.active:
            return
        self.active = True
        ev.source.launch(self._listener.ACTIVATE, self._listener)

    def update(self):
        """
        Called directly by the main function. Launch the UPDATE SceneEvent if
        the Scene is active.
        """
        if not self.active:
            return
        ev.source.launch(self._listener.UPDATE, self._listener)

    def destroy(self):
        """
        Deactivate the scene, unsubscribe from all events and launch the
        DESTROY SceneEvent.
        """
        ev.source.launch(self._listener.DESTROY, self._listener)
        self.active = False
        # self._gev_listener(ev.EventHandler(self.destroy),
        #                    self._gev_listener.QUIT).ignore()

    def get_free_id(self):
        """Get a free id from the scene's GameObject map."""
        if not self.gameobjects:
            return 0
        return list(self.gameobject_ids())[-1] + 1

    def register_gameobject(self, game_object):
        """Register 'game_object' in the scene's GameObject map"""
        new_id = self.get_free_id()
        self.gameobjects[new_id] = game_object
        self._listener(ev.EventHandler(game_object.destroy),
                       self._listener.DESTROY).listen()
        self._listener(ev.EventHandler(game_object.update),
                       self._listener.UPDATE).listen()
        return new_id

    def unregister_gameobject(self, gameobject_id):
        """Unregister 'game_object' from the scene's GameObject map"""
        gobj = self.gameobjects[gameobject_id]
        self._listener(ev.EventHandler(gobj.update),
                       self._listener.UPDATE).ignore()
        self._listener(ev.EventHandler(gobj.destroy),
                       self._listener.DESTROY).ignore()
        del(self.gameobjects[gameobject_id])

    def gameobject_instances(self):
        """Return all registered gameobjects"""
        return self.gameobjects.values()

    def gameobject_ids(self):
        """Return all registered gameobject ids"""
        return self.gameobjects.keys()

    def __str__(self):
        """Return a string containing the name of the Scene and the status."""
        return f'Scene(name={self.name}, active={self.active})'
