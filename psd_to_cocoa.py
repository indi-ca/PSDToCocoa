"""PSDToCocoa.

Translates PSD groups and layers into Cocoa UI elements.
A naming convention is necessary. This implementation
builds on top of the Slicy App's naming convention.

The PSD is assumed to be in 2x resolution.

img_    tag for an UIImageView
    assumes that there is a @2x in it

Usage:
   psd_to_cocoa.py <psd>

Options:
    -h --help     Show this screen.
    --version     Show version.

"""

# https://github.com/kmike/psd-tools
import os
import re

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
            self.render_image(item, source_bbox)

        if item.name[:4] == 'view':
            self.render_view(item, source_bbox)

        if item.name[:4] == 'image':
            self.render_image(item, source_bbox)

        # if item.name[-7:] == '@2x.png':


        source_bbox = item.bbox
        if isinstance(item, Group):
            for child_item in item.layers:
                if child_item.visible:
                    self.encode(child_item, source_bbox)

    def display(self, item, source_bbox):
        print "\n\n"
        print item.name
        self.translate(item.bbox, source_bbox)

    def render_view(self, item, source_bbox):
        print "\n\n"
        print item.name
        self.translate(item.bbox, source_bbox)

    def render_image(self, item, source_bbox):
        print "\n\nImage"
        print item.name
        dim = self.translate(item.bbox, source_bbox)

        basename = os.path.basename(item.name)
        just_filename = os.path.splitext(basename)[0][:-3]

        CGRect = "({0}, {1}, {2}, {3})".format(dim[0], dim[1], dim[2], dim[3])
        print CGRect
        print "{0} = [[UIImageView alloc] initWithFrame:CGRectMake{1}];".format(
            just_filename, CGRect)
        print '[{0} setImage:[UIImage imageNamed:@"hypbp_img_title.png"]];'.format(
            just_filename, just_filename + '.png')

        # hypbp_img_title = [[UIImageView alloc] initWithFrame:CGRectMake(0, 0, 618, 75)];
        # [hypbp_img_title setImage:[UIImage imageNamed:@"hypbp_img_title.png"]];


    def translate(self, bbox, source_bbox):
        d = 2

        # Seems as though the bounding box is 1px larger than the layer
        origin_x = (bbox.x1 + 1) / d
        origin_y = (bbox.y1 + 1) / d

        source_origin_x = (source_bbox.x1 + 1) / d
        source_origin_y = (source_bbox.y1 + 1) / d

        width_1x = (bbox.width - 2) / d
        height_1x = (bbox.height - 2) / d

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

