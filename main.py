from controller import Controller

def main():
    """Main loop of the game."""
    ctl = Controller()
    while 1:
        # Get the directional key pressed and move macgyver if that tile
        # is on the maze path (MacGyver can't cross walls or go outside
        # the maze boundaries.)
        direction = ctl.key_down()
        if direction is not None and ctl.next_tile_is_path(direction):
            ctl.move_macgyver(direction)
            if ctl.object_here():
                ctl.pick_up_object()
            # When MacGyver reaches the guard, if no objects are left
            # in the maze, he wins; otherwise, game over.
            if ctl.guard_here():
                if ctl.collected_all_objects():
                    ctl.win()
                else:
                    ctl.game_over()
                return
        # Only run every 100 ms
        ctl.wait()


if __name__ == '__main__':
    main()
