import os

__author__ = "Indika Piyasena"


class iOSRenderer:
    def __init__(self):
        pass

    def render_view(self, item, source_bbox):
        print "\n\n"
        print item.name
        dim = self.translate(item, source_bbox)
        print "H:|-{0}-[{1}({2})]".format(dim[0], item.name, dim[2])
        print "V:|-{0}-[{1}({2})]".format(dim[1], item.name, dim[3])

    def render_label(self, item, source_bbox):
        print "\n\n"
        print item.name
        dim = self.translate(item, source_bbox)
        print "H:|-{0}-[{1}({2})]".format(dim[0], item.name, dim[2])
        print "V:|-{0}-[{1}({2})]".format(dim[1], item.name, dim[3])

    def render_image(self, item, source_bbox):
        print "\n\n* Image"
        print item.name
        dim = self.translate(item, source_bbox)

        basename = os.path.basename(item.name)
        just_filename = os.path.splitext(basename)[0][:-3]

        CGRect = "({0}, {1}, {2}, {3})".format(dim[0], dim[1], dim[2], dim[3])
        print CGRect
        print "{0} = [[UIImageView alloc] initWithFrame:CGRectMake{1}];".format(
            just_filename, CGRect)
        print '[{0} setImage:[UIImage imageNamed:@"{1}"]];'.format(
            just_filename, just_filename + '.png')
        print '@"H:|-{0}-[{1}({2})]",'.format(dim[0], just_filename, dim[2])
        print '@"V:|-{0}-[{1}({2})]",'.format(dim[1], just_filename, dim[3])


    def render_button(self, item, source_bbox):
        print "\n\n* Button"
        print item.name
        dim = self.translate(item.bbox, source_bbox)

        basename = os.path.basename(item.name)
        just_filename = os.path.splitext(basename)[0][:-3]

        CGRect = "({0}, {1}, {2}, {3})".format(dim[0], dim[1], dim[2], dim[3])
        print CGRect
        print "{0} = [[UIButton alloc] initWithFrame:CGRectMake{1}];".format(
            just_filename, CGRect)
        print '[{0} setImage:[UIImage imageNamed:@"{1}"] forState:UIControlStateNormal];'.format(
            just_filename, just_filename + '.png')
        print '[{0} setImage:[UIImage imageNamed:@"{1}"] forState:UIControlStateHighlighted];'.format(
            just_filename, just_filename + '.png')

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
    print "Running iOSRenderer in stand-alone-mode"

    ios_renderer = iOSRenderer()
