"""
This module contains the image modification logic for the game
"""

import random
import cv2
from image_processing.image_effect import ColourEffect
from image_processing.image_effect import BlurEffect
from image_processing.image_effect import BrightnessEffect
from image_processing.image_effect import GreyscaleEffect
from image_processing.image_effect import PixelateEffect
from image_processing.image_effect import ContrastEffect
from core.difference import Difference
from utils.status_messages import ImageEffectType
from utils.constants import (
    MAX_DIFFERENCE_AREA_SIZE_DIVISOR,
    MIN_DIFFERENCE_AREA_SIZE_DIVISOR,
    NUMBER_OF_DIFFERENCES,
    MIN_REGION_DETAIL_SCORE
)

class ModifiedImageBuilder:
    """
    This class creates the modified version of the selected image
    """

    def __init__(self):
        """
        This method initializes the image modifier with default alteration values
        """
        self.count_diff = NUMBER_OF_DIFFERENCES
        self.diff = []
        self.diff_types = [
            ImageEffectType.BLUR.value,
            ImageEffectType.COLOUR_SHIFT.value,
            ImageEffectType.BRIGHTNESS.value,
            ImageEffectType.GREY_SHIFT.value,
            ImageEffectType.PIXELATE.value,
            ImageEffectType.CONTRAST.value
        ]
        self.color_effect = ColourEffect()
        self.blur_effect = BlurEffect()
        self.brightness_effect = BrightnessEffect()
        self.greyscale_effect = GreyscaleEffect()
        self.pixelate_effect = PixelateEffect()
        self.contrast_effect = ContrastEffect()

    def copy_img(self, img):
        """
        This method creates a copy of the original image and applies alterations to it

        :param img: original image
        :return: altered copy of the original image
        """
        altered_img = img.copy()
        self.create_alterations(altered_img)
        final_altered_img = self.apply_alterations(altered_img)
        return final_altered_img

    def create_alterations(self, img):
        """
        This method creates random difference areas inside the image

        :param img: image used to calculate valid difference areas
        :return: list of generated difference areas
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
            has_detail = self.has_enough_visual_detail(img, new_area)

            if not check_overlap and has_detail:
                self.diff.append(new_area)

        return self.diff

    def check_area_overlap(self, new_area):
        """
        This method checks whether a new difference area overlaps with an existing area

        :param new_area: created difference area that needs to be checked
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

        :param img: image that will be altered
        :return: image after all alterations have been applied
        """
        for area in self.diff:
            if area.alteration_name == ImageEffectType.BLUR.value:
                img = self.blur_effect.apply(img, area)

            elif area.alteration_name == ImageEffectType.COLOUR_SHIFT.value:
                img = self.color_effect.apply(img, area)

            elif area.alteration_name == ImageEffectType.BRIGHTNESS.value:
                img = self.brightness_effect.apply(img, area)

            elif area.alteration_name == ImageEffectType.GREY_SHIFT.value:
                img = self.greyscale_effect.apply(img, area)

            elif area.alteration_name == ImageEffectType.PIXELATE.value:
                img = self.pixelate_effect.apply(img, area)

            elif area.alteration_name == ImageEffectType.CONTRAST.value:
                img = self.contrast_effect.apply(img, area)
        return img

    def get_alterations(self):
        """
        This method returns the list of generated difference areas

        :return: list of difference areas created for the current image
        """
        return self.diff

    def img_dimensions(self, img):
        """
        This method returns the height and width of the image

        :param img: OpenCV image
        :return: image height and width
        """
        height = img.shape[0]
        width = img.shape[1]
        return height, width

    def has_enough_visual_detail(self, img, area):
        """
        Checks whether the selected image area has enough texture or colour variation.

        :param img: OpenCV image
        :param area: Difference area containing x, y, width, and height
        :return: True if the selected area has enough visual detail, otherwise False
        """
        selected_area = img[
            area.y:area.y + area.height,
            area.x:area.x + area.width
        ]

        grey_area = cv2.cvtColor(selected_area, cv2.COLOR_BGR2GRAY)
        detail_score = grey_area.std()

        return detail_score >= MIN_REGION_DETAIL_SCORE