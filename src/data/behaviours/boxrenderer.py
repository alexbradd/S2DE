"""
This module contains the BoxRenderer Behaviour.
"""
import pygame

from engine import Behaviour
from engine import ComponentError

from components import Transform
import engine.vars as gvars


class BoxRenderer(Behaviour):
    """
    The BoxRenderer renders, as the name implies, a simple rectangle with
    dimensions 'width' and 'height' on the screen at the position of the
    Transform attached to the same GameObject with color 'color'.
    """
    
    def __init__(self, enabled=True, width=0, height=0, color=(255, 255, 255)):
        """
        Constructor for BoxRenderer. Takes in a bool that specifies if
        the component should be enabled ('enabled'), the dimensions of the
        rectangle ('width' and 'height') and a tuple with the RGB values of the
        color.
        """
        super().__init__(enabled)
        self.width = width
        self.height = height
        self.color = color[:]
        self.surface = pygame.Surface((self.width, self.height))
        self.transform = None
        
    def on_attach(self):
        """Get a reference to the GameObject's transform"""
        self.transform = self.gameobject.get_component(Transform)
        if not self.transform:
            raise ComponentError('Cannot find Transform attached to GameObject',
                                 self)
        
    def on_behaviour_update(self):
        """Draw the rectangle on the screen"""
        self.surface.fill(gvars.FLUSH_COLOR)

        rect = [0, 0, self.width, self.height]
        pygame.draw.rect(self.surface, self.color, rect)
        gvars.SCREEN.blit(self.surface, self.transform.absolute_pos)
