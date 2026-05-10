"""
This module stores status messages shown in the application
"""

from enum import Enum

class GameStatus(Enum):
    """
    This enum stores the possible result statuses for game actions
    """

    NO_IMAGE = "no_image"
    ROUND_LOCKED = "locked"
    ALREADY_FOUND = "already_found"
    DIFFERENCE_FOUND = "found"
    ROUND_COMPLETE = "complete"
    WRONG_CLICK = "wrong"
    MAX_MISTAKES = "max_mistakes"
    NOTHING_TO_REVEAL = "nothing_to_reveal"
    DIFFERENCES_REVEALED = "revealed"

class StatusMessage(Enum):
    """
    This enum stores the user-facing status messages shown in the GUI
    """

    ROUND_LOCKED = "This round is finished. Load a new image to continue."
    ALREADY_FOUND = "You already found that difference."
    DIFFERENCE_FOUND = "Correct. Difference found."
    ROUND_COMPLETE = "Well done. You found all 5 differences."
    WRONG_CLICK = "Wrong click. Try again."
    MAX_MISTAKES = "You made 3 mistakes. No more guesses are allowed for this image."
    NOTHING_TO_REVEAL = "There are no remaining differences to reveal."
    DIFFERENCES_REVEALED = "All unfound differences have been revealed in blue."
    LOAD_IMAGE_TO_START = "Load an image to start."
    IMAGE_LOADING_CANCELLED = "Image loading cancelled."
    IMAGE_COULD_NOT_BE_LOADED = "Image could not be loaded."
    NEW_IMAGE_LOADED = "New image loaded. Click the modified image to find the 5 differences."
    PLEASE_LOAD_IMAGE_FIRST = "Please load an image first."
    CLICK_INSIDE_MODIFIED_IMAGE = "Click inside the modified image."

class DialogTitle(Enum):
    """
    This enum stores titles used in file dialogs and message boxes
    """

    CHOOSE_IMAGE = "Choose an image"
    IMAGE_ERROR = "Image Error"
    CLICK_ERROR = "Click Error"
    REVEAL_ERROR = "Reveal Error"
    ROUND_COMPLETE = "Round Complete"
    ROUND_LOCKED = "Round Locked"
    REVEAL = "Reveal"

class ImageFileExtension(Enum):
    """
    This enum stores supported image file extensions
    """

    JPG = ".jpg"
    JPEG = ".jpeg"
    PNG = ".png"
    BMP = ".bmp"

class FileTypeOption(Enum):
    """
    This enum stores file type options used in the image file dialog
    """

    SUPPORTED_IMAGES = ("Supported image files", "*.jpg *.jpeg *.png *.bmp")
    JPEG_IMAGES = ("JPEG files", "*.jpg *.jpeg")
    PNG_IMAGES = ("PNG files", "*.png")
    BMP_IMAGES = ("BMP files", "*.bmp")
    ALL_FILES = ("All files", "*.*")


class InfoLabelTemplate(Enum):
    """
    This enum stores text templates used for game information labels
    """

    REMAINING = "Remaining: {remaining}"
    MISTAKES = "Mistakes: {mistakes}/{max_mistakes}"
    SCORE = "Round score: {round_score} | Total score: {total_score}"


class ErrorMessageTemplate(Enum):
    """
    This enum stores error message templates that include dynamic values
    """

    CLICK_ERROR = "Something went wrong while checking the click: {error}"
    REVEAL_ERROR = "Could not reveal differences: {error}"


class LayoutText(Enum):
    """
    This enum stores text values used in the Tkinter layout
    """

    APP_HEADER_TITLE = "Spot the Difference"
    APP_HEADER_SUBTITLE = "Find all 5 hidden changes in the modified image."

    LOAD_IMAGE_BUTTON = "Load Image"
    REVEAL_DIFFERENCES_BUTTON = "Reveal Differences"

    REMAINING_STAT_TITLE = "Remaining"
    MISTAKES_STAT_TITLE = "Mistakes"
    SCORE_STAT_TITLE = "Score"

    ORIGINAL_IMAGE_TITLE = "Original Image"
    MODIFIED_IMAGE_TITLE = "Modified Image"

    ORIGINAL_IMAGE_PLACEHOLDER = "Original image will appear here"
    MODIFIED_IMAGE_PLACEHOLDER = "Click the image to find differences"

class AlterationType(Enum):
    """
    This enum stores the image alteration type names used by the image modifier
    """

    BLUR = "blur"
    COLOUR_SHIFT = "colour_shift"
    BRIGHTNESS = "brightness"
    GREY_SHIFT = "grey_shift"

class TkinterEvent(Enum):
    """
    This enum stores Tkinter event binding strings
    """

    MOUSE_ENTER = "<Enter>"
    MOUSE_LEAVE = "<Leave>"
    LEFT_MOUSE_CLICK = "<Button-1>"


class TkinterOption(Enum):
    """
    This enum stores Tkinter option string values
    """

    WEST_ANCHOR = "w"
    CENTER_ANCHOR = "center"
    HAND_CURSOR = "hand2"