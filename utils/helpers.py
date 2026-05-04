"""
Helper functions
"""

"""
This method returns the lowercase file extension, such as .jpg or .png.
"""
def get_file_extension(file_path):
    dot_index = file_path.rfind(".")
    if dot_index == -1:
        extension = ""
    else:
        extension = file_path[dot_index:]
    return extension.lower()


"""
This method returns image width and height from an OpenCV image
"""
def get_image_size(image):
    height = image.shape[0]
    width = image.shape[1]
    return width, height