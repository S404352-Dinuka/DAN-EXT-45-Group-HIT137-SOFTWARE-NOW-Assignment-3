import cv2

class Alterations:
    def __init__(self):
        pass

    def apply(self, img, area):
        pass


    #Used open cv to select the area in the image to change the color channel to blue and applied it
class Color_Change(Alterations):
    def apply(self, img, area):
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        new_area = img[y:y + h, x:x + w]
        new_area[:, :, 0] = cv2.add(new_area[:,:,0], 50)
        img[y:y+h, x:x+w] = new_area
        return img
    #Applied blur using opencv by selecting the area and set the kernal size to apply blur
class Blur_Change(Alterations):
    def apply(self, img, area):
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        new_area = img[y:y + h, x:x + w]
        blur_area = cv2.GaussianBlur(new_area, (17, 17), 0)
        img[y:y+h, x:x+w] = blur_area
        return img
    #Changes the selected areas brightness using opencv by keeping the constrast alpha same and changing beta to increase the brightness
class Change_Brightness(Alterations):
    def apply(self, img, area):
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        new_area = img[y:y + h, x:x + w]
        bright_area = cv2.convertScaleAbs(new_area, alpha=1.0, beta=20)
        img[y:y+h, x:x+w] = bright_area
        return img
    
class Change_GreyScale(Alterations):
    def apply(self, img, area):
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        new_area = img[y:y + h, x:x + w]
        grey_area = cv2.cvtColor(new_area, cv2.COLOR_BGR2GRAY)
        grey_area_bgr = cv2.cvtColor(grey_area, cv2.COLOR_GRAY2BGR)
        img[y:y+h, x:x+w] = grey_area_bgr
        return img    
    