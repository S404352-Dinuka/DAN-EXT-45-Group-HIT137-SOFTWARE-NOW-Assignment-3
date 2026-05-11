"""
This module contains click detection logic for difference regions.
"""


class DifferenceClickDetector:
    """
    This class checks player clicks against difference regions.
    """

    def find_clicked_found_difference(self, differences_list, click_cord_x, click_cord_y, tolerance):
        """
        This method returns a difference that was already found

        :param differences_list:List of difference regions
        :param click_cord_x: x coordinate of the player's click
        :param click_cord_y: y coordinate of the player's click
        :param tolerance: extra clickable area
        :return: found difference if matched, otherwise None
        """
        for diff in differences_list:
            player_clicked_found_difference = (
                diff.found
                and diff.check_if_click_within_region(click_cord_x, click_cord_y, tolerance)
            )
            if player_clicked_found_difference:
                return diff
        return None

    def find_clicked_unresolved_difference(self, differences_list, click_cord_x, click_cord_y, tolerance):
        """
        This method returns an unresolved difference that matches the player's click

        :param differences_list: List of difference regions
        :param click_cord_x:x coordinate of the player's click
        :param click_cord_y:y coordinate of the player's click
        :param tolerance:extra clickable area around each difference region
        :return: unresolved difference if matched, otherwise None
        """
        for diff in differences_list:
            difference_is_unresolved = not diff.check_if_difference_resolved()
            player_clicked_difference = diff.check_if_click_within_region(
                click_cord_x,
                click_cord_y,
                tolerance
            )
            if difference_is_unresolved and player_clicked_difference:
                return diff

        return None