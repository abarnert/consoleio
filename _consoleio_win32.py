from msvcrt import kbhit, getch, getche, getwch, getwche
from msvcrt import putch, putwch, ungetch, ungetwch

def enable():
    if not sys.stdin.isatty():
        raise RuntimeError('consoleio on non-tty')
    return False

def disable():
    pass
