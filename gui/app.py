"""
Main Tkinter app controller.
This class connects GUI, image processing, and game logic.
"""

from tkinter import filedialog, messagebox

from core.game_manager import GameManager
from gui.image_display_helper import ImageDisplayHelper
from gui.layout import MainLayout
from image_processing.image_loader import ImageLoader
from image_processing.image_modifier import ImageModifiier
from utils.constants import (
    APP_TITLE,
    MAX_DISPLAY_HEIGHT,
    MAX_DISPLAY_WIDTH,
    MIN_DISPLAY_HEIGHT,
    MIN_DISPLAY_WIDTH,
    DEFAULT_DISPLAY_SCALE,
    IMAGE_DISPLAY_INNER_PADDING,
    IMAGE_LABEL_BORDER_WIDTH,
    IMAGE_LABEL_HIGHLIGHT_THICKNESS,
    IMAGE_LABEL_PADDING,
    MIN_AVAILABLE_IMAGE_DISPLAY_SIZE,
    MIN_VALID_WIDGET_SIZE,
    SCREEN_HEIGHT_RESERVED_SPACE,
    SCREEN_WIDTH_RESERVED_SPACE,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,

)
from utils.status_messages import (
    DialogTitle,
    ErrorMessageTemplate,
    FileTypeOption,
    GameStatus,
    InfoLabelTemplate,
    StatusMessage,
)


