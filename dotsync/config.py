import yaml
import os
import logging
from contextlib import closing
from ordereddict import OrderedDict

from .tracked_file import TrackedFile


class Config(object):
    @classmethod
    def load(cls, filename):
        # generate blank config if file does not exist
        if not os.path.exists(filename):
            return Config()

        with closing(open(filename, 'r')) as fp:
            data = yaml.load(fp) or {}

            defaults = data.get('defaults', {})
            default_destination = defaults.get('destination')

            tracked_files = []
            for index, tracked_file in enumerate(data.get('tracked_files', [])):
                tracked_file = TrackedFile(
                    source=tracked_file.get('source'),
                    destination=tracked_file.get('destination', default_destination)
                )

                if tracked_file.is_valid():
                    tracked_files.append(tracked_file)
                else:
                    logging.warn('Invalid file/folder: source=%s, destination=%s' % (str(tracked_file.source), str(tracked_file.destination)))

            return Config(tracked_files, default_destination)

    def __init__(self, tracked_files=None, default_destination=None):
        tracked_files = tracked_files or []
        self.tracked_files_by_source = OrderedDict()

        for tracked_file in tracked_files:
            self.tracked_files_by_source[tracked_file.source] = tracked_file

        self.default_destination = default_destination

    @property
    def tracked_files(self):
        return self.tracked_files_by_source.values()

    def add_file(self, source, destination):
        if source in self.tracked_files_by_source:
            tracked_file = self.tracked_files_by_source[source]

            return tracked_file.is_valid()

        # otherwise create
        tracked_file = TrackedFile(
            source=source,
            destination=destination
        )

        if tracked_file.is_valid():
            self.tracked_files_by_source[source] = tracked_file
            return True
        else:
            return False

    def remove_file(self, source):
        if source in self.tracked_files_by_source:
            del self.tracked_files_by_source[source]

            return True

        return False

    def __getstate__(self):
        output = {
            'tracked_files': [tracked_file.__getstate__() for tracked_file in self.tracked_files]
        }

        defaults = {}

        if self.default_destination:
            defaults['destination'] = self.default_destination

        if defaults:
            output['defaults'] = defaults

        return output

    def save(self, filename):
        with closing(open(filename, 'w')) as fp:
            fp.write(yaml.dump(self.__getstate__()))

    def restore(self):
        for tracked_file in self.tracked_files_by_source:
            tracked_file.restore()
