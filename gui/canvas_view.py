"""
This module provides image display helper functions for the Tkinter GUI.

It converts OpenCV images into Tkinter compatible images and draws
difference circles on copies of the original and modified images.
"""

import cv2
from PIL import Image, ImageTk

from utils.constants import FOUND_COLOUR, REVEAL_COLOUR

class CanvasView:
    """
    This class handles image display operations for the game screen.
    """

    def draw_difference_circles(self, original_image, modified_image, differences):
        return original_image, modified_image

    def create_display_image(self, opencv_image, maximum_box_width, maximum_box_height):
        """
        This method prepares an OpenCV image for display in Tkinter.

        It resizes the image to fit inside the given display box while keeping
        the original aspect ratio. It then converts the resized OpenCV image into
        a Tkinter PhotoImage.

        :param opencv_image: The OpenCV image that needs to be displayed
        :param maximum_box_width: The maximum width allowed for the displayed image
        :param maximum_box_height: The maximum height allowed for the displayed image
        :return: A Tkinter PhotoImage and the scale value used during resizing
        """
        original_image_height = opencv_image.shape[0]
        original_image_width = opencv_image.shape[1]

        display_box_width = int(maximum_box_width)
        display_box_height = int(maximum_box_height)

        if display_box_width < 1:
            display_box_width = 1

        if display_box_height < 1:
            display_box_height = 1

        width_scale_ratio = display_box_width / original_image_width
        height_scale_ratio = display_box_height / original_image_height

        display_scale = min(width_scale_ratio, height_scale_ratio)

        if display_scale <= 0:
            raise ValueError("Display scale is invalid.")

        resized_image_width = int(original_image_width * display_scale)
        resized_image_height = int(original_image_height * display_scale)

        if resized_image_width < 1:
            resized_image_width = 1

        if resized_image_height < 1:
            resized_image_height = 1

        if display_scale < 1:
            resize_interpolation_method = cv2.INTER_AREA
        else:
            resize_interpolation_method = cv2.INTER_LINEAR

        resized_opencv_image = cv2.resize(
            opencv_image,
            (resized_image_width, resized_image_height),
            interpolation=resize_interpolation_method
        )

        rgb_display_image = cv2.cvtColor(resized_opencv_image, cv2.COLOR_BGR2RGB)
        pillow_image = Image.fromarray(rgb_display_image)
        tkinter_photo_image = ImageTk.PhotoImage(pillow_image)

        return tkinter_photo_image, display_scale