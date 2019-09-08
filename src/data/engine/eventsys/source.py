"""Module that contains methods for launching events."""
import engine.eventsys.listeners
import copy


def launch(key, listener, data=None):
    """
    Launch an event of type 'key' that the 'listener' class is listening
    to and passes the EventData 'data'.
    """
    # Safe in case variation of listener.listeners[key]
    listeners = copy.copy(listener.listeners[key])
    for l in listeners:
        l.notify(data)


def launch_go(key, gobj_id, data=None):
    """
    Launch a GameObjectEvent of type 'key' that the GameObjectEventListener
    class is listening to targeted to the GameObject with id 'go_id' and
    pass to it the EventData 'data'.
    """
    # Safe in case variation of listener.-.listeners[key]
    listener = engine.eventsys.listeners.GameObjectEventListener
    listeners = copy.copy(listener.listeners[key])
    for l in listeners:
        if l.gobj_id == gobj_id:
            l.notify(data)
