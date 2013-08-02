import contextlib
import sys

if sys.platform == 'win32':
    from _consoleio_win32 import *
else:
    from _consoleio_posix import *

@contextlib.contextmanager    
def enabling():
    was_disabled = enable()
    yield was_disabled
    if was_disabled:
        disable()

def _test():
    import itertools
    import time
    spinner = '-\|/'
    it = itertools.cycle(spinner)
    with enabling():
        for ch in 'Press any key to continue:  ':
            putwch(ch)
        while not kbhit():
            putch(b'\010')
            putwch(next(it))
            time.sleep(1)
        hit = getwch()
    print('\nYou hit: {} ({})'.format(hit, hex(ord(hit))))

if __name__ == '__main__':
    _test()
    
