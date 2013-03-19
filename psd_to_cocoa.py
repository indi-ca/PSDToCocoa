"""PSDToCocoa.

Translates PSD groups and layers into Cocoa UI elements.
A naming convention is necessary. This implementation
builds on top of the Slicy App's naming convention.

The PSD is assumed to be in 2x resolution.

img_    tag for an UIImageView
    assumes that there is a @2x in it

Usage:
   psd_to_cocoa.py process <psd>
   psd_to_cocoa.py input <file>     processes PSDs found in a file. TODO

Options:
    -h --help     Show this screen.
    --version     Show version.

"""

# https://github.com/kmike/psd-tools
import re
from renderers.ios import iOSRenderer

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
        self.renderer = iOSRenderer()
        # print(self.arguments)
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

    def process(self):
        psd_file = self.arguments['<psd>']
        psd = PSDImage.load(psd_file)
        print psd.header
        print psd.layers

        source_bbox = psd.bbox

        for item in psd.layers:
            if item.visible:
                self.encode(item, source_bbox)

    def encode(self, item, source_bbox):
        match = re.search(r".*img_.*", item.name)
        if match:
            self.renderer.render_image(item, source_bbox)

        match = re.search(r".*btn_.*", item.name)
        if match:
            self.renderer.render_button(item, source_bbox)

        match = re.search(r".*view_.*", item.name)
        if match:
            self.renderer.render_view(item, source_bbox)

        match = re.search(r".*label_.*", item.name)
        if match:
            self.renderer.render_label(item, source_bbox)

        source_bbox = item.bbox
        if isinstance(item, Group):
            for child_item in item.layers:
                if child_item.visible:
                    self.encode(child_item, source_bbox)

    def display(self, item, source_bbox):
        print "\n\n"
        print item.name
        self.translate(item, source_bbox)

    def translate(self, item, source_bbox):
        d = 2

        bbox = item.bbox
        # Seems as though the bounding box is 1px larger than the layer
        origin_x = bbox.x1 / d
        origin_y = bbox.y1 / d

        source_origin_x = source_bbox.x1 / d
        source_origin_y = source_bbox.y1 / d

        width_1x = bbox.width / d
        height_1x = bbox.height / d

        print "Absolute: CGRectMake({0}, {1}, {2}, {3})".format(origin_x,
                                                                origin_y,
                                                                width_1x,
                                                                height_1x)

        relative = (
            origin_x - source_origin_x, origin_y - source_origin_y, width_1x,
            height_1x)
        print "Relative: CGRectMake({0}, {1}, {2}, {3})".format(
            origin_x - source_origin_x, origin_y - source_origin_y,
            width_1x, height_1x)

        print "Width: %s" % width_1x
        print "Height: %s" % height_1x
        return relative


if __name__ == "__main__":
    print "Running PSDToCocoa in stand-alone-mode"
    psd_to_cocoa = PSDToCocoa()
    psd_to_cocoa.process()

