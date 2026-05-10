"""
This module contains the image loading logic for the application
It validates the selected image file format and loads the image using OpenCV
"""

import cv2
import os
from utils.status_messages import ImageFileExtension, StatusMessage


class ImageLoader:
    """
    This class handles image file loading
    """

    def __init__(self):
        """
        This method initializes the image loader with supported image formats
        """
        self.formats = [
            ImageFileExtension.JPG.value,
            ImageFileExtension.JPEG.value,
            ImageFileExtension.PNG.value,
            ImageFileExtension.BMP.value
        ]
        self.img_path = None

    def load_img(self, filePath):
        """
        This method loads an image from the given file path

        :param filePath:path of the image file
        :return: Loaded image if successful, otherwise a ValueError object
        """
        self.img_path = filePath
        file_type = os.path.splitext(filePath)[1].lower()

        if file_type in self.formats:
            img = cv2.imread(filePath)

            if img is None:
                return ValueError(StatusMessage.IMAGE_COULD_NOT_BE_LOADED.value)

            return img