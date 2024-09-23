import curses
# ==================== key finder ====================
def test_keys(stdscr):
    '''
        Initiated with "curses.wrapper(test_keys)".
        It shows the key code of the keypad button pressed while this function is running.
            To exit it requires pressing ESC button.
    '''
    stdscr.clear()
    stdscr.addstr(0, 0, "Press keys (ESC to exit):")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        stdscr.addstr(1, 0, f"Key code: {key} ")
        stdscr.refresh()
        
        if key == 27:  # ESC key
            break


