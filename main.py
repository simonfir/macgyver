from controller import Controller

def main():
    """Main loop of the game."""
    ctl = Controller()
    while 1:
        # For each directional key down, get the next tile
        # coordinates in the direction of the key and move macgyver if
        # that tile is on the maze path (MacGyver can't cross walls or
        # go outside the maze boundaries.)
        for direction in ctl.keys_down():
            if ctl.next_tile_is_path(direction):
                ctl.move_macgyver(direction)
                if ctl.object_here():
                    ctl.pick_up_object()
                # When MacGyver reaches the guard, if no objects are left
                # in the maze, he wins and goes to the next level;
                # otherwise, game over and level is restarted.
                if ctl.guard_here():
                    if ctl.collected_all_objects():
                        ctl.win()
                        ctl.next_level()
                    else:
                        ctl.game_over()
                        ctl.restart_level()
        ctl.wait()


if __name__ == '__main__':
    main()
