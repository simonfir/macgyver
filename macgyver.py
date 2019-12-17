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
        self.image = pygame.transform.scale(
            pygame.image.load(filename).convert_alpha(), (TILE_SIZE, TILE_SIZE))
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

    def __init__(self, coordinates):
        GameElement.__init__(self, 'ressource/macgyver.png', coordinates)

    def next_tile_in_direction(self, key_pressed):
        """Get the coordinates of the tile in the direction
        corresponding to the key pressed"""
        vx, vy = VECTORS[key_pressed]
        return (self.x + vx, self.y + vy)

    def move_to_tile(self, coordinates):
        """Move MacGyver to a tile coordinates"""
        self.x, self.y = coordinates
        self.draw()


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
        # Dictionaries: self.wall[x, y] = GameElement
        self.walls = {}
        self.paths = {}

        # initialize pygame display
        pygame.display.set_mode((TILE_SIZE * self.height,
                                 TILE_SIZE * self.width))

        # For each character and its coordinates, add the coresponding
        # GameElememnts, then update the display
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == '#':
                    self.walls[x, y] = GameElement('ressource/wall.png', (x, y))
                elif char in (' ', 'S', 'E'):
                    self.paths[x, y] = GameElement('ressource/path.png', (x, y))
                if char == 'S':
                    self.start = (x, y)
                elif char == 'E':
                    self.exit = (x, y)

    def draw_path(self, coordinates):
        """Blit path tile"""
        self.paths[coordinates].draw()


def draw_text(text):
    """Blit text centered on display"""
    # Font size proportional to tile size
    font = pygame.font.Font(None, TILE_SIZE * 4)
    text = font.render(text, 1, (255, 255, 255))
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
    maze = Maze('maze.txt')
    macgyver = MacGyver(maze.start)
    guard = GameElement('ressource/gardien.png', maze.exit)
    pygame.display.update()

    # Main loop
    while 1:
        # Get events.
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            # If directional key pressed, get next tile coordinates and
            # check if it's on the maze path (MacGyver can't cross walls
            # or go outside the maze boundaries.) then move macgyver.
            elif event.type == KEYDOWN and event.key in VECTORS:
                next_tile = macgyver.next_tile_in_direction(event.key)
                if next_tile in maze.paths:
                    # Erase macgyver on previous tile.
                    maze.draw_path(macgyver.coordinates)
                    macgyver.move_to_tile(next_tile)
                    pygame.display.update()
                    # Player wins when he reaches the guard.
                    if next_tile == guard.coordinates:
                        draw_text('YOU WIN!')
                        pygame.display.update()
        pygame.time.wait(100)


if __name__ == '__main__':
    main()
