"""
This module contains image alteration classes used to create visible differences
Each alteration class applies a different OpenCV-based change to a selected image region
"""

import cv2


class Alterations:
    """
    This class is the base class for all image alteration types
    Child classes override the apply method to change a selected image region in different ways
    """

    def __init__(self):
        """
        This method initializes the base alteration object.
        """
        pass

    def apply(self, img, area):
        """
        This method applies an alteration to a selected image area
        This base method is intended to be overridden by child classes

        :param img: The OpenCV image that will be modified
        :param area: The selected difference area containing x, y, width, and height
        :return: The modified OpenCV image
        """
        pass


class Color_Change(Alterations):
    """
    This class applies a colour change to a selected image area
    It uses OpenCV to increase the blue colour channel inside the selected region
    """

    def apply(self, img, area):
        """
        This method changes the colour of the selected image area
        It selects the region using the area coordinates and increases
        the blue channel value to create a visible difference

        :param img: The OpenCV image that will be modified
        :param area: The selected difference area containing x, y, width, and height
        :return: The modified OpenCV image
        """
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        new_area = img[y:y + h, x:x + w]
        new_area[:, :, 0] = cv2.add(new_area[:, :, 0], 50)
        img[y:y+h, x:x+w] = new_area
        return img


class Blur_Change(Alterations):
    """
    This class applies a blur effect to a selected image area
    It uses OpenCV Gaussian blur to make the selected region look different from the original image
    """

    def apply(self, img, area):
        """
        This method blurs the selected image area
        It selects the region using the area coordinates and applies a Gaussian blur with a fixed kernel size

        :param img: The OpenCV image that will be modified
        :param area: The selected difference area containing x, y, width, and height
        :return: The modified OpenCV image
        """
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        new_area = img[y:y + h, x:x + w]
        blur_area = cv2.GaussianBlur(new_area, (17, 17), 0)
        img[y:y+h, x:x+w] = blur_area
        return img


class Change_Brightness(Alterations):
    """
    This class changes the brightness of a selected image area
    It uses OpenCV to increase the brightness while keeping the contrast value unchanged
    """

    def apply(self, img, area):
        """
        This method increases the brightness of the selected image area
        It selects the region using the area coordinates and applies
        convertScaleAbs with alpha as contrast and beta as brightness

        :param img: The OpenCV image that will be modified
        :param area: The selected difference area containing x, y, width, and height
        :return: The modified OpenCV image
        """
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        new_area = img[y:y + h, x:x + w]
        bright_area = cv2.convertScaleAbs(new_area, alpha=1.0, beta=20)
        img[y:y+h, x:x+w] = bright_area
        return img


class Change_GreyScale(Alterations):
    """
    This class converts a selected image area into greyscale
    It converts the selected region to greyscale and then converts it back to BGR
    so it can be placed back into the original color image
    """

    def apply(self, img, area):
        """
        This method applies a greyscale effect to the selected image area
        It selects the region using the area coordinates, converts it to greyscale,
        and converts it back to BGR format before updating the original image

        :param img: The OpenCV image that will be modified
        :param area: The selected difference area containing x, y, width, and height
        :return: The modified OpenCV image
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