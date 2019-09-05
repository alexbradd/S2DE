"""
Module containing base classes that every Component inherits from. For info
on how a Component or Behaviour works, check out the docs for the respective
classes.
"""


class Component:
    """
    Useful docs to read for more information:
    - engine.gameobject module
    - scene_data_doc file

    Components are objects that add behaviour to GameObjects. For a Component
    to work, it needs to be 'attached' to a GameObject. At a low level, this
    means that the Component gets subscribed to all the GameObject's events and
    gets a reference to the GameObject it is attached to. Likewise, to
    stop a Component from working you need to 'detach' it. At a low level, this
    means that the Component gets unsubscribed from all the GameObject's events
    and loses the reference to the GameObject it is attached to.

    The attachment/detachment to a GameObject is done through GameObject's
    attach() and detach() methods. A Component can be attached to a GameObject
    at any point of his lifecycle (except after death, but I think that's
    obvious).

    Components add their functionality to GameObjects through overriding of the
    methods provided. Each of these methods will be executed at a particular
    point of a GameObject lifecycle:
    - on_create(): executed on GameObject creation. The only components
      capable of catching this event are the one passed into the GameObject's
      constructor.
    - on_spawn(): executed everytime a GameObject gets spawned.
    - on_attach(): executed right after the Component is attached. Should be
      used as a initialization method.
    - on_component_update(): executed everytime a GameObject updates. Since this
      is a function that will run every frame, it is best to put code that
      relies on heavy methods such as find() or get_component() in the
      on_attach() and on_create() method.
    - on_detach(forced): executed right before a Component gets detached.
      The on_detach() method can be 'forced', signalling to the Component that
      it is best not to throw a fuss when detached (like the provided Transform
      component). Forcing a detach is, however, to be used in very dire
      situations.
    - on_despawn(): executed everytime a GameObject is despawned.
    - on_destroy(): executed right before a GameObject is destroyed.

    At GameObject creation, on_attach() will be called before on_create()
    because a component needs to be attached to receive events. Similarly, at
    GameObject deletion, on_destroy() will be called before on_detach() for the
    same reason. This reinforces the fact that on_attach() and on_detach() are
    a Component's true init and deinit methods. The constructor should only be
    used to create the Component's attributes, that will be assigned in the
    on_attach() method.

    At GameObject death the detachment of all Components will always be forced.

    The base Component class should not be used: every Component has to inherit
    from it.
    """

    def __init__(self):
        """Base Component constructor"""
        self.gameobject = None

    def on_create(self):
        """
        Executed on GameObject creation. The only components capable of catching
        this event are the one passed into the GameObject's constructor.
        """
        pass

    def on_spawn(self):
        """Executed everytime a GameObject gets spawned."""
        pass

    def on_attach(self):
        """
        Executed right after the Component is attached. Should be used as an
        initialization method.
        """
        pass

    def on_component_update(self):
        """
        Executed everytime a GameObject updates. Since this is a function that
        will run every frame, it is best to put code that relies on heavy
        methods such as find() or get_component() in the on_attach() and
        on_create() method.
        """
        pass

    def on_detach(self, forced=False):
        """
        Executed right before a Component gets detached. The on_detach() method
        can be 'forced', signalling to the Component that it is best not to
        throw a fuss when detached. Forcing a detach is, however, to be used in
        very dire situations.
        """
        pass

    def on_despawn(self):
        """Executed everytime a GameObject is despawned."""
        pass

    def on_destroy(self):
        """Executed right before a GameObject is destroyed."""
        pass

    def __str__(self):
        """Return a formatted string with all the Component's defining info."""
        return f'Component(type={self.__class__}, gameobject={self.gameobject})'


class Behaviour(Component):
    """
    Useful docs to read for more informations:
    - engine.basecomponents.Component class

    A Behaviour is a specialized Component that has the unique ability to be
    turned on and off.

    Everything is the same as the normal Component except for the update method
    that should be overridden.

    A Behaviour must override the on_behaviour_update() method. Overriding the
    inherited on_component_updated() will effectively turn the Behaviour into a
    normal Component as the method will be called at every update, not obeying
    the enabled flag. Overriding the wrong update method might also risk of
    breaking the correct one.
    """

    def __init__(self, enabled=True):
        """Base Behaviour constructor"""
        super().__init__()
        self.enabled = enabled

    def on_component_update(self):
        """Inherited update method. Should not be touched."""
        if not self.enabled:
            return
        self.on_behaviour_update()

    def on_behaviour_update(self):
        """Executed at every GameObject update if the Behaviour is enabled."""
        pass

    def __str__(self):
        """Return a formatted string with all the Behaviour's defining info."""
        return f'Behaviour(type={self.__class__}, enabled={self.enabled}, ' \
            f'gameobject={self.gameobject})'


class ComponentError(Exception):
    """
    Generic error thrown by a Component or Behaviour.
    Caught in main.main(): call __str__() and then exit with code 1.
    """

    def __init__(self, message, component):
        """
        Constructor for Component Error. Takes the 'message', the string that
        will be displayed, and the 'component' that threw it.
        """
        self.message = message
        self.component = component

    def __str__(self):
        """Return a formatted string containing the error message."""
        return f'Error with component {self.component}: {self.message}'
