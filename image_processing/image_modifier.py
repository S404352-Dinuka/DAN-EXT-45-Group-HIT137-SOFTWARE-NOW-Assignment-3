"""
This module contains the image modification logic for the game
It creates random non overlapping difference areas, applies different
OpenCV-based alterations to those areas, and stores the generated difference regions for click detection
"""

import random
import cv2
from image_processing.alterations import Color_Change
from image_processing.alterations import Blur_Change
from image_processing.alterations import Change_Brightness
from image_processing.alterations import Change_GreyScale
from core.difference import Difference
from utils.status_messages import AlterationType
from utils.constants import (
    MAX_DIFFERENCE_AREA_SIZE_DIVISOR,
    MIN_DIFFERENCE_AREA_SIZE_DIVISOR,
    NUMBER_OF_DIFFERENCES,
)

class ImageModifiier:
    """
    This class creates the modified version of the selected image
    It generates random difference areas, checks that they do not overlap,
    applies different alteration types, and stores the final difference list.
    """

    def __init__(self):
        """
        This method initializes the image modifier with default alteration values
        It stores the number of differences, the list of created differences,
        the available alteration types, and the alteration objects.
        """
        self.count_diff = NUMBER_OF_DIFFERENCES
        self.diff = []
        self.diff_types = [
            AlterationType.BLUR.value,
            AlterationType.COLOUR_SHIFT.value,
            AlterationType.BRIGHTNESS.value,
            AlterationType.GREY_SHIFT.value
        ]
        self.color_change = Color_Change()
        self.blur_change = Blur_Change()
        self.change_brightness = Change_Brightness()
        self.change_greyscale = Change_GreyScale()

    def copy_img(self, img):
        """
        This method creates a copy of the original image and applies alterations to it

        :param img: The original OpenCV image
        :return: The altered copy of the original image
        """
        altered_img = img.copy()
        self.create_alterations(altered_img)
        final_altered_img = self.apply_alterations(altered_img)
        return final_altered_img

    def create_alterations(self, img):
        """
        This method creates random difference areas inside the image
        It generates random area sizes, positions, and alteration types
        It continues until the required number of non-overlapping difference
        areas has been created

        :param img: The OpenCV image used to calculate valid difference areas.
        :return: The list of generated difference areas.
        """
        img_heignt, img_width = self.img_dimensions(img)
        self.diff = []

        while len(self.diff) < self.count_diff:
            area_width = random.randint(
                img_width // MIN_DIFFERENCE_AREA_SIZE_DIVISOR,
                img_width // MAX_DIFFERENCE_AREA_SIZE_DIVISOR
            )
            area_height = random.randint(
                img_heignt // MIN_DIFFERENCE_AREA_SIZE_DIVISOR,
                img_heignt // MAX_DIFFERENCE_AREA_SIZE_DIVISOR
            )
            area_x = random.randint(0, (img_width - area_width))
            area_y = random.randint(0, (img_heignt - area_height))
            area_type_no = random.randint(0, len(self.diff_types) - 1)
            area_type = self.diff_types[area_type_no]
            new_area = Difference(
                x=area_x,
                y=area_y,
                width=area_width,
                height=area_height,
                alteration_name=area_type,
                found=False
            )

            check_overlap = self.check_area_overlap(new_area)
            if check_overlap == False:
                self.diff.append(new_area)

        return self.diff

    def check_area_overlap(self, new_area):
        """
        This method checks whether a new difference area overlaps with an existing area

        :param new_area: The newly created difference area that needs to be checked
        :return: True if the new area overlaps with an existing area, otherwise False
        """
        for area in self.diff:
            new_left = new_area.x
            new_right = new_area.x + new_area.width
            new_top = new_area.y
            new_bottom = new_area.y + new_area.height

            area_left = area.x
            area_right = area.x + area.width
            area_top = area.y
            area_bottom = area.y + area.height

            if new_top > area_bottom or new_bottom < area_top:
                continue
            elif new_left > area_right or new_right < area_left:
                continue
            return True
        return False

    def apply_alterations(self, img):
        """
        This method applies the selected alteration type to each difference area

        It checks the alteration name stored in each difference area and applies
        the matching OpenCV alteration to the image

        :param img: The OpenCV image that will be altered
        :return: The OpenCV image after all alterations have been applied
        """
        for area in self.diff:
            if area.alteration_name == AlterationType.BLUR.value:
                img = self.blur_change.apply(img, area)

            elif area.alteration_name == AlterationType.COLOUR_SHIFT.value:
                img = self.color_change.apply(img, area)

            elif area.alteration_name == AlterationType.BRIGHTNESS.value:
                img = self.change_brightness.apply(img, area)

            elif area.alteration_name == AlterationType.GREY_SHIFT.value:
                img = self.change_greyscale.apply(img, area)
        return img

    def get_alterations(self):
        """
        This method returns the list of generated difference areas

        :return: The list of difference areas created for the current image
        """
        return self.diff

    def img_dimensions(self, img):
        """
        This method returns the height and width of the image

        :param img: The OpenCV image
        :return: The image height and width
        """
        height = img.shape[0]
        width = img.shape[1]
        return height, width

    def convert_to_rgb(self, img):
        """
        This method converts an OpenCV image from BGR format to RGB format

        :param img: The OpenCV image in BGR color format.
        :return: The converted image in RGB color format.
        """
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return rgb_img