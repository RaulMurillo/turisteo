#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from PIL import Image, ImageDraw, ImageFont


def plot_rectangle(path, p0, p1):
    """Plots rectangle in image."""

    # get the image
    im = Image.open(path).convert('RGB')
    # print(im.size)
    s = min(im.size)//100
    w = min(10, s)

    draw = ImageDraw.Draw(im)
    draw.rectangle((p0, p1), outline="#ff0000", width=w)
    del draw

    # im.show()
    n = path.split('.')
    name = n[0]
    for i in range(1, len(n)-1):
        name += '.' + n[i]

    name += '_square.' + n[-1]
    # print(name)
    im.save(name)


if __name__ == '__main__':

    plot_rectangle('./resources/img1.jpg', (565, 1018), (1488, 1555))
    plot_rectangle('./resources/img2.jpg', (1760, 1329), (1941, 2008))
    plot_rectangle('./resources/img3.jpg', (192, 203), (975, 425))
