import pygame
from pygame.locals import *


TILE_SIZE = 40
# Vector pointing to the next tile in the direction corresponding
# to the directional key.
VECTORS = {
        K_LEFT: (-TILE_SIZE, 0),
        K_RIGHT: (TILE_SIZE, 0),
        K_UP: (0, -TILE_SIZE),
        K_DOWN: (0, TILE_SIZE),
        } 


def tile_coords_to_rect(x, y):
    """Convert maze coordinates in tiles to position in pixels on the
    pygame display. Return a pygame.Rect object."""
    return pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)


class GameElement:

    def __init__(self, filename, coordinates):
        """Create element from image file and tile coordinates.

        - filename (str): image file
        - coordinates (tuple): tile's x, y coordinates
        """
        # Convert coords in tiles to pixel position.
        x, y = coordinates
        self.rect = tile_coords_to_rect(x, y)
        # Load image, scale it to fit TILE_SIZE and blit it.
        self.image = pygame.transform.scale(
            pygame.image.load(filename).convert_alpha(), (TILE_SIZE, TILE_SIZE))
        pygame.display.get_surface().blit(self.image, self.rect)


class MacGyver(GameElement):

    def __init__(self, coordinates):
        GameElement.__init__(self, 'ressource/macgyver.png', coordinates)
        pygame.display.update()

    def move_in_direction(self, key_pressed):
        """ Move MacGyver to the next tile in the direction corresponding
        to the key pressed."""
        # Add the vector coresponding to the directional key pressed
        # to the position.
        x, y = VECTORS[key_pressed]
        self.rect.x += x
        self.rect.y += y
        # Blit and update display.
        pygame.display.get_surface().blit(self.image, self.rect)
        pygame.display.update()


class Maze:
    """Object containing the maze's elements: walls tiles, path tiles"""

    def __init__(self, filename):
        """Load maze map from file and initialize pygame display.

        The file must contain a visual representation of the maze map
        where each tile is represented by a character:
        - wall: '#'
        - path: ' ' (space)
        - start: 'S'
        - exit: 'E'
        """
        # Get list of file's lines without newline characters.
        with open(filename, 'r') as f:
            lines = [l[:-1] for l in f]

        # Initialize maze's attributes
        self.height = len(lines)
        self.width = len(lines[0])
        # Group objects
        self.walls = []
        self.paths = []

        # initialize pygame display
        pygame.init()
        pygame.display.set_mode((TILE_SIZE * self.height,
                                 TILE_SIZE * self.width))

        # For each character and its coordinates, add the coresponding
        # GameElememnts, then update the display
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == '#':
                    self.walls.append(GameElement(
                        'ressource/wall.png', (x, y)))
                elif char in (' ', 'S', 'E'):
                    self.paths.append(GameElement(
                        'ressource/path.png', (x, y)))
                if char == 'S':
                    self.start = (x, y)
                elif char == 'E':
                    self.exit = (x, y)
        pygame.display.update()


def main():
    """Initialization and main loop of the game"""
    # Initialization
    maze = Maze('maze.txt')
    macgyver = MacGyver(maze.start)
    # Main loop
    while 1:
        # Get events.
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            # If directional key pressed, move macgyver.
            if event.type == KEYDOWN and event.key in VECTORS:
                macgyver.move_in_direction(event.key)
        pygame.time.wait(100)


if __name__ == '__main__':
    main()
