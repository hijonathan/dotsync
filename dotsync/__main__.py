#!/usr/bin/env python
"""

Usage:
  dotsync add <source> [--destination=<destination>] [options]
  dotsync remove <source> [options]
  dotsync save [options]
  dotsync restore [--destination=<destination>] [options]

Options:
  -c --config=<config>      Configuration file [default: ~/.moxie.yaml]
  -t --test                 Run as a test only
  -l --loglevel=<loglevel>  Logging level [default: INFO]
  -h --help                 Show this help message and exit
  -v --version              Show version and exit

"""

import sys
import platform
from docopt import docopt

from . import __version__
from . import __platforms__

from .core import main


def entry():
    if platform.system() not in __platforms__:
        sys.stderr.write("Dotsync wasn't designed to run on your system, sorry.")
        return 1

    return main(docopt(__doc__, version=__version__))


if __name__ == '__main__':
    sys.exit(entry())
