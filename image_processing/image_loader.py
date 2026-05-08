import cv2
import os

class ImageLoader:
    #Intailizes the image path used and the format of the image accepted
    def __init__(self):
        self.formats = [".jpg", ".jpeg", ".png", ".bmp"]
        self.img_path = None
    #Loads the image and checks if the image loaded properly
    def load_img(self, filePath):
        self.img_path = filePath
        file_type = os.path.splitext(filePath)[1].lower()
        if file_type in self.formats:
            img = cv2.imread(filePath)
            if img is None:
                return ValueError("Image not loaded")
            return img
