import pygame
from pygame.locals import *

TILE_SIZE = 40
DIR_KEYS = {K_LEFT: 'left', K_RIGHT: 'right', K_UP: 'up', K_DOWN: 'down'}
    

def _coords_to_rect(coordinates):
    """Convert coordinates in tiles to pygame.Rect position"""
    x, y = coordinates
    return pygame.Rect(x * TILE_SIZE, y * TILE_SIZE,
                       TILE_SIZE, TILE_SIZE)

def wait(n):
    pygame.time.wait(n)

def init():
    pygame.init()


def set_dimensions(width, height):
    x, y, w, h = _coords_to_rect((width, height))
    pygame.display.set_mode((x, y))


def draw(*elements):
    """Blit an image on tile coordinates
    
    elements -- dictionary {<coordinates>: <image>}"""
    for element in elements:
        # Load, convert image.
        image = pygame.transform.scale(
            pygame.image.load(element.image).convert_alpha(),
            (TILE_SIZE, TILE_SIZE))
        # Convert coordinates.
        rect = _coords_to_rect(element.coordinates)
        # Blit.
        pygame.display.get_surface().blit(image, rect)
    pygame.display.update()


def draw_text(text, color='white'):
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


class KeysState:

    def __init__(self):
        self.state = dict.fromkeys(DIR_KEYS, False)

    @property
    def down(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            # Update which keys are beeing pressed in keys_down:
            if event.type == KEYDOWN and event.key in DIR_KEYS:
                self.state[event.key] = True
            elif event.type == KEYUP and event.key in DIR_KEYS:
                self.state[event.key] = False
        return [DIR_KEYS[key] for key, down in self.state.items() if down]
