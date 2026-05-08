"""
This module contains click detection logic for difference regions.

It checks whether the player's click matches a found or unresolved
difference region.
"""


class DifferenceClickDetector:
    """
    This class checks player clicks against difference regions.
    """

    def find_clicked_found_difference(self, differences_list, click_cord_x, click_cord_y, tolerance):
        """
        This method returns a difference that was already found
        if the player clicks inside that same region again

        :param differences_list: The list of difference regions
        :param click_cord_x: The x coordinate of the player's click
        :param click_cord_y: The y coordinate of the player's click
        :param tolerance: The extra clickable area around each difference region
        :return: The already found difference if matched, otherwise None
        """
        for diff in differences_list:
            player_clicked_found_difference = (
                diff.found
                and diff.is_click_within_region(click_cord_x, click_cord_y, tolerance)
            )
            if player_clicked_found_difference:
                return diff
        return None

    def find_clicked_unresolved_difference(self, differences_list, click_cord_x, click_cord_y, tolerance):
        """
        This method returns an unresolved difference that matches the player's click
        A difference is unresolved when it has not been found or revealed yet

        :param differences_list: The list of difference regions
        :param click_cord_x: The x coordinate of the player's click
        :param click_cord_y: The y coordinate of the player's click
        :param tolerance: The extra clickable area around each difference region
        :return: The clicked unresolved difference if matched, otherwise None
        """
        for diff in differences_list:
            difference_is_unresolved = not diff.is_difference_resolved()
            player_clicked_difference = diff.is_click_within_region(
                click_cord_x,
                click_cord_y,
                tolerance
            )
            if difference_is_unresolved and player_clicked_difference:
                return diff

        return None