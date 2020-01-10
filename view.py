import sys

import pygame
from pygame.locals import *


class View:
    """Draw tiles on a grid using pygame."""

    # Convert pygame key constant to string
    DIR_KEYS = {K_LEFT: 'left', K_RIGHT: 'right', K_UP: 'up', K_DOWN: 'down'}

    def __init__(self, tile_size):
        """Initialize view, set grid's tile size in pixels."""
        pygame.init()
        self._tile_size = tile_size
        # Store the loaded images
        self._images = {}
        # The directional key currently down
        self._key_down = None

    def get_key_down(self):
        """Get which directional key is currently down. Return str or
        None if none are down."""
        # Get key down (if more than one key down in the queue, return
        # the last one)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN and event.key in self.DIR_KEYS:
                self._key_down = event.key
            elif event.type == KEYUP and event.key == self._key_down:
                self._key_down = None
        # Convert pygame key constant to string
        return self.DIR_KEYS.get(self._key_down, None)

    @staticmethod
    def wait(n):
        pygame.time.wait(n)

    @staticmethod
    def update():
        pygame.display.update()

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

    def draw(self, filename, coordinates):
        """Draw image at coordinates."""
        # Store loaded images in self._images so that they're only
        # loaded once.
        if filename not in self._images:
            image = pygame.image.load(filename)
            # White --> transparent.
            image.set_colorkey(pygame.Color('white'))
            image = pygame.transform.scale(
                image, (self._tile_size, self._tile_size))
            self._images[filename] = image

        # Convert coordinates.
        rect = pygame.Rect(self._coords_to_pixels(coordinates),
                           (self._tile_size, self._tile_size))
        # Blit.
        self._blit(self._images[filename], rect)

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

    def draw_text_at(self, text, coordinates, color='white'):
        """Blit text on display at tiles coordinates."""
        font = pygame.font.Font(None, self._tile_size)
        text = font.render(text, 1, pygame.Color(color))
        text_rect = text.get_rect().move(self._coords_to_pixels(coordinates))
        # Blit.
        self._blit(text, text_rect)
