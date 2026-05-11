"""
Helper functions
"""
from utils.constants import DIFFERENCE_CIRCLE_EXTRA_RADIUS

def get_file_extension(file_path):
    """
    This method returns the lowercase file extension, such as .jpg or .png

    :param file_path: path of the file
    :return:
    """
    dot_index = file_path.rfind(".")
    if dot_index == -1:
        extension = ""
    else:
        extension = file_path[dot_index:]
    return extension.lower()


def get_image_size(image):
    """
    This method returns image width and height from an OpenCV image
    :param image: image file
    :return:
    """
    height = image.shape[0]
    width = image.shape[1]
    return width, height

def calculate_difference_circle_radius(difference):
    """
    Calculates the circle radius used to mark a difference region.

    :param difference:Difference region containing width and height values
    :return: The calculated circle radius
    """
    half_width = difference.width / 2
    half_height = difference.height / 2

    corner_distance_from_center = (
        half_width * half_width
        + half_height * half_height
    ) ** 0.5

    circle_radius = int(
        corner_distance_from_center
        + DIFFERENCE_CIRCLE_EXTRA_RADIUS
    )

    return circle_radius