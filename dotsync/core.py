import os
import sys
import logging
from termcolor import colored

from .config import Config


def init_logging(args):
    logging.basicConfig(level=logging.INFO)

    if hasattr(logging, args['--loglevel'].upper()):
        logging.getLogger().setLevel(getattr(logging, args['--loglevel'].upper()))
    else:
        sys.stderr.write("No such log level '%s', defaulting to 'INFO'\n", args['--loglevel'])


def check_status(config):
    # Calculate max host and port width for alignment
    width = max([len("{0} -> {1}".format(f.source, f.destination)) for f in config.tracked_files])

    # Show linked files
    for tracked_file in config.tracked_files:
        aligned_file = "{0} -> {1}".format(tracked_file.source, tracked_file.destination).ljust(width, ' ')
        if tracked_file.is_saved():
            sys.stdout.write("{0} {1}\n".format(aligned_file, colored('TRACKED', 'green')))
        else:
            sys.stdout.write("{0} {1}\n".format(aligned_file, "UNTRACKED"))

    return 0


def add_file(args, config):
    if not config.destination and not args['--destination']:
        sys.stderr.write("The heck should I put this stuff?.\n\nInclude a --destination argument, or set a default directory in your dotsync config.\n")
        return 1

    result = config.add_file(
        source=args['<source>'],
        destination=args['<destination>']
    )

    if result:
        config.save(os.path.expanduser(args['--config']))
        sys.stderr.write("Added file. Run \"dotsync save\" to save your file.\n")
        return 0
    else:
        sys.stderr.write("Failed to add file.\n")
        return 1


def remove_file(args, config):
    result = config.remove_file(args['<source>'])

    if result:
        config.save(os.path.expanduser(args['--config']))
        sys.stderr.write("Removed file.\n")
        return 0
    else:
        sys.stderr.write("Failed to remove file.\n")
        return 1


def save_files(config):
    # Loop through configured files.
    for tracked_file in config.tracked_files:
        tracked_file.save()


def restore_files(args, config):
    if not config.destination and not args['--destination']:
        sys.stderr.write("Where should I restore your settings from?.\n\nInclude a --destination argument, or set a default directory in your dotsync config.\n")
        return 1

    config.restore()
    return 0


def main(args):
    init_logging(args)

    # load config file
    config = Config.load(os.path.expanduser(args['--config']))

    if args['status']:
        return check_status(config)

    if args['add']:
        return add_file(args, config)
    elif args['remove']:
        return remove_file(args, config)

    # Bail out if no files configured
    if len(config.files) == 0:
        sys.stderr.write("No files configured.\n\nAdd one via the \"dotsync add\" command or by editing {0}\n".format(args['--config']))
        return 1

    if args['save']:
        return save_files(config)
    elif args['restore']:
        return restore_files(args, config)

    sys.stderr.write("Nothing to do.\n")  # shit.
    return 1
