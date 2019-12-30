import model
import view


def main():
    """Initialization and main loop of the game."""
    # Initialization
    view.init()
    maze = model.Maze()
    # height + 1 to make space for counter.
    view.set_dimensions(maze.width, maze.height + 1)
    # Characters
    macgyver = model.MacGyver(maze.start)
    guard = model.Guard(maze.exit)
    # Objects
    coordinates_list = maze.random_path_tiles(model.NBR_OBJECTS)
    objects = model.create_objects(coordinates_list)
    # Counter
    counter = model.Counter(model.NBR_OBJECTS)

    # Draw all the elements on screen:
    view.draw(*maze.paths.values(), *maze.walls.values(),
              guard, macgyver, *objects.values())
    view.draw_text_at(counter.text, (0, maze.height))

    # Main loop
    keys_state = view.KeysState()
    while 1:
        # For each directional key down, get the next tile
        # coordinates in the direction of the key and move macgyver if
        # that tile is on the maze path (MacGyver can't cross walls or
        # go outside the maze boundaries.)
        for key in keys_state.down:
            next_tile = macgyver.next_tile_in_direction(key)
            if next_tile not in maze.paths:
                continue

            # Erase macgyver on previous tile.
            view.draw(maze.paths[macgyver.coordinates])
            # Move macgyver to next tile
            macgyver.move_to(next_tile)
            view.draw(macgyver)

            # Pick up object
            if macgyver.coordinates in objects:
                del objects[macgyver.coordinates]
                counter.increment()
                view.draw_text_at(counter.text, (0, maze.height))

            # When MacGyver reaches the guard, if no objects are left
            # in the maze, he wins; otherwise, game over.
            if macgyver.coordinates == guard.coordinates:
                if not objects:
                    view.draw_centered_text('YOU WIN!', '#ffff99')
                else:
                    # Erase MacGyver with guard.
                    view.draw(guard)
                    view.draw_centered_text('GAME OVER', 'red')
                # Wait 2 s and close game.
                view.wait(2000)
                return
        # Only run loop every 100 ms
        view.wait(100)


if __name__ == '__main__':
    main()
