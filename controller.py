import model
import view


class Controller:

    def __init__(self):
        """Initiate view, add and draw all the game elements."""
        # Initialization
        self.view = view.View(tile_size=40)
        # Maze
        self.maze = model.Maze()
        self.view.set_dimensions(self.maze.width, self.maze.height)
        # Characters
        self.macgyver = model.MacGyver(self.maze.start)
        self.guard = model.Guard(self.maze.exit)
        # Objects
        coordinates_list = self.maze.random_path_tiles(model.NBR_OBJECTS)
        self.objects = model.create_objects(coordinates_list)
        # Counter
        self.counter = model.Counter(model.NBR_OBJECTS)

        self._refresh()

    def _refresh(self):
        """Redraw all the elements on the screen."""
        for element in (*self.maze.paths.values(), *self.maze.walls.values(),
                        self.guard, self.macgyver, *self.objects.values()):
            self.view.draw(element.image, element.coordinates)
        self.view.draw_text_at(self.counter.text, (0, self.maze.height -1))
        self.view.update()

    def key_down(self):
        """Get which directional key is currently pressed (down)."""
        return self.view.get_key_down()

    def next_tile_is_path(self, direction):
        """Check if the tile next to MacGvyer is a path.
        direction -- 'left', 'right', 'up' or 'down'"""
        return (self.macgyver.next_tile_in_direction(direction)
                in self.maze.paths)

    def move_macgyver(self, direction):
        """Move MacGyver one tile.
        direction -- 'left', 'right', 'up' or 'down'"""
        self.macgyver.move_in_direction(direction)
        self._refresh()

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
        self._refresh()

    def collected_all_objects(self):
        """Check if there is no objects left on the maze."""
        return self.objects == {}

    def win(self):
        """Show victory message."""
        self.view.draw_centered_text('YOU WIN!', '#ffff99')
        self.view.update()
        self.view.wait(2000)

    def game_over(self):
        """Show defeat message."""
        # Erase MacGyver with guard.
        self.view.draw(self.guard.image, self.guard.coordinates)
        self.view.draw_centered_text('GAME OVER', 'red')
        self.view.update()
        self.view.wait(2000)

    def wait(self):
        self.view.wait(100)
