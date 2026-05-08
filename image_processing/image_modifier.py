import random
import cv2
from image_processing.alterations import Color_Change
from image_processing.alterations import Blur_Change
from image_processing.alterations import Change_Brightness
from image_processing.alterations import Change_GreyScale
from core.difference import Difference

class ImageModifiier:
    def __init__(self):
        #Stores variables needed like count of difference, tyoe and storing.
        self.count_diff = 5
        self.diff = []
        self.diff_types = ["blur", "colour_shift", "brightness", "grey_shift"]
        self.color_change = Color_Change()
        self.blur_change = Blur_Change()
        self.change_brightness = Change_Brightness()
        self.change_greyscale = Change_GreyScale()
    #Creates a duplicate of the image and calls the methods to create the altered image copy
    def copy_img(self, img):
        altered_img = img.copy()
        self.create_alterations(altered_img)
        final_altered_img = self.apply_alterations(altered_img)
        return final_altered_img

    def create_alterations(self, img):
        img_heignt, img_width = self.img_dimensions(img)
        self.diff = []
        #Loop to create different sizes of areas within the image to be altered and loops until 5 different areas are created without any overlapping between them
        while len(self.diff) < self.count_diff:
            #Randomly appoints an area, orgin coordinates within the image and type of change that is applied to the area
            area_width = random.randint(img_width // 25, img_width // 5)
            area_height = random.randint(img_heignt // 25, img_heignt // 5)
            area_x = random.randint(0, (img_width - area_width))
            area_y = random.randint(0, (img_heignt - area_height))
            area_type_no = random.randint(0, 3)
            area_type = self.diff_types[area_type_no]
            new_area = Difference(
                x = area_x,
                y = area_y,
                width = area_width,
                height = area_height,
                alteration_name = area_type,
                found = False
            )
            #Checks for overlap and if no overlap then added to list
            check_overlap = self.check_area_overlap(new_area)
            if check_overlap == False:
                self.diff.append(new_area)

        return self.diff
    #Checks if there's any overlap with the existing areas with the new area
    def check_area_overlap(self, new_area):
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
                
    #Applies the image alterations to the specfied areas of the image according to the type of change
    def apply_alterations(self, img):
        for area in self.diff:
            if area.alteration_name == "blur":
                img = self.blur_change.apply(img, area)
            elif area.alteration_name == "colour_shift":
                img = self.color_change.apply(img, area)
            elif area.alteration_name == "brightness":
                img = self.change_brightness.apply(img, area)
            elif area.alteration_name == "grey_shift":
                img = self.change_greyscale.apply(img, area)
        return img

    def get_alterations(self):
        return self.diff
    
    #Gives the height and width of the image
    def img_dimensions(self, img):
        height = img.shape[0]
        width = img.shape[1]
        return height, width
    
    #Converts images from bgr to rgb for display
    def convert_to_rgb(self, img):
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return rgb_img