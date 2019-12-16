class Maze:
    """Object containing the maze's elements: walls tiles, path tiles"""

    def __init__(self, filename):
        """Load maze map from file.

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
        # list of (x, y) tuple of tiles coordinates
        self.walls = []
        self.paths = []

        # For each character, add its coordinates to the right maze
        # elememnts list
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == '#':
                    self.walls.append((x, y))
                elif char == ' ':
                    self.paths.append((x, y))
                elif char == 'S':
                    self.start = (x, y)
                elif char == 'E':
                    self.exit = (x, y)

# TESTS
if __name__ == '__main__':
    maze = Maze('maze.txt')
    print(maze.height)
    print(maze.width)
    print(maze.walls)
    print(maze.paths)
    print(maze.start)
    print(maze.exit)
