import logging
import os


class TrackedFile(object):
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def is_valid(self):
        return self.source and self.destination

    def is_saved(self):
        # Not yet implemented
        return False

    def save(self):
        if not os.path.exists(self.destination) or not os.path.isdir(self.destination):
            os.mkdir(self.destination)
            logging.info('Created a new directory for your tracked files at %s', self.destination)

        # TODO: Figure out how to copy shit
        os.mv(self.source, self.destination)
        os.symlink(self.source, self.destination)
        os.remove(self.source)

        logging.info("Successfully copied and symlink'd %s to %s", self.source, self.destination)

    def __getstate__(self):
        return {
            'source': self.source,
            'destination': self.destination
        }
