"""
This module contains the Transform component, one the fundamental components.
"""
from engine import Component
from engine import ComponentError


class Transform(Component):
    """
    The Transform is a Component that gives the GameObject to which is attached
    to the ability to have a position on the game's screen. This position can
    be 'absolute' (what the name implies) or 'local' (relative to a 'parent'
    Transform).

    A Transform can have a parent and many childs, making creating a hierarchy
    of Transforms possible. if a Transform has a parent, then its local position
    is defined.

    A Transform should always be attached at GameObject creation (passed in
    to the constructor) and every GameObject should have one. This is why
    a Transform will raise a Warning if detached, unless forced.
    """

    def __init__(self, x=0, y=0, absolute=True, parent=None):
        """
        Constructor for the Transform. Takes in the position of the
        Transform ('x', 'y'), a bool that determines if the given position
        should be interpreted as absolute or local ('absolute') and the
        name of the GameObject that will hold the Transform that will act as the
        parent to this one.
        """
        super().__init__()
        self.parent = None
        self.absolute_pos = [0, 0]
        self.local_pos = [0, 0]
        self.childs = []

        self._parent_name = parent
        self._arg_pos = [x, y]
        self._absolute = absolute

    def on_attach(self):
        """Complain if there are more than one Transforms"""
        if self.gameobject.get_component(Transform) is not self:
            raise ComponentError("More than one Transform component on the "
                                 "same GameObject is not allowed", self)

    def on_create(self):
        """Init position from arguments and find parent, if any is passed"""
        if self.gameobject.get_component(Transform) is not self:
            raise ComponentError("More than one Transform component on the "
                                 "same GameObject is not allowed", self)
        if self._parent_name is not None:
            self.parent(self._parent_name)
        if self._absolute:
            self._pos_from_absolute(*self._arg_pos)
        else:
            self._pos_from_local(*self._arg_pos)

    def _pos_from_absolute(self, x, y):
        """Gets absolute and local position from absolute x and y"""
        self.absolute_pos[0] = x
        self.absolute_pos[1] = y
        if self.parent is not None:
            self.local_pos[0] = self.absolute_pos[0] - \
                self.parent.absolute_pos[0]
            self.local_pos[1] = self.absolute_pos[1] - \
                self.parent.absolute_pos[1]

    def _pos_from_local(self, x, y):
        """Gets absolute and local position from local x and y"""
        if self.parent is None:
            raise ComponentError('Incoherent arguments: passing local '
                                 'position but no parent??', self)
        self.local_pos[0] = x
        self.local_pos[1] = y
        self.absolute_pos[0] = self.parent.absolute_pos[0] + self.local_pos[0]
        self.absolute_pos[1] = self.parent.absolute_pos[1] + self.local_pos[1]

    def on_component_update(self):
        """Update positions"""
        if self.parent is None:
            return
        self.absolute_pos[0] = self.parent.absolute_pos[0] + self.local_pos[0]
        self.absolute_pos[1] = self.parent.absolute_pos[1] + self.local_pos[1]

    def on_detach(self, forced=False):
        """Complain if not forced"""
        if not forced:
            raise RuntimeWarning('A GameObject should never be without a '
                                 'Transform')

    def on_destroy(self):
        """Unparent this Tranform and destroy all its childs"""
        self.unparent()

        for child in self.childs:
            child.destroy_gameobject()

    def destroy_gameobject(self):
        """Destroys the GameObject that this Transform is attached to"""
        try:
            self.gameobject.destroy()
        except KeyError:
            raise RuntimeWarning(f'{self.gameobject} is already destroyed')

    def unparent(self):
        """Remove this Transforms parent"""
        if not self.parent:
            return
        self.parent = None
        self.local_pos = [0, 0]

    def parent(self, parent):
        """Parent this Transform to a GameObject with name or id 'parent'"""
        parent_gobj = self.gameobject.find(parent)
        if parent_gobj == self.gameobject:
            raise ComponentError('Transform cannot be parent of itself', self)
        if not parent:
            raise ComponentError(f'Gameobject {parent} cannot be found', self)
        parent_transform = parent_gobj.get_component(Transform)
        if not parent_transform:
            raise ComponentError(f'Gameobject {parent} is without a Transform',
                                 self)
        self.parent = parent_transform
        self.parent.childs.append(self)
