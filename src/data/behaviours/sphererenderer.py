"""
This module contains the BoxRenderer Behaviour.
"""
import pygame

from engine import Behaviour
from engine import ComponentError

from components import Transform
import engine.vars as gvars


class CircleRenderer(Behaviour):
    """
    The CircleRenderer renders, as the name implies, a simple circle with
    radius 'radius' on the screen at the position of the Transform attached to
    the same GameObject with color 'color'.
    """
    
    def __init__(self, enabled=True, radius=0, color=(255, 255, 255)):
        """
        Constructor for CircleRenderer. Takes in a bool that specifies if
        the component should be enabled ('enabled'), the radius of the circle
        ('radius') and a tuple with the RGB values of the color.
        """
        super().__init__(enabled)
        self.radius = radius
        self.color = color[:]
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2))

        self.transform = None

    def on_attach(self):
        """Get a reference to the GameObject's transform"""
        self.transform = self.gameobject.get_component(Transform)
        if not self.transform:
            raise ComponentError('Cannot find Transform attached to GameObject',
                                 self)
        
    def on_behaviour_update(self):
        """Draw the circle on the screen"""
        self.surface.fill(gvars.FLUSH_COLOR)
        
        pos = [self.radius, self.radius]
        pygame.draw.circle(self.surface, self.color, pos, self.radius)
        
        gvars.SCREEN.blit(self.surface, self.transform.absolute_pos)
