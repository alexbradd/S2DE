"""Module containing the various listener objects."""
from engine.eventsys.handling import EventHandler


class Listener:
    """
    Base Listener object. It should never be used. Use one of its subclasses
    instead.

    There cannot be more than one Listener with the same EventHandler listening
    to the same source. As a matter of fact, at Listener creation, if another
    Listener with the same EventHandler (for more detailed info on EventHandler
    equality, see docs for the EventHandler class) is found listening to the
    same source, that one is returned instead of creating a new one. This
    behaviour can be overridden by passing the 'force' flag, but is not
    recommended.

    Every Listener contains a static dictionary that maps a list of Listeners to
    the ID of an event. When a Listener starts listening to the event it is
    registered in the aforementioned dictionary and will be visible to the
    sources. When the same Listener will stop listening, it will be removed from
    the list.
    """

    listeners = {}

    def __init__(self, event_handler, type_id, force=False):
        """
        Init for the Listener class. It takes in the 'event_handler'
        object and the 'type_id' of the event to which the Listener will listen.
        """
        self.event_handler = event_handler
        self.type_id = type_id
        self.forced = force

    def __new__(cls, event_handler, type_id, force=False):
        """
        To avoid having multiple Listeners with the same EventHandler with
        the same source_id, the function searches for a Listener with the
        same EventHandler in the listeners dictionary using source_id as the
        key.
        If an equivalent Listener is not found, then a new one is created.

        This behaviour can behaviour can be overridden by passing the force
        flag.
        """
        if isinstance(event_handler, EventHandler):
            if not force:
                listener = cls.find_listener(event_handler, type_id)
                if listener is None:
                    return object.__new__(cls)
                return listener
            return object.__new__(cls)
        raise TypeError(f'Passed argument {event_handler} is not an ' +
                        'EventHandler.')

    def notify(self, event_data):
        """
        Execute the callback stored in 'self.event_handler' and pass to it
        'event_data'
        """
        self.event_handler.execute(event_data)

    def listen(self):
        """Listen for the event of type with id 'self.type_id'"""
        listener = self.find_listener(self.event_handler, self.type_id)
        if listener is None or self.forced:
            self.__class__.listeners[self.type_id].append(self)

    def ignore(self):
        """Stop listening to the event of type with id 'self.type_id'"""
        # Passing the reference to make the code more readable
        listening_to_source = self.__class__.listeners[self.type_id]
        for i, listener in enumerate(listening_to_source):
            if listener == self:
                del(listening_to_source[i])

    @classmethod
    def find_listener(cls, event_handler, type_id):
        """
        Get a Listener instance that has the same 'event_handler' from all the
        listeners listening to event with 'type_id'.
        If no Listener is found, return None.
        """
        source = cls.listeners[type_id]
        for listener in source:  # loop listeners
            if listener.event_handler == event_handler:
                return listener
        return None


class GameEventListener(Listener):
    """Listener that listens to GameEvents."""

    CLICKDOWN = 0
    CLICKUP = 1
    MOUSEMOTION = 2

    KEYDOWN = 3
    KEYUP = 4

    ACTIVE = 5
    QUIT = 6

    listeners = {CLICKDOWN: [],
                 CLICKUP: [],
                 MOUSEMOTION: [],
                 KEYDOWN: [],
                 KEYUP: [],
                 ACTIVE: [],
                 QUIT: []}


class SceneEventListener(Listener):
    """Listener that listens to SceneEvents."""

    # CREATE = 0  Removed because was unreachable
    ACTIVATE = 1
    UPDATE = 2
    DESTROY = 3

    listeners = { # CREATE: [],
                 ACTIVATE: [],
                 UPDATE: [],
                 DESTROY: []}


class GameObjectEventListener(Listener):
    """
    Listener that listens to GameObjectEvents.

    The GameObjectEventListener, due to the special nature of the
    GameObjectEvent, needs the GameObject ID of the GameObject that is tied to.
    This makes each GameObjectEvent visible only to listeners that have the same
    GameObject id as the source, not sharing said event with all listeners.
    """

    CREATE = 0
    SPAWN = 1
    UPDATE = 3
    DESPAWN = 5
    DESTROY = 6

    listeners = {CREATE: [],
                 SPAWN: [],
                 UPDATE: [],
                 DESPAWN: [],
                 DESTROY: []}

    def __init__(self, event_handler, type_id, gobj_id, force=False):
        super().__init__(event_handler, type_id, force)
        self.gobj_id = gobj_id

    def __new__(cls, event_handler, type_id, gobj_id, force=False):
        return super().__new__(cls, event_handler, type_id, force)
