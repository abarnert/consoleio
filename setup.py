from distutils.core import setup
import sys

modules = ['consoleio']
if sys.platform == 'win32':
    modules.append('_consoleio_win32')
else:
    modules.append('_consoleio_posix')

setup(name = 'consoleio',
      version = '0.1',
      description = 'cross-platform conio-style raw I/O',
      author = 'Andrew Barnert',
      author_email = 'abarnert@yahoo.com',
      url = 'https://github.com/abarnert/consoleio',
      py_modules = modules
    )
