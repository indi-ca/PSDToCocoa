"""PSDToCocoa.

Translates PSD groups and layers into Cocoa UI elements.
A naming convention is necessary. This implementation
builds on top of the Slicy App's naming convention.

Usage:
   psd_to_cocoa.py process <psd>

Options:
    -h --help     Show this screen.
    --version     Show version.

"""

# https://github.com/kmike/psd-tools


__author__ = "Indika Piyasena"

from docopt import docopt
from psd_tools import PSDImage
from psd_tools import Layer, Group

import logging

# logger = logging.getLogger("psd_tools")
logger = logging.getLogger(__name__)

class PSDToCocoa:
    def __init__(self):
        self.configure_logging()
        self.arguments = docopt(__doc__, version='PSDToCocoa 0.1')
        print(self.arguments)
        pass

    def process(self):
        psd_file = self.arguments['<psd>']
        psd = PSDImage.load(psd_file)
        print psd.header

        print psd.layers

        for item in psd.layers:
            if item.visible:
                self.encode(item)


        pass

    def translate(self, bbox):
        origin_x = (bbox.x1 + 2) / 2
        origin_y = (bbox.y1 + 2) / 2

        width_1x = (bbox.width - 2) / 2
        height_1x = (bbox.height - 2) / 2

        print "CGRectMake({0}, {1}, {2}, {3})".format(origin_x, origin_y, width_1x, height_1x)
        print "Width: %s" % width_1x
        print "Height: %s" % height_1x
        pass

    def configure_logging(self):
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        pass

    def encode(self, item):
        if item.name[:4] == 'view':
            self.display(item)

        if item.name[-7:] == '@2x.png':
            self.display(item)

        if isinstance(item, Group):
            for item in item.layers:
                if item.visible:
                    self.encode(item)

    def display(self, item):
        print "\n\n"
        print item.name
        self.translate(item.bbox)

    pass


if __name__ == "__main__":
    print "Running PSDToCocoa in stand-alone-mode"
    psd_to_cocoa = PSDToCocoa()
    psd_to_cocoa.process()

