from random import shuffle
from os import path

# Data files names
MAZE_MAP = 'maze.txt'
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
        coordinates -- (x, y) coordinates measured in tiles
        """
        # Store coordinates in tiles (they will be converted to pixels
        # in the draw method)
        self.x, self.y = coordinates
        self.image = path.join(path.dirname(__file__), IMAGES_DIR, filename)

    @property
    def coordinates(self):
        """Get coordinates (in tiles). Return a tuple."""
        return self.x, self.y


class MacGyver(GameElement):
    """GameElement that can be moved."""

    def __init__(self, coordinates):
        GameElement.__init__(self, MACGYVER_IMG, coordinates)

    def next_tile_in_direction(self, direction):
        """Get the coordinates of the next tile. Return (x, y) tuple.
        key -- string: 'left', 'right', 'up' or 'down'
        """
        # Vector pointing to the next tile.
        vec_x, vec_y = {
            'left': (-1, 0),
            'right': (1, 0),
            'up': (0, -1),
            'down': (0, 1),
        }[direction]
        return self.x + vec_x, self.y + vec_y

    def move_in_direction(self, direction):
        """Move MacGyvre to the next tile.
        key -- string: 'left', 'right', 'up' or 'down'
        """
        self.x, self.y = self.next_tile_in_direction(direction)


class Guard(GameElement):

    def __init__(self, coordinates):
        GameElement.__init__(self, GUARD_IMG, coordinates)


def create_objects(coordinates_list):
    """Create objects to collect.
    Return a dictionary {coordinates: GameElement}

    coordinates_list -- list of coordinates measured in tiles"""
    return {coords: GameElement(image, coords)
            for image, coords in zip(OBJECTS_IMGS, coordinates_list)}


class Counter:
    """Count of the objects collected."""

    def __init__(self, total):
        """Create counter initialized at 0.

        total -- the total number of objects to be collected"""
        self.collected = 0
        self.total = total

    def increment(self):
        """Increment and update counter."""
        self.collected += 1

    @property
    def text(self):
        """Get the text to display"""
        return 'Collected objects: {}/{}'.format(self.collected, self.total)


class Maze:
    """Object containing the maze's elements: walls and path tiles,
    start and exit tions."""

    def __init__(self):
        """Load maze map from file.

        maze_file -- maze map file name
            The maze file must contain a visual representation of the
            maze map where each tile is represented by a character:
            - wall: '#'
            - path: ' ' (space)
            - start: 'S'
            - exit: 'E'
        """
        maze_file = path.join(path.dirname(__file__), MAZE_MAP)
        # Get list of file's lines without newline characters.
        with open(maze_file, 'r') as f:
            lines = [l[:-1] for l in f]

        # Initialize maze's attributes
        self.height = len(lines)
        self.width = len(lines[0])
        self.start = None
        self.exit = None
        # Dictionaries {coordinates: GameElement}
        self.paths = {}
        self.walls = {}

        # For each character and its coordinates, add the corresponding
        # GameElements
        for y, line in enumerate(lines):
            # Make sure all rows have the same width.
            if len(line) != self.width:
                raise Exception('Inconsistent width for line {} in maze file'
                                .format(y + 1))
            for x, char in enumerate(line):
                if char == '#':
                    self.walls[x, y] = GameElement(WALL_IMG, (x, y))
                elif char in (' ', 'S', 'E'):
                    self.paths[x, y] = GameElement(PATH_IMG, (x, y))
                else:
                    raise Exception(
                        "Invalid character '{}' at {},{} in maze file"
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
