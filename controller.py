import model
import view


class Controller:

    def __init__(self):
        """Initiate view, add and draw all the game elements."""
        # Initialization
        view.init()
        self.keys_state = view.KeysState()
        # Maze
        self.maze = model.Maze()
        # height + 1 to make space for counter.
        view.set_dimensions(self.maze.width, self.maze.height + 1)
        # Characters
        self.macgyver = model.MacGyver(self.maze.start)
        self.guard = model.Guard(self.maze.exit)
        # Objects
        coordinates_list = self.maze.random_path_tiles(model.NBR_OBJECTS)
        self.objects = model.create_objects(coordinates_list)
        # Counter
        self.counter = model.Counter(model.NBR_OBJECTS)

        # Draw all the elements on screen:
        view.draw(*self.maze.paths.values(), *self.maze.walls.values(),
              self.guard, self.macgyver, *self.objects.values())
        view.draw_text_at(self.counter.text, (0, self.maze.height))

    def keys_down(self):
        """Get which directional keys are currently pressed (down).
        Return list."""
        return self.keys_state.down

    def next_tile_is_path(self, direction):
        """Check if the tile next to MacGvyer is a path.
        direction -- 'left', 'right', 'up' or 'down'"""
        return (self.macgyver.next_tile_in_direction(direction)
                in self.maze.paths)

    def move_macgyver(self, direction):
        """Move MacGyver one tile.
        direction -- 'left', 'right', 'up' or 'down'"""
        # Erase macgyver on previous tile
        view.draw(self.maze.paths[self.macgyver.coordinates])
        self.macgyver.move_in_direction(direction)
        view.draw(self.macgyver)

    def object_here(self):
        """Check if MacGyver is on the same tile as an object.
        Return bool."""
        return self.macgyver.coordinates in self.objects

    def guard_here(self):
        """Check if MacGyver is on the same tile as the guard.
        Return bool."""
        return self.macgyver.coordinates == self.guard.coordinates

    def pick_up_object(self):
        """Pick up object and update counter."""
        del self.objects[self.macgyver.coordinates]
        self.counter.increment()
        view.draw_text_at(self.counter.text, (0, self.maze.height))

    def collected_all_objects(self):
        """Check if there is no left on the maze."""
        return self.objects == {}

    def win(self):
        """Show victory message."""
        view.draw_centered_text('YOU WIN!', '#ffff99')
        view.wait(2000)

    def game_over(self):
        """Show defeat message."""
        # Erase MacGyver with guard.
        view.draw(self.guard)
        view.draw_centered_text('GAME OVER', 'red')
        view.wait(2000)

    @staticmethod
    def wait():
        view.wait(100)
