"""
Module containing the GameObject class. For info on how a GameObject works,
check the docs for the engine.gameobject.GameObject class
"""
import engine.eventsys as evs
import engine.vars as gvars


class GameObject:
    """
    Useful docs to read for more information:
    - scene_data_doc file in 'scenes' folder
    - engine.eventsys package

    Everything in a Scene is a GameObject. A GameObject, in its essence, is
    nothing more than a list of Components that define its behaviour. Those
    Components are 'attached' to it.

    The main attributes of a GameObject are its name, it gobj_id and its
    Components.

    Every GameObject has a lifecycle and the various steps of this cycle are
    subscriptable events (the listener is the GameObjectEventListener). The
    Component system, for example, uses them to provide an easy way to add
    functionality to every step of a GameObject's lifecycle.

    The lifecycle of a GameObject:
    - CREATE: The GameObject is created and is registered in the current Scene.
      It is not yet spawned. The existence of the GameObject's components is
      guaranteed, but not that of the other GameObject in the Scene.
    - SPAWN: The GameObject begins to update itself every time the Scene
      updates. The existence of all GameObjects and their components is
      guaranteed.
    - UPDATE: The GameObject updates itself every Scene update.
    - DESPAWN: The GameObject stops updating itself, but is not yet destroyed.
      The existence of all GameObjects and their components is guaranteed.
    - DESTROY: Every Component is ripped out and the GameObject is deleted from
      the current scene.
    The SPAWN and DESPAWN steps may occur multiple times in a GameObject's
    lifecycle.

    Components can be attached at scene load via the yaml files in the 'scenes'
    folder. They can also be added and removed dynamically via
    attach() and detach().
    """

    _listener = evs.GameObjectEventListener
    _scene_listener = evs.SceneEventListener

    def __init__(self, name=None, components=None):
        """
        Constructor for GameObject. It initializes base attributes (name and
        id) then attaches all Components and launches the CREATE event.
        """
        self.gobj_id = gvars.current_scene.register_gameobject(self)
        self.name = name
        self.spawned = False
        self.components = []
        self.attach(components)
        evs.source.launch_go(self._listener.CREATE, self.gobj_id)

    def spawn(self):
        """Spawn the GameObject and launch the SPAWN event"""
        # Removed in favour of a boolean check to increase performance
        # self._scene_listener(evs.EventHandler(self.update),
        #                      self._scene_listener.UPDATE).listen()
        self.spawned = True
        evs.source.launch_go(self._listener.SPAWN, self.gobj_id)

    def update(self):
        """Update the GameObject by launching the UPDATE event"""
        if self.spawned:
            evs.source.launch_go(self._listener.UPDATE, self.gobj_id)

    def despawn(self):
        """Despawn the GameObject and launch the DESPAWN event"""
        # Removed in favour of a boolean check to increase performance
        # self._scene_listener(evs.EventHandler(self.update),
        #                      self._scene_listener.UPDATE).stop_listening()
        self.spawned = False
        evs.source.launch_go(self._listener.DESPAWN, self.gobj_id)

    def destroy(self):
        """
        Launch DESTROY event, purge every Component and unregister from current
        scene
        """
        evs.source.launch_go(self._listener.DESTROY, self.gobj_id)
        self._detach_all()
        gvars.current_scene.unregister_gameobject(self.gobj_id)

    def attach(self, to_attach):
        """
        Attach a list or a single component to the GameObject
        """
        if isinstance(to_attach, list):
            self.components.extend(to_attach)
            for component in to_attach:
                self._attach_component(component)
        else:
            self.components.append(to_attach)
            self._attach_component(to_attach)

    def _attach_component(self, component):
        """
        Internal use: subscribe component to all the events and run on_add()
        """
        if component.gameobject:  # Already attached
            return
        self._listener(evs.EventHandler(component.on_create),
                       self._listener.CREATE, self.gobj_id).listen()
        self._listener(evs.EventHandler(component.on_spawn),
                       self._listener.SPAWN, self.gobj_id).listen()
        self._listener(evs.EventHandler(component.on_component_update),
                       self._listener.UPDATE, self.gobj_id).listen()
        self._listener(evs.EventHandler(component.on_despawn),
                       self._listener.DESPAWN, self.gobj_id).listen()
        self._listener(evs.EventHandler(component.on_destroy),
                       self._listener.DESTROY, self.gobj_id).listen()
        component.gameobject = self
        component.on_attach()

    def detach(self, to_detach, all_instances=False):
        """
        Detach the first instance of Components of type 'to_detach'.

        If 'all_instances' is True, remove every instance
        """
        for component in self.components:
            if isinstance(component, to_detach):
                self._detach_component(component)
                self.components.remove(component)
                if not all_instances:
                    return

    def _detach_all(self):
        """Internal use: Force detachment of every component"""
        for component in self.components:
            self._detach_component(component, force=True)
        self.components.clear()

    def _detach_component(self, component, force=False):
        """
        Internal use: unsubscribe component from all the events and run
        on_remove()
        """
        self._listener(evs.EventHandler(component.on_create),
                       self._listener.CREATE, self.gobj_id).ignore()
        self._listener(evs.EventHandler(component.on_spawn),
                       self._listener.SPAWN, self.gobj_id).ignore()
        self._listener(evs.EventHandler(component.on_component_update),
                       self._listener.UPDATE, self.gobj_id).ignore()
        self._listener(evs.EventHandler(component.on_despawn),
                       self._listener.DESPAWN, self.gobj_id).ignore()
        self._listener(evs.EventHandler(component.on_destroy),
                       self._listener.DESTROY, self.gobj_id).ignore()
        component.on_detach(force)
        component.gameobject = None

    def get_component(self, typ, all_instances=False):
        """
        Return the first instance of Component of type 'typ' attached to the
        GameObject.
        Return None if nothing is found.

        If 'all_instances' is True, return a list of every Component of type
        'typ'
        """
        comps = []
        for comp in self.components:
            if isinstance(comp, typ):
                if all_instances:
                    comps.append(comp)
                else:
                    return comp
        if not comps:
            return None
        return comps

    @classmethod
    def find(cls, search, all_instances=False):
        """
        Search the current scene for the GameObject with name or id 'search'
        and return it. Return None if nothing is found.

        If 'all_instances' is True, return a list of every GameObject that
        matches the criteria
        """
        gobjs = []
        if isinstance(search, str):
            for g_obj in gvars.current_scene.gameobject_instances():
                if g_obj.name == search:
                    if all_instances:
                        gobjs.append(g_obj)
                    else:
                        return g_obj
        else:
            for go_id in gvars.current_scene.gameobject_ids():
                if go_id == search:
                    if all_instances:
                        gobjs.append(gvars.current_scene.gameobjects[go_id])
                    else:
                        return gvars.current_scene.gameobjects[go_id]
        if not gobjs:
            return None
        return gobjs

    def __str__(self):
        """Return a string containing id and name of the GameObject."""
        return f'GameObject(ID={self.gobj_id}, name={self.name})'
