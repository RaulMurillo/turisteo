#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from PIL import (Image, ImageDraw, ImageFont)
import logging

def plot_rectangle(path, p0, p1):
    """Plots rectangle in image.
    
    Args:
        path (str): Path of the original image.
        p0 (tuple): Tuple of `(int, int)` that indicates the first coordinate of the rectangle.
        p1 (tuple): Tuple of `(int, int)` that indicates the secong coordinate of the rectangle.

    Returns:
        str: Path of the modified image.
    """    
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
    im_name = n[0]
    for i in range(1, len(n)-1):
        im_name += '.' + n[i]

    im_name += '_square.' + n[-1]
    logging.info(im_name)
    im.save(im_name) 
    return im_name


if __name__ == '__main__':

    plot_rectangle('./geeks.png', (40, 40), (110, 110))
    plot_rectangle('./a.jpg', (565, 1018), (1488, 1555))
    plot_rectangle('./landmark.jpg', (192, 203), (975, 425))
