consoleio
=========

A Python module that provides simple conio-style functionality on both POSIX and Windows.

Example
-------

    import itertools
    from consoleio import * 

    with enabling():
        for ch in 'Press any key to continue:  ':
            putwch(ch)
        spinner = itertools.cycle('-\|/')
        while not khbit():
            putch(b'\010')
            putwch(next(spinner))
            time.sleep(1)
        hit = getwch()
    print('\nYou hit: {}'.format(hit))

Caveats
-------

 * You cannot use this on non-Win32 platforms that do not support termios.
 * Do not call any of the functions outside of enabling.
 * Do not use stdin and stdout in any other way inside of enabling.
 * Do not pass anything but a single unicode char to putwch.
 * Do not pass anything but a single bytes char to putch.
 * Do not call getwch after ungetch, or getch after ungetwch.
 * Do not use putch to write characters that form an invalid sequence in
   the terminal's encoding.
 * Do not taunt happy fun ball. 
 * Any of the above may not raise, or may raise something odd, or may
   succeed but not do what you expected.
 * Dead keys (e.g., option-e on Macs, or alt-keypad-0 on Windows) 
   may not trigger khbit or getch; instead, the dead key plus its 
   continuation key(s) will trigger one keystroke. However, a dead 
   key followed by an invalid continuation key (e.g., option-e 
   followed by f) may trigger two.
 * Special function keys may generate two or keystrokes. On Windows,
   you will get a '\x00' or '\xe0', and then a Win32 keycode; on
   POSIX, it depends on your terminal, but you will generally get an
   escape sequence starting with '\x1b''
 * Characters outside the Unicode BMP may be treated as two
   keystrokes (the corresponding surrogate pair) by getwch/getwche,
   and maybe even by putwch, on Windows.
 * Control-C may or may not be handled on Windows.
 * The echoing functions getche and getwche do not echo non-printable
   characters on Windows (note that this uses the Win32 definition of
   non-printable, not the Python one), but do on POSIX.
 * On POSIX, if you manage to exit the program while still in consoleio 
   mode, your terminal may be screwed up. On most platforms, you can fix 
   this by hitting control-C (to clear any buffered input), then typing 
   "reset".

API
---

    enabling()
        A context manager that calls enable() and disable() properly.
    
    enable()
        If consoleio mode is already enabled, return False and do nothing.
        Otherwise, enable it and return True.
    
    disable()
        Disables consoleio mode, restoring the terminal settings to what
        was in effect before calling enable().

    kbhit()
        Return true if a keypress is waiting to be read.

    getch()
        Read a keypress and return the resulting character as a bytes string. 
        Nothing is echoed to the console. This call will block if a keypress 
        is not already available, but will not wait for Enter to be pressed.
        
    getwch()
        Unicode version of getch, returning a str value.

    getche()
        Similar to getch(), but the keypress will be echoed.

    getwche()
        Unicode variant of getche(), returning a str value.

    putch(char)
        Print the single-character bytes string char to the console 
        without buffering.

    putwch(unicode_char)
        Unicode variant of putch(), accepting a str value.

    ungetch(char)
        Cause the bytes string char to be “pushed back” into the console buffer; 
        it will be the next character read by getch() or getche().

    ungetwch(unicode_char)
        Unicode variant of ungetch(), accepting a str value.

See also
--------

 * stdlib termios, tty, msvcrt, and curses modules.
 * http://code.activestate.com/recipes/134892-getch-like-unbuffered/: An
   ActiveState recipe for getch on Unix, which I'll have to check to see
   if it does anything I should be doing but am not.
 * https://pypi.python.org/pypi/getch: An even more minimalist version of 
   the same idea, providing only getch and getche... but it seems to use a C
   extension module to call MSVCRT or termios functions directly, instead of
   using the existing stdlib wrappers.
 * https://pypi.python.org/pypi/pager: A more complex library that has some
   overlap with consoleio. Also see http://bugs.python.org/issue8408, a 
   rejected bug report to add pager to the stdlib.
 * https://pypi.python.org/pypi/term: An POSIX-only module that extends tty
   (primarily adding context managers, but also an interesting getyx
   function, and code to open /dev/tty).
 * https://pypi.python.org/pypi/termprop: A POSIX-only module that extends
   termios.
 * Various libraries to do cross-platform colored console output (colorconsole,
   termstyle, Colors, colorama, etc.). It's worth verifying that they can be
   used together with consoleio.
 * Various libraries to do more extreme output formatting, including anything
   from cursor addressing to dithering graphics to text (libcaca, fabulous, 
   Console, Python-Conio, etc.), many platform-specific.
 * Various curses extensions/replacements like blessings, and wrappers
   for wincurses.
