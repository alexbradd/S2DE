"""
This module contains the TextRenderer Behaviour.
"""
import pygame

from engine import Behaviour
from engine import ComponentError

from components import Transform
import engine.vars as gvars


class TextRenderer(Behaviour):
    """
    The TextRenderer renders, as the name implies, some text 'text' with
    size 'size' on the screen at the position of the Transform attached to
    the same GameObject with color 'color'.
    """
    
    def __init__(self, enabled=True, size=0, color=(0, 0, 0), text=''):
        """
        Constructor for TextRenderer. Takes in a bool that specifies if
        the component should be enabled ('enabled'), the size of the text
        ('size'), a tuple with the RGB values of its color ('color') and
        a string containing the text that will be rendered.
        """
        super().__init__(enabled)
        self.size = size
        self.color = color
        self.text = text
        
        self.font = pygame.font.Font(None, self.size)
        self.rendered_text = None

        self.transform = None
        
    def on_attach(self):
        """Get a reference to the GameObject's transform"""
        self.transform = self.gameobject.get_component(Transform)
        if not self.transform:
            raise ComponentError('Cannot find Transform attached to GameObject',
                                 self)
        
    def on_behaviour_update(self):
        """Draw the text on the screen"""
        if self.rendered_text:
            self.rendered_text.fill(gvars.FLUSH_COLOR)

        self.rendered_text = self.font.render(self.text, True, self.color)
        gvars.SCREEN.blit(self.rendered_text, self.transform.absolute_pos)

    def change_size(self, new_size):
        """Change the size of the font"""
        self.size = new_size
        self.font = pygame.font.Font(None, self.size)
