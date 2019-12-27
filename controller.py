import model
import view

def main():
    """Initialization and main loop of the game."""
    # Initialization
    view.init()
    maze = model.Maze('maze.txt')
    view.set_dimensions(maze.width, maze.height)
    # Characters
    macgyver = model.MacGyver(maze.start)
    guard = model.Guard(maze.exit)
    # Objects
    coords = maze.random_path_tiles(model.NBR_OBJECTS)
    objects = model.create_objects(coords)
    # Counter
    #counter = model.Counter((1, maze.height), model.NBR_OBJECTS)

    view.draw(
        *maze.paths.values(),
        *maze.walls.values(),
        guard,
        macgyver,
        *objects.values())

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
            macgyver.move_to(next_tile)
            view.draw(macgyver)

            # Pick up object
            if next_tile in objects:
                del objects[next_tile]
                #counter.increment()

            # Player wins when he reaches the guard and has got every
            # objects, if he hasn't, game over.
            if next_tile == guard.coordinates:
                if not objects:
                    view.draw_text('YOU WIN!', '#ffff99')
                else:
                    # Erase MacGyver
                    view.draw(guard)
                    view.draw_text('GAME OVER', 'red')
                # Close game.
                view.wait(2000)
                return
        view.wait(100)


if __name__ == '__main__':
    main()
