"""
Data models for the game which stores data and simple related behavior.
"""

from dataclasses import dataclass


@dataclass
class Difference:
    """
    This class represents one hidden difference region in the image
    """

    x: int
    y: int
    width: int
    height: int
    alteration_name: str
    found: bool = False
    revealed: bool = False

    def get_region_center_point(self):
        """
        This method returns the center point of this difference region

        :return:x and y coordinates of the center point
        """
        center_point_x = self.x + self.width // 2
        center_point_y = self.y + self.height // 2
        return center_point_x, center_point_y

    def is_click_within_region(self, click_cord_x, click_cord_y, tolerance):
        """
        This method checks whether the player's click is inside this difference region

        :param click_cord_x:x coordinate of the player's click
        :param click_cord_y:y coordinate of the player's click
        :param tolerance:extra clickable area around the difference region
        :return: True if the click is inside the region otherwise False
        """
        left_edge = self.x - tolerance
        right_edge = self.x + self.width + tolerance
        top_edge = self.y - tolerance
        bottom_edge = self.y + self.height + tolerance

        click_within_horizontal_range = left_edge <= click_cord_x <= right_edge
        click_within_vertical_range = top_edge <= click_cord_y <= bottom_edge

        return click_within_horizontal_range and click_within_vertical_range

    def is_difference_resolved(self):
        """
        This method checks whether this difference no longer needs to be guessed

        :return: True if the difference is found or revealed, otherwise False
        """
        return self.found or self.revealed