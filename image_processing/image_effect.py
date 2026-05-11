"""
This module contains image alteration classes used to create visible differences
"""

import cv2
from utils.constants import (
    BLUR_KERNEL_SIZE,
    BRIGHTNESS_CHANGE_BETA,
    BRIGHTNESS_EFFECT_BLEND_WEIGHT,
    PIXELATE_SCALE_DOWN_FACTOR,
    PIXELATE_VISIBILITY_ALPHA,
    PIXELATE_VISIBILITY_BETA,
    CONTRAST_EFFECT_ALPHA,
    CONTRAST_EFFECT_BETA,
    COLOUR_EFFECT_BLEND_WEIGHT,
    COLOUR_HUE_SHIFT_VALUE,
    COLOUR_SATURATION_SHIFT_VALUE,
    GREYSCALE_EFFECT_BLEND_WEIGHT
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
        :param area: selected difference area containing x, y, width, and height
        :return:modified image
        """
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        original_area = img[y:y + h, x:x + w].copy()

        hsv_area = cv2.cvtColor(original_area, cv2.COLOR_BGR2HSV)

        hue_channel = hsv_area[:, :, 0].astype("int16")
        shifted_hue_channel = (hue_channel + COLOUR_HUE_SHIFT_VALUE) % 180
        hsv_area[:, :, 0] = shifted_hue_channel.astype("uint8")

        hsv_area[:, :, 1] = cv2.add(
            hsv_area[:, :, 1],
            COLOUR_SATURATION_SHIFT_VALUE
        )

        changed_area = cv2.cvtColor(hsv_area, cv2.COLOR_HSV2BGR)

        blended_area = cv2.addWeighted(
            original_area,
            1 - COLOUR_EFFECT_BLEND_WEIGHT,
            changed_area,
            COLOUR_EFFECT_BLEND_WEIGHT,
            0
        )

        img[y:y + h, x:x + w] = blended_area

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

        selected_area = img[y:y + h, x:x + w]

        blurred_area = cv2.GaussianBlur(
            selected_area,
            (BLUR_KERNEL_SIZE, BLUR_KERNEL_SIZE),
            0
        )

        img[y:y + h, x:x + w] = blurred_area

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

        original_area = img[y:y + h, x:x + w].copy()

        bright_area = cv2.convertScaleAbs(
            original_area,
            alpha=1.0,
            beta=BRIGHTNESS_CHANGE_BETA
        )

        blended_area = cv2.addWeighted(
            original_area,
            1 - BRIGHTNESS_EFFECT_BLEND_WEIGHT,
            bright_area,
            BRIGHTNESS_EFFECT_BLEND_WEIGHT,
            0
        )

        img[y:y + h, x:x + w] = blended_area

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

        original_area = img[y:y + h, x:x + w].copy()

        grey_area = cv2.cvtColor(original_area, cv2.COLOR_BGR2GRAY)
        grey_area_bgr = cv2.cvtColor(grey_area, cv2.COLOR_GRAY2BGR)

        blended_area = cv2.addWeighted(
            original_area,
            1 - GREYSCALE_EFFECT_BLEND_WEIGHT,
            grey_area_bgr,
            GREYSCALE_EFFECT_BLEND_WEIGHT,
            0
        )

        img[y:y + h, x:x + w] = blended_area
        return img

class PixelateEffect(ImageEffect):
    """
    This class applies a pixelation effect to a selected image area
    """

    def apply(self, img, area):
        """
        Pixelates the selected image area by resizing it down and back up

        :param img: The image that will be modified
        :param area: The selected difference area
        :return: The modified image
        """
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        selected_area = img[y:y + h, x:x + w]

        small_width = max(1, w // PIXELATE_SCALE_DOWN_FACTOR)
        small_height = max(1, h // PIXELATE_SCALE_DOWN_FACTOR)

        small_area = cv2.resize(
            selected_area,
            (small_width, small_height),
            interpolation=cv2.INTER_AREA
        )

        pixelated_area = cv2.resize(
            small_area,
            (w, h),
            interpolation=cv2.INTER_NEAREST
        )

        pixelated_area = cv2.convertScaleAbs(
            pixelated_area,
            alpha=PIXELATE_VISIBILITY_ALPHA,
            beta=PIXELATE_VISIBILITY_BETA
        )

        img[y:y + h, x:x + w] = pixelated_area

        return img

class ContrastEffect(ImageEffect):
    """
    This class applies a contrast change to a selected image area
    """

    def apply(self, img, area):
        """
        This method increases the contrast of the selected image area.

        :param img: Image that will be modified
        :param area: The selected difference area containing x, y, width, and height
        :return: Modified image
        """
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        selected_area = img[y:y + h, x:x + w]

        contrast_area = cv2.convertScaleAbs(
            selected_area,
            alpha=CONTRAST_EFFECT_ALPHA,
            beta=CONTRAST_EFFECT_BETA
        )

        img[y:y + h, x:x + w] = contrast_area

        return img