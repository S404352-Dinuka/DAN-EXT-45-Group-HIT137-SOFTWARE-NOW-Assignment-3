"""
Helper functions
"""

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