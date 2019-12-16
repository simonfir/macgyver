import pygame


TILE_SIZE = 40

def tile_coords_to_rect(x, y):
    """Convert maze coordinates in tiles to position in pixels on the
    pygame display. Return a pygame.Rect object."""
    return pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)


class GameElement:

    def __init__(self, filename, x, y):
        """Create element from image file and tile coordinates.

        - filename: image file
        - x, y: tile's coordinates
        """
        # convert coords in tiles to pixel position
        self.rect = tile_coords_to_rect(x, y)
        # Load image, scale it to fit TILE_SIZE and blit it
        self.image = pygame.transform.scale(
            pygame.image.load(filename).convert(),
            (TILE_SIZE, TILE_SIZE))
        pygame.display.get_surface().blit(self.image, self.rect)


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
                    self.walls.append(GameElement('ressource/wall.png', x, y))
                if char in (' ', 'S', 'E'):
                    self.paths.append(GameElement('ressource/path.png', x, y))
                elif char == 'S':
                    self.start = (x, y)
                elif char == 'E':
                    self.exit = (x, y)
        pygame.display.update()


# TESTS
if __name__ == '__main__':
    maze = Maze('maze.txt')
    pygame.time.wait(10000)
