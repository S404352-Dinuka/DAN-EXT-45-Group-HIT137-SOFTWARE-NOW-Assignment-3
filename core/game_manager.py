"""
Core game rules and game state
"""

from core.difference_click_detector import DifferenceClickDetector
from utils.constants import CLICK_TOLERANCE, MAX_MISTAKES
from utils.status_messages import GameStatus,StatusMessage

class GameManager:
    """
    This class manages the main game state and game rules

    It stores the current images, hidden differences, scores, mistakes,
    and round lock status. It also validates player clicks and reveals
    remaining differences when required
    """

    def __init__(self):
        """
        This method initializes the game manager with default game values.
        """
        self.detector = DifferenceClickDetector()
        self.original_image = None
        self.modified_image = None
        self.differences = []
        self.image_path = ""
        self.max_mistakes = MAX_MISTAKES
        self.click_tolerance = CLICK_TOLERANCE
        self.round_score = 0
        self.total_score = 0
        self.mistakes = 0
        self.round_locked = True

    def reset_and_load_new_image(self, original_image, modified_image, differences_list, img_path):
        """
        This method starts a new round with a newly loaded image
        It stores the original image, modified image, difference list, and image path.
        It also resets the round score and mistake count, and unlocks the round for the player

        :param original_image: The original image loaded for the game.
        :param modified_image: The modified image that contains hidden differences.
        :param differences_list: The list of difference regions for the current round.
        :param img_path: The file path of the selected image.
        """
        #TODO :: Need to Implement

    def get_remaining_differences_count(self):
        """
        This method returns how many differences have not been found or revealed yet

        :return: The number of unresolved differences remaining in the current round
        """
        remaining_count = 0
        # TODO :: Need to Implement
        return remaining_count


    def validate_click(self, click_cord_x, click_cord_y):
        """
        This method checks a player's click and returns a result status with a message

        It checks whether an image is loaded, whether the round is locked,
        whether the clicked difference was already found, whether the player
        clicked a new unresolved difference, or whether the click is incorrect

        :param click_cord_x: The x coordinate of the player's click.
        :param click_cord_y: The y coordinate of the player's click.
        :return: A GameStatus value and a related user-facing message.
        """
        if self.original_image is None:
            return GameStatus.NO_IMAGE, StatusMessage.PLEASE_LOAD_IMAGE_FIRST.value

        if self.round_locked:
            return GameStatus.ROUND_LOCKED, StatusMessage.ROUND_LOCKED.value

        difference_already_found = self.detector.find_clicked_found_difference(
            self.differences,
            click_cord_x,
            click_cord_y,
            self.click_tolerance
        )

        if difference_already_found is not None:
            return GameStatus.ALREADY_FOUND, StatusMessage.ALREADY_FOUND.value

        unresolved_difference = self.detector.find_clicked_unresolved_difference(
            self.differences,
            click_cord_x,
            click_cord_y,
            self.click_tolerance
        )

        if unresolved_difference is not None:
            unresolved_difference.found = True
            self.round_score = self.round_score + 1
            self.total_score = self.total_score + 1

            if self.get_remaining_differences_count() == 0:
                self.round_locked = True
                return GameStatus.ROUND_COMPLETE, StatusMessage.ALREADY_FOUND.value

            return GameStatus.DIFFERENCE_FOUND, StatusMessage.DIFFERENCE_FOUND.value

        self.mistakes = self.mistakes + 1

        if self.mistakes >= self.max_mistakes:
            self.round_locked = True
            return GameStatus.MAX_MISTAKES, StatusMessage.MAX_MISTAKES.value

        return GameStatus.WRONG_CLICK, StatusMessage.WRONG_CLICK.value

    def reveal_unfound_differences(self):
        """
        This method reveals all remaining differences and locks the current round

        If no image is loaded, it returns a no-image status
        If there are no remaining differences, it locks the round and returns a message
        Otherwise, it marks all unfound differences as revealed and locks the round

        :return: A GameStatus value and a related user facing message.
        """
        if self.original_image is None:
            status = GameStatus.NO_IMAGE, StatusMessage.PLEASE_LOAD_IMAGE_FIRST.value
        elif self.get_remaining_differences_count() == 0:
            self.round_locked = True
            status = GameStatus.NOTHING_TO_REVEAL, StatusMessage.NOTHING_TO_REVEAL.value
        else:
            for diff in self.differences:
                if not diff.found:
                    diff.revealed = True
            self.round_locked = True
            status = GameStatus.DIFFERENCES_REVEALED, StatusMessage.DIFFERENCES_REVEALED.value
        return status