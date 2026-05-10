"""
This module contains image alteration classes used to create visible differences
"""

import cv2
from utils.constants import (
    BLUR_KERNEL_SIZE,
    BRIGHTNESS_CHANGE_BETA,
    PIXELATE_SCALE_DOWN_FACTOR,
    HUE_SHIFT_VALUE,
    SATURATION_SHIFT_VALUE,
    BLUR_EDGE_THRESHOLD_HIGH,
    BLUR_EDGE_THRESHOLD_LOW,
    MIN_BLUR_EDGE_DENSITY,
    PLAIN_REGION_BLUR_BRIGHTNESS_CHANGE,
    PLAIN_REGION_BRIGHTNESS_THRESHOLD,
    CONTRAST_EFFECT_ALPHA,
    CONTRAST_EFFECT_BETA,
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

        selected_area = img[y:y + h, x:x + w]

        hsv_area = cv2.cvtColor(selected_area, cv2.COLOR_BGR2HSV)

        hue_channel = hsv_area[:, :, 0].astype("int16")
        shifted_hue_channel = (hue_channel + HUE_SHIFT_VALUE) % 180
        hsv_area[:, :, 0] = shifted_hue_channel.astype("uint8")

        hsv_area[:, :, 1] = cv2.add(
            hsv_area[:, :, 1],
            SATURATION_SHIFT_VALUE
        )

        changed_area = cv2.cvtColor(hsv_area, cv2.COLOR_HSV2BGR)

        img[y:y + h, x:x + w] = changed_area

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

        grey_area = cv2.cvtColor(selected_area, cv2.COLOR_BGR2GRAY)

        edge_image = cv2.Canny(
            grey_area,
            BLUR_EDGE_THRESHOLD_LOW,
            BLUR_EDGE_THRESHOLD_HIGH
        )

        edge_density = cv2.countNonZero(edge_image) / edge_image.size

        blurred_area = cv2.GaussianBlur(
            selected_area,
            (BLUR_KERNEL_SIZE, BLUR_KERNEL_SIZE),
            0
        )

        if edge_density < MIN_BLUR_EDGE_DENSITY:
            if blurred_area.mean() > PLAIN_REGION_BRIGHTNESS_THRESHOLD:
                blurred_area = cv2.subtract(
                    blurred_area,
                    PLAIN_REGION_BLUR_BRIGHTNESS_CHANGE
                )
            else:
                blurred_area = cv2.add(
                    blurred_area,
                    PLAIN_REGION_BLUR_BRIGHTNESS_CHANGE
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
            interpolation=cv2.INTER_LINEAR
        )

        pixelated_area = cv2.resize(
            small_area,
            (w, h),
            interpolation=cv2.INTER_NEAREST
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