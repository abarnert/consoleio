import contextlib
import fcntl
import os
import select
import sys
import termios
import tty

# Things that are illegal but may not be flagged:
# * Calling anything (but enable) while not enabled
# * Calling getch after ungetwch or vice-versa

_termstash, _flagstash = None, None
_pushback = []

def enable():
    global _termstash, _flagstash
    if not sys.stdin.isatty():
        raise RuntimeError('consoleio on non-tty')
    if _termstash:
        return False
    fd = sys.stdin.fileno()
    _termstash = termios.tcgetattr(fd)
    tty.setraw(fd)
    _flagstash = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, _flagstash | os.O_NONBLOCK)
    return True

def disable():
    global _termstash, _flagstash
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSANOW, _termstash)
    fcntl.fcntl(fd, fcntl.F_SETFL, _flagstash)
    _termstash, _flagstash = None, None

def kbhit():
    if _pushback:
        return True
    r, _, _ = select.select([sys.stdin.fileno()], [], [], 0)
    return bool(r)

@contextlib.contextmanager
def _echoing():
    stash = termios.tcgetattr(fd)
    new[tty.LFLAG] |= termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, new)
    yield
    termios.tcsetattr(fd, termios.TCSANOW, stash)

def getch():
    if _pushback:
        return _pushback.pop(0)
    return sys.stdin.buffer.read(1)

def getwch():
    if _pushback:
        return _pushback.pop(0)
    return sys.stdin.read(1)

def getche():
    if _pushback:
        ch = _pushback.pop(0)
        putch(ch)
        return ch
    with _echoing():
        return sys.stdin.buffer.read(1)

def getwche():
    if _pushback:
        wch = _pushback.pop(0)
        putwch(wch)
        return wch
    with echoing():
        return sys.stdin.read(1)

def ungetch(ch):
    _pushback.append(ch)

def ungetwch(wch):
    _pushback.append(wch)

def putch(ch):
    sys.stdout.buffer.write(ch)
    sys.stdout.flush()

def putwch(wch):
    sys.stdout.write(wch)
    sys.stdout.flush()
