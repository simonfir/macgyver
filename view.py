import sys

import pygame
from pygame.locals import *


class View:
    """Draw tiles on a grid using pygame."""

    def __init__(self, tile_size):
        """Initialize view, set grid's tile size in pixels."""
        pygame.init()
        self._tile_size = tile_size

    @staticmethod
    def wait(n):
        pygame.time.wait(n)

    @staticmethod
    def _blit(surface, rect):
        pygame.display.get_surface().blit(surface, rect)

    def set_dimensions(self, width, height):
        """Set dimensions of the display.

        width, height -- dimensions measured in tiles"""
        pygame.display.set_mode(self._coords_to_pixels((width, height)))

    def _coords_to_pixels(self, coordinates):
        """Convert coordinates in tiles to position in pixels"""
        x, y = coordinates
        return x * self._tile_size, y * self._tile_size

    def _load_image(self, filename):
        """Load, convert image and scale image to tile size."""
        return pygame.transform.scale(
            pygame.image.load(filename).convert_alpha(),
            (self._tile_size, self._tile_size))

    def draw(self, *elements):
        """Blit element's images and update display

        elements -- object(s) containing an attribute image (str: file path) and
        an attribute coordinates (tuple: coordinates in tiles)
        """
        for element in elements:
            image = self._load_image(element.image)
            # Convert coordinates.
            rect = pygame.Rect(self._coords_to_pixels(element.coordinates),
                               (self._tile_size, self._tile_size))
            # Blit.
            self._blit(image, rect)
        pygame.display.update()

    def draw_centered_text(self, text, color='white'):
        """Blit text centered on display."""
        font = pygame.font.Font(None, 100)
        text = font.render(text, 1, pygame.Color(color))
        # Center text.
        display_rect = pygame.display.get_surface().get_rect()
        text_rect = text.get_rect()
        text_rect.center = display_rect.center
        # Blit
        self._blit(text, text_rect)
        pygame.display.update()

    def draw_text_at(self, text, coordinates, color='white'):
        """Blit text on display at tiles coordinates."""
        font = pygame.font.Font(None, self._tile_size)
        text = font.render(text, 1, pygame.Color(color))
        text_rect = text.get_rect().move(self._coords_to_pixels(coordinates))
        # Erase previous text with black rectangle.
        pygame.draw.rect(pygame.display.get_surface(), pygame.Color('black'),
                         text_rect)
        # Blit.
        self._blit(text, text_rect)
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