class SpotTheDifferenceApplication:
    """
    This class controls the main Spot the Difference application
    """

    def __init__(self, root):
        """
        This method initializes the main application

        :param root: The main Tkinter root window
        """
        self.root = root
        self.root.title(APP_TITLE)
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.image_loader = ImageLoader()
        self.image_modifier = ImageModifiier()
        self.game_manager = GameManager()
        self.image_display_helper = ImageDisplayHelper()
        self.original_photo = None
        self.modified_photo = None
        self.display_scale = DEFAULT_DISPLAY_SCALE
        self.max_image_width = MAX_DISPLAY_WIDTH
        self.max_image_height = MAX_DISPLAY_HEIGHT
        self.setup_image_display_size()
        self.layout = MainLayout(
            self.root,
            self.load_image,
            self.reveal_differences,
            self.on_modified_image_click
        )
        self.update_info_labels()
        self.update_layout_status_text(StatusMessage.LOAD_IMAGE_TO_START)

    def calculate_maximum_display_width(self):
        """
        This method calculates a suitable maximum width for each image

        :return: Calculated maximum display width
        """
        screen_width_pixels = self.root.winfo_screenwidth()
        available_width_per_image = (screen_width_pixels - SCREEN_WIDTH_RESERVED_SPACE) // 2
        maximum_width = min(
            MAX_DISPLAY_WIDTH,
            max(MIN_DISPLAY_WIDTH, available_width_per_image)
        )
        return maximum_width

    def calculate_maximum_display_height(self):
        """
        This method calculates a suitable maximum height for the displayed images

        :return: The calculated maximum display height
        """
        screen_height_pixels = self.root.winfo_screenheight()
        available_height_for_images = screen_height_pixels - SCREEN_HEIGHT_RESERVED_SPACE

        maximum_height = min(
            MAX_DISPLAY_HEIGHT,
            max(MIN_DISPLAY_HEIGHT, available_height_for_images)
        )

        return maximum_height

    def setup_image_display_size(self):
        """
        This method sets the maximum display width and height for the images
        """
        self.max_image_width = self.calculate_maximum_display_width()
        self.max_image_height = self.calculate_maximum_display_height()

    def load_image(self):
        """
        This method opens the file dialog, loads an image, creates differences and resets the game state for a new round
        """
        img_file_path = filedialog.askopenfilename(
            title=DialogTitle.CHOOSE_IMAGE.value,
            filetypes=[
                FileTypeOption.SUPPORTED_IMAGES.value,
                FileTypeOption.JPEG_IMAGES.value,
                FileTypeOption.PNG_IMAGES.value,
                FileTypeOption.BMP_IMAGES.value,
                FileTypeOption.ALL_FILES.value,
            ]
        )

        if img_file_path == "":
            self.update_layout_status_text(StatusMessage.IMAGE_LOADING_CANCELLED)
            return

        try:
            original_image = self.image_loader.load_img(img_file_path)

            modified_image = self.image_modifier.copy_img(
                original_image
            )

            differences = self.image_modifier.get_alterations()

            self.game_manager.reset_and_load_new_image(
                original_image,
                modified_image,
                differences,
                img_file_path
            )

            self.update_layout_status_text(StatusMessage.NEW_IMAGE_LOADED)

            self.refresh_images()
            self.update_info_labels()

        except Exception as error:
            messagebox.showerror(
                DialogTitle.IMAGE_ERROR.value,
                str(error)
            )
            self.update_layout_status_text(StatusMessage.IMAGE_COULD_NOT_BE_LOADED)

    def get_available_image_display_size(self):
        """
        This method gets the actual available image display size from the GUI

        :return: The available display width and height of the images
        """
        self.root.update_idletasks()

        original_area_width = self.layout.original_image_area.winfo_width()
        original_area_height = self.layout.original_image_area.winfo_height()

        modified_area_width = self.layout.modified_image_area.winfo_width()
        modified_area_height = self.layout.modified_image_area.winfo_height()

        available_width = min(original_area_width, modified_area_width)
        available_height = min(original_area_height, modified_area_height)

        if available_width <= MIN_VALID_WIDGET_SIZE:
            available_width = self.max_image_width

        if available_height <= MIN_VALID_WIDGET_SIZE:
            available_height = self.max_image_height

        available_width = available_width - IMAGE_DISPLAY_INNER_PADDING
        available_height = available_height - IMAGE_DISPLAY_INNER_PADDING

        if available_width < MIN_AVAILABLE_IMAGE_DISPLAY_SIZE:
            available_width = MIN_AVAILABLE_IMAGE_DISPLAY_SIZE

        if available_height < MIN_AVAILABLE_IMAGE_DISPLAY_SIZE:
            available_height = MIN_AVAILABLE_IMAGE_DISPLAY_SIZE

        return available_width, available_height

    def get_original_click_coordinates(self, event):
        """
        This method converts click coordinates on the displayed image to original image coordinates

        :param event: The Tkinter mouse click event
        :return: Original image x and y coordinates, or None values if the click is invalid
        """
        if self.modified_photo is None:
            return None, None

        displayed_image_width = self.modified_photo.width()
        displayed_image_height = self.modified_photo.height()

        if event.x < 0 or event.y < 0:
            return None, None

        if event.x >= displayed_image_width:
            return None, None

        if event.y >= displayed_image_height:
            return None, None

        original_x = int(event.x / self.display_scale)
        original_y = int(event.y / self.display_scale)

        return original_x, original_y

    def on_modified_image_click(self, event):
        """
        This method handles player clicks inside the modified image

        :param event: The Tkinter mouse click event
        """
        if self.game_manager.modified_image is None:
            self.update_layout_status_text(StatusMessage.PLEASE_LOAD_IMAGE_FIRST)
            return

        try:
            original_x, original_y = self.get_original_click_coordinates(event)

            if original_x is None or original_y is None:
                self.update_layout_status_text(StatusMessage.CLICK_INSIDE_MODIFIED_IMAGE)
                return

            image_height = self.game_manager.modified_image.shape[0]
            image_width = self.game_manager.modified_image.shape[1]

            if original_x < 0 or original_y < 0:
                self.update_layout_status_text(StatusMessage.CLICK_INSIDE_MODIFIED_IMAGE)
                return

            if original_x >= image_width or original_y >= image_height:
                self.update_layout_status_text(StatusMessage.CLICK_INSIDE_MODIFIED_IMAGE)
                return

            result, message = self.game_manager.validate_click(original_x, original_y)

            self.update_layout_status_text(message)
            self.refresh_images()
            self.update_info_labels()

            if result == GameStatus.ROUND_COMPLETE:
                messagebox.showinfo(
                    DialogTitle.ROUND_COMPLETE.value,
                    message
                )

            if result == GameStatus.MAX_MISTAKES:
                messagebox.showwarning(
                    DialogTitle.ROUND_LOCKED.value,
                    message
                )

        except Exception as error:
            messagebox.showerror(
                DialogTitle.CLICK_ERROR.value,
                ErrorMessageTemplate.CLICK_ERROR.value.format(error=error)
            )

    def reveal_differences(self):
        """
        This method reveals all differences that the player has not found
        """
        try:
            result, message = self.game_manager.reveal_unfound_differences()

            self.update_layout_status_text(message)
            self.refresh_images()
            self.update_info_labels()

            if result == GameStatus.DIFFERENCES_REVEALED:
                messagebox.showinfo(
                    DialogTitle.REVEAL.value,
                    message
                )

        except Exception as error:
            messagebox.showerror(
                DialogTitle.REVEAL_ERROR.value,
                ErrorMessageTemplate.REVEAL_ERROR.value.format(error=error)
            )

    def refresh_images(self):
        """
        This method refreshes both displayed images after loading, finding, or revealing differences
        """
        if self.game_manager.original_image is None:
            return

        if self.game_manager.modified_image is None:
            return

        original_marked, modified_marked = self.image_display_helper.draw_difference_circles(
            self.game_manager.original_image,
            self.game_manager.modified_image,
            self.game_manager.differences
        )

        display_width, display_height = self.get_available_image_display_size()

        self.original_photo, original_scale = self.image_display_helper.create_display_image(
            original_marked,
            display_width,
            display_height
        )

        self.modified_photo, modified_scale = self.image_display_helper.create_display_image(
            modified_marked,
            display_width,
            display_height
        )

        self.display_scale = modified_scale

        self.layout.original_label.config(
            image=self.original_photo,
            text="",
            width=self.original_photo.width(),
            height=self.original_photo.height(),
            padx=IMAGE_LABEL_PADDING,
            pady=IMAGE_LABEL_PADDING,
            bd=IMAGE_LABEL_BORDER_WIDTH,
            highlightthickness=IMAGE_LABEL_HIGHLIGHT_THICKNESS
        )

        self.layout.modified_label.config(
            image=self.modified_photo,
            text="",
            width=self.modified_photo.width(),
            height=self.modified_photo.height(),
            padx=IMAGE_LABEL_PADDING,
            pady=IMAGE_LABEL_PADDING,
            bd=IMAGE_LABEL_BORDER_WIDTH,
            highlightthickness=IMAGE_LABEL_HIGHLIGHT_THICKNESS
        )

    def update_info_labels(self):
        """
        This method updates score, remaining count, and mistake count on screen
        """
        remaining = self.game_manager.get_remaining_differences_count()
        mistakes = self.game_manager.mistakes
        max_mistakes = self.game_manager.max_mistakes
        round_score = self.game_manager.round_score
        total_score = self.game_manager.total_score

        self.layout.remaining_text.set(
            InfoLabelTemplate.REMAINING.value.format(remaining=remaining)
        )

        self.layout.mistakes_text.set(
            InfoLabelTemplate.MISTAKES.value.format(
                mistakes=mistakes,
                max_mistakes=max_mistakes
            )
        )

        self.layout.score_text.set(
            InfoLabelTemplate.SCORE.value.format(
                round_score=round_score,
                total_score=total_score
            )
        )

    def update_layout_status_text(self, status_message):
        """
        This method updates the status message shown in the GUI

        :param status_message: The status message to show in the GUI
        """
        if isinstance(status_message, StatusMessage):
            self.layout.status_text.set(status_message.value)
        else:
            self.layout.status_text.set(status_message)