"""
This module contains the image modification logic for the game
"""

import random
import cv2
from image_processing.image_effect import ColourEffect
from image_processing.image_effect import BlurEffect
from image_processing.image_effect import BrightnessEffect
from image_processing.image_effect import GreyscaleEffect
from image_processing.image_effect import PixelateEffect
from image_processing.image_effect import ContrastEffect
from core.difference import Difference
from utils.status_messages import ImageEffectType
from utils.helpers import calculate_difference_circle_radius
from utils.constants import (
    NUMBER_OF_DIFFERENCES,
    BLUR_EDGE_THRESHOLD_HIGH,
    BLUR_EDGE_THRESHOLD_LOW,
    MIN_BLUR_EDGE_DENSITY,
    DIFFERENCE_CIRCLE_MIN_GAP,
    CANDIDATE_GRID_COLUMNS,
    CANDIDATE_GRID_ROWS,
    CANDIDATE_AREA_MIN_SCALE,
    CANDIDATE_AREA_MAX_SCALE,
    MIN_REGION_DETAIL_SCORE,
    PLAIN_AREA_BRIGHTNESS_THRESHOLD,
    PLAIN_AREA_VISIBILITY_CHANGE,
    PLAIN_AREA_VISIBILITY_BLEND_WEIGHT,
)

