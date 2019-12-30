import sys

import pygame
from pygame.locals import *


TILE_SIZE = 40


def wait(n):
    pygame.time.wait(n)


def init():
    pygame.init()


def set_dimensions(width, height):
    """Set dimensions of the display.

    width, height -- dimensions measured in tiles"""
    pygame.display.set_mode(_coords_to_pixels((width, height)))


def _coords_to_pixels(coordinates):
    """Convert coordinates in tiles to position in pixels"""
    x, y = coordinates
    return x * TILE_SIZE, y * TILE_SIZE


def load_image(filename):
    """Load, convert image and scale image to tile size."""
    return pygame.transform.scale(
        pygame.image.load(filename).convert_alpha(),
        (TILE_SIZE, TILE_SIZE))


def draw(*elements):
    """Blit element's images and update display
    
    elements -- object(s) containing an attribute image (str: file path) and
    an attribute coordinates (tuple: coordinates in tiles)
    """
    for element in elements:
        # Convert coordinates.
        image = load_image(element.image)
        rect = pygame.Rect(_coords_to_pixels(element.coordinates),
                           (TILE_SIZE, TILE_SIZE))
        # Blit.
        pygame.display.get_surface().blit(image, rect)
    pygame.display.update()


def draw_centered_text(text, color='white'):
    """Blit text centered on display."""
    font = pygame.font.Font(None, 100)
    text = font.render(text, 1, pygame.Color(color))
    # Center text.
    display_rect = pygame.display.get_surface().get_rect()
    text_rect = text.get_rect()
    text_rect.center = display_rect.center
    # Blit
    pygame.display.get_surface().blit(text, text_rect)
    pygame.display.update()


def draw_text_at(text, coordinates, color='white'):
    """Blit text on display at tiles coordinates."""
    font = pygame.font.Font(None, TILE_SIZE)
    text = font.render(text, 1, pygame.Color(color))
    text_rect = text.get_rect().move(_coords_to_pixels(coordinates))
    # Erase previous text with black rectangle.
    pygame.draw.rect(pygame.display.get_surface(), pygame.Color('black'),
                     text_rect)
    # Blit.
    pygame.display.get_surface().blit(text, text_rect)
    pygame.display.update()


class KeysState:
    """Store the state (up or down) of the directional keys."""
    # Convert pygame key constant to string
    DIR_KEYS = {K_LEFT: 'left', K_RIGHT: 'right', K_UP: 'up', K_DOWN: 'down'}

    def __init__(self):
        """Initialize state with all directional keys up."""
        self.state = dict.fromkeys(self.DIR_KEYS, False)

    @property
    def down(self):
        """Update keys state and return a list of the directional keys
        currently down."""
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            # Update keys state.
            if event.type == KEYDOWN and event.key in self.DIR_KEYS:
                self.state[event.key] = True
            elif event.type == KEYUP and event.key in self.DIR_KEYS:
                self.state[event.key] = False
        # Only return keys currently down. Convert pygame key constants
        # to string
        return [self.DIR_KEYS[key] for key, down in self.state.items() if down]
