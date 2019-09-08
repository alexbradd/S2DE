"""
Module that contains the EventHandler and EventData class.
"""
import copy


class EventHandler:
    """
    An EventHandler is a class that holds a callback (a reference to a
    function) and the arguments (args or kwargs) that will be passed. The
    function inside the EventHandler can be then executed.

    EventHandlers are used by Listeners to execute functions when an event
    is launched.

    NOTE: Two EventHandlers are equal when the callback (the function) and its
    arguments are equal. So two EventHandlers pointing to the same function
    of two different instances of an object are different, but two
    EventHandlers pointing to the same function of the same instance of an
    object are equal.
    """

    def __init__(self, callback, *args, **kwargs):
        """
        Constructor for EventHandler. It takes a function 'callback' and the
        arguments to pass to it in form of args and kwargs. The self parameter
        should not be added to the arguments of the function.
        """
        self.callback = callback
        self.args = copy.deepcopy(args)
        self.kwargs = copy.deepcopy(kwargs)

    def execute(self, event_data):
        """
        Execute the callback.

        If 'event_data' is None, it is not passed: only the args and kwargs
        will be passed to the callback.
        """
        if event_data is None:
            self.callback(*self.args, **self.kwargs)
        else:
            self.callback(event_data, *self.args, **self.kwargs)

    def __eq__(self, other):
        """
        Return true if callback and passed parameters are the same.
        """
        callback_eq = self.callback == other.callback
        args_eq = self.args == other.args
        kwargs_eq = self.kwargs == other.kwargs
        return callback_eq and args_eq and kwargs_eq

    def __str__(self):
        """
        Return a formatted string with the callback and its arguments.
        """
        return f'EventHandler({self.callback}, {self.args}, {self.kwargs})'


class EventData:
    """
    Class that is used by events to transfer all the data that they
    need to give the EventHandlers.

    It doesn't have any fixed instance fields, instead each key value pair
    passed to the constructor becomes one of the EventData's instance fields.
    """

    def __init__(self, **kwargs):
        """
        Constructor for EventData. Each kwarg passed will become an instance
        field of the returned EventData.
        """
        self.__dict__.update(kwargs)