class ModifiedImageBuilder:
    """
    This class creates the modified version of the selected image
    """

    def __init__(self):
        """
        This method initializes the image modifier with default alteration values
        """
        self.count_diff = NUMBER_OF_DIFFERENCES
        self.diff = []
        self.diff_types = [
            ImageEffectType.BLUR.value,
            ImageEffectType.COLOUR_SHIFT.value,
            ImageEffectType.BRIGHTNESS.value,
            ImageEffectType.GREY_SHIFT.value,
            ImageEffectType.PIXELATE.value,
            ImageEffectType.CONTRAST.value
        ]
        self.color_effect = ColourEffect()
        self.blur_effect = BlurEffect()
        self.brightness_effect = BrightnessEffect()
        self.greyscale_effect = GreyscaleEffect()
        self.pixelate_effect = PixelateEffect()
        self.contrast_effect = ContrastEffect()

    def copy_img(self, img):
        """
        This method creates a copy of the original image and applies alterations to it

        :param img: original image
        :return: altered copy of the original image
        """
        altered_img = img.copy()
        self.create_alterations(altered_img)
        final_altered_img = self.apply_alterations(altered_img)
        return final_altered_img

    def create_alterations(self, img):
        """
        Creates difference areas

        :param img:OpenCV image used to calculate valid difference areas
        :return:List of generated difference areas
        """
        img_height, img_width = self.img_dimensions(img)
        self.diff = []

        candidate_areas = self.create_candidate_areas(img_width, img_height)
        random.shuffle(candidate_areas)

        all_effect_types = [
            ImageEffectType.BLUR.value,
            ImageEffectType.COLOUR_SHIFT.value,
            ImageEffectType.BRIGHTNESS.value,
            ImageEffectType.GREY_SHIFT.value,
            ImageEffectType.PIXELATE.value,
            ImageEffectType.CONTRAST.value
        ]

        used_effect_types = set()

        blur_area = self.get_best_blur_area(img, candidate_areas)

        if blur_area is not None:
            blur_area.alteration_name = ImageEffectType.BLUR.value
            self.diff.append(blur_area)
            used_effect_types.add(ImageEffectType.BLUR.value)

            candidate_areas = [
                area for area in candidate_areas if area is not blur_area
            ]

            candidate_areas = self.remove_overlapping_candidate_areas(candidate_areas)

        pixelate_area = self.get_suitable_area_for_effect(
            img,
            candidate_areas,
            ImageEffectType.PIXELATE.value
        )

        if pixelate_area is None:
            pixelate_area = self.get_any_non_overlapping_area(candidate_areas)

        if pixelate_area is not None and len(self.diff) < self.count_diff:
            pixelate_area.alteration_name = ImageEffectType.PIXELATE.value
            self.diff.append(pixelate_area)
            used_effect_types.add(ImageEffectType.PIXELATE.value)

            candidate_areas = [
                area for area in candidate_areas if area is not pixelate_area
            ]
            candidate_areas = self.remove_overlapping_candidate_areas(candidate_areas)

        remaining_effect_types = [
            effect_type
            for effect_type in all_effect_types
            if effect_type not in used_effect_types
        ]

        random.shuffle(remaining_effect_types)

        for effect_type in remaining_effect_types:
            if len(self.diff) >= self.count_diff:
                break

            selected_area = self.get_suitable_area_for_effect(
                img,
                candidate_areas,
                effect_type
            )

            if selected_area is None:
                selected_area = self.get_any_non_overlapping_area(candidate_areas)

            if selected_area is None:
                continue

            selected_area.alteration_name = effect_type
            self.diff.append(selected_area)
            used_effect_types.add(effect_type)

            candidate_areas = [
                area for area in candidate_areas if area is not selected_area
            ]
            candidate_areas = self.remove_overlapping_candidate_areas(candidate_areas)

        while len(self.diff) < self.count_diff:
            selected_area = self.get_any_non_overlapping_area(candidate_areas)

            if selected_area is None:
                break

            available_effect_types = [
                effect_type
                for effect_type in all_effect_types
                if effect_type not in used_effect_types
            ]

            if len(available_effect_types) == 0:
                available_effect_types = all_effect_types

            selected_effect_type = random.choice(available_effect_types)

            selected_area.alteration_name = selected_effect_type
            self.diff.append(selected_area)
            used_effect_types.add(selected_effect_type)

            candidate_areas = [
                area for area in candidate_areas if area is not selected_area
            ]

            candidate_areas = self.remove_overlapping_candidate_areas(candidate_areas)

        return self.diff
    def apply_alterations(self, img):
        """
        This method applies the selected alteration type to each difference area

        :param img: image that will be altered
        :return: image after all alterations have been applied
        """
        for area in self.diff:
            is_plain_area = not self.has_enough_visual_detail(img, area)

            if area.alteration_name == ImageEffectType.BLUR.value:
                img = self.blur_effect.apply(img, area)

            elif area.alteration_name == ImageEffectType.COLOUR_SHIFT.value:
                img = self.color_effect.apply(img, area)

            elif area.alteration_name == ImageEffectType.BRIGHTNESS.value:
                img = self.brightness_effect.apply(img, area)

            elif area.alteration_name == ImageEffectType.GREY_SHIFT.value:
                img = self.greyscale_effect.apply(img, area)

            elif area.alteration_name == ImageEffectType.PIXELATE.value:
                img = self.pixelate_effect.apply(img, area)

            elif area.alteration_name == ImageEffectType.CONTRAST.value:
                img = self.contrast_effect.apply(img, area)

            if is_plain_area:
                img = self.improve_plain_area_visibility(img, area)
        return img

    def get_alterations(self):
        """
        This method returns the list of generated difference areas

        :return: list of difference areas created for the current image
        """
        return self.diff

    def img_dimensions(self, img):
        """
        This method returns the height and width of the image

        :param img: OpenCV image
        :return: image height and width
        """
        height = img.shape[0]
        width = img.shape[1]
        return height, width

    def get_edge_density(self, img, area):
        """
        Calculates the edge density of the selected image area

        :param img: Image that will be checked
        :param area: Selected difference area
        :return: Edge density value of the selected area
        """
        selected_area = img[
            area.y:area.y + area.height,
            area.x:area.x + area.width
        ]

        grey_area = cv2.cvtColor(selected_area, cv2.COLOR_BGR2GRAY)

        edge_image = cv2.Canny(
            grey_area,
            BLUR_EDGE_THRESHOLD_LOW,
            BLUR_EDGE_THRESHOLD_HIGH
        )

        edge_density = cv2.countNonZero(edge_image) / edge_image.size

        return edge_density

    def create_candidate_areas(self, img_width, img_height):
        """
        Creates fixed candidate areas using a grid

        :param img_width: Width of the image
        :param img_height: Height of the image
        :return: List of candidate Difference areas
        """
        candidate_areas = []

        cell_width = img_width // CANDIDATE_GRID_COLUMNS
        cell_height = img_height // CANDIDATE_GRID_ROWS

        for row in range(CANDIDATE_GRID_ROWS):
            for column in range(CANDIDATE_GRID_COLUMNS):
                area_width_scale = random.uniform(
                    CANDIDATE_AREA_MIN_SCALE,
                    CANDIDATE_AREA_MAX_SCALE
                )

                area_height_scale = random.uniform(
                    CANDIDATE_AREA_MIN_SCALE,
                    CANDIDATE_AREA_MAX_SCALE
                )

                area_width = int(cell_width * area_width_scale)
                area_height = int(cell_height * area_height_scale)

                area_x = column * cell_width + (cell_width - area_width) // 2
                area_y = row * cell_height + (cell_height - area_height) // 2

                candidate_area = Difference(
                    x=area_x,
                    y=area_y,
                    width=area_width,
                    height=area_height,
                    alteration_name="",
                    found=False
                )

                candidate_areas.append(candidate_area)

        return candidate_areas

    def get_best_blur_area(self, img, candidate_areas):
        """
        Selects the candidate area with the highest edge density for blur.

        :param img: Image that will be checked.
        :param candidate_areas: List of candidate areas.
        :return: Best blur area if edge density is high enough, otherwise None.
        """
        best_area = None
        highest_edge_density = 0

        for area in candidate_areas:
            edge_density = self.get_edge_density(img, area)

            if edge_density > highest_edge_density:
                highest_edge_density = edge_density
                best_area = area

        if highest_edge_density >= MIN_BLUR_EDGE_DENSITY:
            return best_area

        return None

    def check_area_overlap(self, new_area):
        """
        Checks whether a new difference area overlaps with an existing area

        :param new_area: Newly created difference area
        :return: True if the new area overlaps otherwise False
        """
        new_left = new_area.x
        new_right = new_area.x + new_area.width
        new_top = new_area.y
        new_bottom = new_area.y + new_area.height

        new_center_x, new_center_y = new_area.get_region_center_point()
        new_circle_radius = calculate_difference_circle_radius(new_area)
        for area in self.diff:
            area_left = area.x
            area_right = area.x + area.width
            area_top = area.y
            area_bottom = area.y + area.height

            rectangles_overlap = not (
                new_top > area_bottom
                or new_bottom < area_top
                or new_left > area_right
                or new_right < area_left
            )

            if rectangles_overlap:
                return True

            area_center_x, area_center_y = area.get_region_center_point()
            area_circle_radius = calculate_difference_circle_radius(area)

            distance_x = new_center_x - area_center_x
            distance_y = new_center_y - area_center_y

            distance_between_centres_squared = (
                distance_x * distance_x
                + distance_y * distance_y
            )

            minimum_allowed_distance = (
                new_circle_radius
                + area_circle_radius
                + DIFFERENCE_CIRCLE_MIN_GAP
            )

            if distance_between_centres_squared < minimum_allowed_distance * minimum_allowed_distance:
                return True

        return False

    def remove_overlapping_candidate_areas(self, candidate_areas):
        """
        Removes candidate areas that overlap with already selected difference areas

        :param candidate_areas: Candidate difference areas
        :return: Candidate areas that do not overlap with existing selected areas
        """
        non_overlapping_areas = []

        for candidate_area in candidate_areas:
            if not self.check_area_overlap(candidate_area):
                non_overlapping_areas.append(candidate_area)

        return non_overlapping_areas

    def has_enough_colour_for_greyscale(self, img, area):
        """
        Checks whether the selected area has enough color so the greyscale effect will be visible

        :param img: OpenCV image used to check the selected area
        :param area: Difference area containing x, y, width, and height values
        :return: True if the selected area has enough color otherwise False
        """
        selected_area = img[
            area.y:area.y + area.height,
            area.x:area.x + area.width
        ]

        if selected_area.size == 0:
            return False

        hsv_area = cv2.cvtColor(selected_area, cv2.COLOR_BGR2HSV)
        average_saturation = hsv_area[:, :, 1].mean()

        return average_saturation >= 25

    def get_suitable_area_for_effect(self, img, candidate_areas, effect_type):
        """
        Returns a suitable candidate area for the given image effect

        :param img: Image used to check the selected area
        :param candidate_areas: List of available candidate areas
        :param effect_type: Image effect type to be applied
        :return: Suitable candidate area if found otherwise None
        """
        shuffled_candidates = candidate_areas.copy()
        random.shuffle(shuffled_candidates)

        for candidate_area in shuffled_candidates:
            if self.check_area_overlap(candidate_area):
                continue

            if not self.has_enough_visual_detail(img, candidate_area):
                continue

            if effect_type == ImageEffectType.GREY_SHIFT.value:
                if not self.has_enough_colour_for_greyscale(img, candidate_area):
                    continue

            return candidate_area

        return None

    def has_enough_visual_detail(self, img, area):
        """
        Checks whether the selected image area has enough texture or color variation.

        :param img:OpenCV image used to check the selected area
        :param area:Difference area containing x, y, width, and height values
        :return:True if the selected area has enough visual detail otherwise False
        """
        selected_area = img[
            area.y:area.y + area.height,
            area.x:area.x + area.width
        ]

        if selected_area.size == 0:
            return False

        grey_area = cv2.cvtColor(selected_area, cv2.COLOR_BGR2GRAY)
        detail_score = grey_area.std()

        return detail_score >= MIN_REGION_DETAIL_SCORE

    def get_any_non_overlapping_area(self, candidate_areas):
        """
        Returns any candidate area that does not overlap with already selected areas

        :param candidate_areas: List of candidate difference areas
        :return: A non-overlapping candidate area if available, otherwise None
        """
        shuffled_candidate_areas = candidate_areas.copy()
        random.shuffle(shuffled_candidate_areas)

        for candidate_area in shuffled_candidate_areas:
            if not self.check_area_overlap(candidate_area):
                return candidate_area

        return None

    def improve_plain_area_visibility(self, img, area):
        """
        Applies a small visibility adjustment to plain image areas.

        :param img: Image that will be modified
        :param area: Difference area with x, y, width, and height values
        :return: Modified image
        """
        x = area.x
        y = area.y
        w = area.width
        h = area.height

        original_area = img[y:y + h, x:x + w].copy()

        if original_area.size == 0:
            return img

        grey_area = cv2.cvtColor(original_area, cv2.COLOR_BGR2GRAY)
        average_brightness = grey_area.mean()

        if average_brightness > PLAIN_AREA_BRIGHTNESS_THRESHOLD:
            adjusted_area = cv2.subtract(original_area, PLAIN_AREA_VISIBILITY_CHANGE)
        else:
            adjusted_area = cv2.add(original_area,PLAIN_AREA_VISIBILITY_CHANGE)

        blended_area = cv2.addWeighted(
            original_area,
            1 - PLAIN_AREA_VISIBILITY_BLEND_WEIGHT,
            adjusted_area,
            PLAIN_AREA_VISIBILITY_BLEND_WEIGHT,
            0
        )

        img[y:y + h, x:x + w] = blended_area

        return img