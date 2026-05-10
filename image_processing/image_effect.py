"""
This module contains image alteration classes used to create visible differences
"""

import cv2
from utils.constants import (
    BLUR_KERNEL_SIZE,
    BRIGHTNESS_CHANGE_BETA,
    COLOUR_CHANGE_BLUE_INCREMENT,
)


class ImageEffect:
    """
    This class is the base class for all image alteration types
    """

    def __init__(self):
        """
        This method initializes the base alteration object.
        """
        pass

    def apply(self, img, area):
        """
        This method applies an alteration to a selected image area

        :param img:image that will be modified
        :param area: The selected difference area containing x, y, width, and height
        :return:modified image
        """
        pass


class ColourEffect(ImageEffect):
    """
    This class applies a color change to a selected image area
    """

    def apply(self, img, area):
        """
        This method changes the color of the selected image area

        :param img: image that will be modified
        :param area:elected difference area containing x, y, width, and height
        :return:modified image
        """
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        new_area = img[y:y + h, x:x + w]
        new_area[:, :, 0] = cv2.add(new_area[:, :, 0], COLOUR_CHANGE_BLUE_INCREMENT)
        img[y:y+h, x:x+w] = new_area
        return img


class BlurEffect(ImageEffect):
    """
    This class applies a blur effect to a selected image area
    """

    def apply(self, img, area):
        """
        This method blurs the selected image area

        :param img:image that will be modified
        :param area:selected difference area containing x, y, width, and height
        :return:modified image
        """
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        new_area = img[y:y + h, x:x + w]
        blur_area = cv2.GaussianBlur(new_area, (BLUR_KERNEL_SIZE, BLUR_KERNEL_SIZE), 0)
        img[y:y+h, x:x+w] = blur_area
        return img


class BrightnessEffect(ImageEffect):
    """
    This class changes the brightness of a selected image area
    """

    def apply(self, img, area):
        """
        This method increases the brightness of the selected image area

        :param img: image that will be modified
        :param area:selected difference area containing x, y, width, and height
        :return:modified image
        """
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        new_area = img[y:y + h, x:x + w]
        bright_area = cv2.convertScaleAbs(new_area, alpha=1.0, beta=BRIGHTNESS_CHANGE_BETA)
        img[y:y+h, x:x+w] = bright_area
        return img


class GreyscaleEffect(ImageEffect):
    """
    This class converts a selected image area into greyscale
    """

    def apply(self, img, area):
        """
        This method applies a greyscale effect to the selected image area

        :param img:image that will be modified
        :param area:selected difference area containing x, y, width, and height
        :return:modified image
        """
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        new_area = img[y:y + h, x:x + w]
        grey_area = cv2.cvtColor(new_area, cv2.COLOR_BGR2GRAY)
        grey_area_bgr = cv2.cvtColor(grey_area, cv2.COLOR_GRAY2BGR)
        img[y:y+h, x:x+w] = grey_area_bgr
        return img