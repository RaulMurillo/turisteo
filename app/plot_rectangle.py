#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from PIL import Image, ImageDraw
import logging


def plot_rectangle(image, p0, p1, color='red'):
    """Plots rectangle in image.

    Args:
        image (str): Path of the original image.
        p0 (dict): Dict with keys 'x' and 'y' that indicates the first coordinate of the rectangle.
        p1 (dict): Dict with keys 'x' and 'y' that indicates the second coordinate of the rectangle.
    Returns:
        str: Path of the modified image.
    """
    # get the image
    img = Image.open(image).convert('RGB')
    # print(im.size)
    s = min(img.size)//100
    w = min(10, s)

    try:
        p0 = (p0['x'], p0['y'])
        p1 = (p1['x'], p1['y'])

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
    except KeyError:
        logging.warning('Bad points for rectangle.')
        new_img_name = image
    except:
        logging.warning('Unknown error.')
        new_img_name = image
    return new_img_name


if __name__ == '__main__':

    plot_rectangle('./geeks.png', (40, 40), (110, 110))
    plot_rectangle('./a.jpg', (565, 1018), (1488, 1555))
    plot_rectangle('./landmark.jpg', (192, 203), (975, 425))
