from random import shuffle
from os import path

# Vector pointing to the next tile in the direction corresponding
# to the directional key.
VECTORS = {
    'left': (-1, 0),
    'right': (1, 0),
    'up': (0, -1),
    'down': (0, 1),
    }

# Images file names
IMAGES_DIR = 'ressource'
WALL_IMG = 'wall.png'
PATH_IMG = 'path.png'
MACGYVER_IMG = 'macgyver.png'
GUARD_IMG = 'gardien.png'
OBJECTS_IMGS = ('aiguille.png', 'seringue.png',
                  'tube_plastique.png', 'ether.png')
NBR_OBJECTS = len(OBJECTS_IMGS)


class GameElement:
    """Represent an element of the game: an image that can be drawn on a
    tile."""

    def __init__(self, filename, coordinates):
        """Create element from image file and tile coordinates.

        filename -- image file name
        coordinates -- (x, y) coordinates mesured in tiles
        """
        # Store coordinates in tiles (they will be converted to pixels
        # in the draw method)
        self.x, self.y = coordinates
        self.image = path.join(path.dirname(__file__), IMAGES_DIR, filename)

    @property
    def coordinates(self):
        """Get coordinates (in tiles). Return a tuple."""
        return (self.x, self.y)


class MacGyver(GameElement):
    """GameElement that can be moved."""

    def __init__(self, coordinates):
        GameElement.__init__(self, MACGYVER_IMG, coordinates)

    def next_tile_in_direction(self, key):
        """Get the coordinates of the tile in the direction corresponding
        to the key pressed. Return (x, y) tuple.

        key -- pygame key constant"""
        vx, vy = VECTORS[key]
        return (self.x + vx, self.y + vy)

    def move_to(self, coordinates):
        self.x, self.y = coordinates


class Guard(GameElement):

    def __init__(self, coordinates):
        GameElement.__init__(self, GUARD_IMG, coordinates)


def create_objects(coords_list):
    return {coords: GameElement(image, coords)
            for image, coords in zip(OBJECTS_IMGS, coords_list)}


class Counter:
    """Display a count of the objects collected."""

    def __init__(self, coordinates, total):
        """Create counter initialized at 0 and draw it.

        coordinates -- (in tiles) where to draw the counter
        total -- the total number of objects to be collected"""
        self.collected = 0
        self.total = total
        self.x, self.y = coordinates
        self._draw()

    def increment(self):
        """Increment and update counter."""
        self.collected += 1
        self._draw()


class Maze:
    """Object containing the maze's elements: walls and path tiles,
    start and exit tions."""

    def __init__(self, maze_file):
        """Load maze map from file.

        maze_file -- maze map file name
            The maze file must contain a visual representation of the
            maze map where each tile is represented by a character:
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
        # Dictionaries: self.paths[x, y] = GameElement
        self.paths = {}
        self.walls = {}

        # For each character and its coordinates, add the coresponding
        # GameElememnts
        for y, line in enumerate(lines):
            # Make sure if all rows have the same width
            if len(line) != self.width:
                raise Exception('Inconsitant width for line {} in maze file'
                                .format(y + 1))
            for x, char in enumerate(line):
                if char == '#':
                    self.walls[x, y] = GameElement(WALL_IMG, (x, y))
                elif char in (' ', 'S', 'E'):
                    self.paths[x, y] = GameElement(PATH_IMG, (x, y))
                else:
                    raise Exception("Invalid character '{}' at {},{} in maze file"
                                    .format(char, y + 1, x + 1))
                if char == 'S':
                    self.start = (x, y)
                elif char == 'E':
                    self.exit = (x, y)

        if self.start is None or self.exit is None:
            raise Exception('Start or exit missing from maze file')

    def random_path_tiles(self, n):
        """Get the coordinates (in tiles) of n random path tiles."""
        coords = list(self.paths.keys())
        # Don't add objects on start or exit
        coords.remove(self.start)
        coords.remove(self.exit)
        shuffle(coords)
        return coords[:n]

