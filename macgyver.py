from random import shuffle
from os import path

import pygame
from pygame.locals import *


TILE_SIZE = 40
# Vector pointing to the next tile in the direction corresponding
# to the directional key.
VECTORS = {
    K_LEFT: (-1, 0),
    K_RIGHT: (1, 0),
    K_UP: (0, -1),
    K_DOWN: (0, 1),
    }


class GameElement:

    def __init__(self, filename, coordinates):
        """Create element from image file and tile coordinates.

        - filename (str): image file
        - coordinates (tuple): x, y coordinates in tiles
        """
        # Store coordinates in tiles (they will be converted to pixels
        # in the draw method)
        self.x, self.y = coordinates
        # Load image, scale it to fit TILE_SIZE and draw element.
        filename = path.join(path.dirname(__file__), 'ressource', filename)
        self.image = pygame.transform.scale(
            pygame.image.load(filename).convert_alpha(),
            (TILE_SIZE, TILE_SIZE))
        self.draw()

    @property
    def coordinates(self):
        """Get coordinates (in tiles). Return a tuple"""
        return (self.x, self.y)

    def draw(self):
        """Blit element's image on the screen"""
        # convert tile coordinates to pixel positions
        rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE,
                           TILE_SIZE, TILE_SIZE)
        pygame.display.get_surface().blit(self.image, rect)


class MacGyver(GameElement):

    def next_tile_in_direction(self, key_pressed):
        """Get the coordinates of the tile in the direction
        corresponding to the key pressed"""
        vx, vy = VECTORS[key_pressed]
        return (self.x + vx, self.y + vy)

    def move_to_tile(self, coordinates):
        """Move MacGyver to a tile coordinates"""
        self.x, self.y = coordinates
        self.draw()


class Counter:
    """Display a count of the objects collected"""

    def __init__(self, coordinates, total):
        """Create counter with 0 objects, and draw it

        coordinates -- coordinates in tiles
        total -- the total number of objects to be collected"""
        self.collected = 0
        self.total = total
        self.x, self.y = coordinates
        self._draw()

    def increment(self):
        """Increment and update counter"""
        self.collected += 1
        self._draw()

    def _draw(self):
        """Draw counter on display"""
        font = pygame.font.Font(None, TILE_SIZE)
        text = font.render(
            'Objects collected : {}/{}'.format(self.collected, self.total),
            1, pygame.Color('#888866'))
        text_rect = text.get_rect().move(self.x * TILE_SIZE, self.y * TILE_SIZE)
        # Erease previous text with black rectangle
        pygame.draw.rect(pygame.display.get_surface(), pygame.Color('black'),
                         text_rect)
        # Blit new text
        pygame.display.get_surface().blit(text, text_rect)


class Maze:
    """Object containing the maze's elements: walls tiles, path tiles"""

    def __init__(self, maze_file, wall_file, path_file):
        """Load maze map from file and initialize pygame display.

        The file must contain a visual representation of the maze map
        where each tile is represented by a character:
        - wall: '#'
        - path: ' ' (space)
        - start: 'S'
        - exit: 'E'
        """
        maze_file = path.join(path.dirname(__file__), maze_file)
        # Get list of file's lines without newline characters.
        with open(maze_file, 'r') as f:
            lines = [l[:-1] for l in f]

        # Initialize maze's attributes
        self.height = len(lines)
        self.width = len(lines[0])
        self.start = None
        self.exit = None
        # Dictionaries: self.wall[x, y] = GameElement
        self.walls = {}
        self.paths = {}

        # Set display's dimensions
        pygame.display.set_mode((TILE_SIZE * self.width,
                                 TILE_SIZE * (self.height + 1)))

        # For each character and its coordinates, add the coresponding
        # GameElememnts
        for y, line in enumerate(lines):
            # Make sure if all rows have the same width
            if len(line) != self.width:
                raise Exception('Inconsitant width for line {} in maze file'
                                .format(y + 1))
            for x, char in enumerate(line):
                if char == '#':
                    self.walls[x, y] = GameElement(wall_file, (x, y))
                elif char in (' ', 'S', 'E'):
                    self.paths[x, y] = GameElement(path_file, (x, y))
                else:
                    raise Exception("Invalid character '{}' at {},{} in maze file"
                                    .format(char, y + 1, x + 1))
                if char == 'S':
                    self.start = (x, y)
                elif char == 'E':
                    self.exit = (x, y)

        if self.start is None or self.exit is None:
            raise Exception('Start or exit missing from maze file')

    def draw_path(self, coordinates):
        """Blit path tile"""
        self.paths[coordinates].draw()

    def _random_path_tiles(self, n):
        """Get the coordinates (in tiles) of n random path tiles"""
        coords = list(self.paths.keys())
        # Don't add objects on start or exit
        coords.remove(self.start)
        coords.remove(self.exit)
        shuffle(coords)
        return coords[:n]

    def add_objects(self, *filenames):
        """Add all objects to maze take image file names as arguments"""
        # Create counter
        nbr_objects = len(filenames)
        self.counter = Counter((1, self.height), nbr_objects)
        # Get random coordinates
        coords = self._random_path_tiles(nbr_objects)
        # Like self.walls and self.paths
        self.objects = {coords[i]: GameElement(filenames[i], coords[i])
                        for i in range(nbr_objects)}

    def remove_object(self, coordinates):
        """Delete object at coordinates from maze and update counter"""
        del self.objects[coordinates]
        self.counter.increment()


def draw_text(text, color='white'):
    """Blit text centered on display"""
    font = pygame.font.Font(None, 100)
    text = font.render(text, 1, pygame.Color(color))
    # Center text.
    display_rect = pygame.display.get_surface().get_rect()
    text_rect = text.get_rect()
    text_rect.center = display_rect.center
    # Blit
    pygame.display.get_surface().blit(text, text_rect)


def main():
    """Initialization and main loop of the game"""
    # Initialization
    pygame.init()
    maze = Maze('maze.txt', 'wall.png', 'path.png')
    macgyver = MacGyver('macgyver.png', maze.start)
    guard = GameElement('gardien.png', maze.exit)
    maze.add_objects('aiguille.png', 'ether.png',
                     'seringue.png', 'tube_plastique.png')
    pygame.display.update()

    # Main loop
    keys_down = {}
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            # Update which keys are beeing pressed in keys_down:
            if event.type == KEYDOWN and event.key in VECTORS:
                keys_down[event.key] = True
            elif event.type == KEYUP and event.key in VECTORS:
                keys_down[event.key] = False

        # For each directional key down, get the next tile
        # coordinates in the direction of the key and move macgyver if
        # that tile is on the maze path (MacGyver can't cross walls or
        # go outside the maze boundaries.)
        for key, down in keys_down.items():
            if not down:
                continue
            next_tile = macgyver.next_tile_in_direction(key)
            if next_tile not in maze.paths:
                continue

            # Erase macgyver on previous tile.
            maze.draw_path(macgyver.coordinates)
            macgyver.move_to_tile(next_tile)

            # Pick up object
            if next_tile in maze.objects:
                maze.remove_object(next_tile)

            # Player wins when he reaches the guard and has got every
            # objects, if he hasn't, game over.
            if next_tile == guard.coordinates:
                if len(maze.objects) == 0:
                    draw_text('YOU WIN!', '#ffff99')
                else:
                    # Erase MacGyver
                    guard.draw()
                    draw_text('GAME OVER', 'red')
                # Close game.
                pygame.display.update()
                pygame.time.wait(2000)
                return

        # Refresh display
        pygame.display.update()
        pygame.time.wait(100)


if __name__ == '__main__':
    main()
