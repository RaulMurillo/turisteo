#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from PIL import Image, ImageDraw
import logging


def plot_rectangle(image, p0, p1, color='red'):
    """Plots rectangle in image.

    Args:
        image (str): Path of the original image.
        p0 (tuple): Tuple of `(int, int)` that indicates the first coordinate of the rectangle.
        p1 (tuple): Tuple of `(int, int)` that indicates the secong coordinate of the rectangle.
    Returns:
        str: Path of the modified image.
    """
    # get the image
    img = Image.open(image).convert('RGB')
    # print(im.size)
    s = min(img.size)//100
    w = min(10, s)

    draw = ImageDraw.Draw(img)
    draw.rectangle((p0, p1), fill=None, outline=color, width=w)
    del draw

    # img.show()
    img_name, extension = image.rsplit('.', 1)
    # img_name = n[0]
    # for i in range(1, len(n)-1):
    #     img_name += '.' + n[i]

    new_img_name = img_name + '_square.' + extension
    logging.info(new_img_name)
    img.save(new_img_name)
    return new_img_name


if __name__ == '__main__':

    plot_rectangle('./geeks.png', (40, 40), (110, 110))
    plot_rectangle('./a.jpg', (565, 1018), (1488, 1555))
    plot_rectangle('./landmark.jpg', (192, 203), (975, 425))
