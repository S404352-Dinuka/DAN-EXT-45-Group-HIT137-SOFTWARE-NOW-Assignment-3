"""
This builds the visual interface.
"""

import tkinter as tk

from utils.constants import (
    APP_BACKGROUND_COLOUR,
    APP_FONT_BOLD,
    APP_FONT_BUTTON,
    APP_FONT_CARD_TITLE,
    APP_FONT_NORMAL,
    APP_FONT_STATUS,
    APP_FONT_SUBTITLE,
    APP_FONT_TITLE,
    BORDER_COLOUR,
    BUTTON_PADDING_X,
    BUTTON_PADDING_Y,
    CARD_BACKGROUND_COLOUR,
    IMAGE_AREA_MIN_HEIGHT,
    IMAGE_AREA_MIN_WIDTH,
    IMAGE_PLACEHOLDER_BACKGROUND,
    MUTED_TEXT_COLOUR,
    PLACEHOLDER_PADDING_X,
    PLACEHOLDER_PADDING_Y,
    PLACEHOLDER_WRAP_LENGTH,
    SECONDARY_COLOUR,
    SECONDARY_HOVER_COLOUR,
    STATUS_ACCENT_COLOUR,
    STATUS_BACKGROUND_COLOUR,
    STATUS_TEXT_COLOUR,
    TEXT_COLOUR,
)

"""
This class builds and stores the main GUI widgets.
"""
class MainLayout:
    def __init__(self, root, load_command, reveal_command, click_command):
        self.root = root
        self.load_command = load_command
        self.reveal_command = reveal_command
        self.click_command = click_command
        self.remaining_text = tk.StringVar()
        self.mistakes_text = tk.StringVar()
        self.score_text = tk.StringVar()
        self.status_text = tk.StringVar()
        self.original_image_area = None
        self.modified_image_area = None
        self.original_label = None
        self.modified_label = None
        self.build_layout()

    """
    This method builds the main GUI widgets.
    """
    def build_layout(self):
        self.root.configure(bg=APP_BACKGROUND_COLOUR)
        main_container = tk.Frame(
            self.root,
            bg=APP_BACKGROUND_COLOUR,
            padx=18,
            pady=16
        )
        main_container.pack(fill=tk.BOTH, expand=True)
        self.create_header(main_container)
        self.create_control_panel(main_container)
        self.create_status_label(main_container)
        self.create_image_section(main_container)

    """
    This method creates the app title section.
    """
    def create_header(self, parent_frame):
        """
        TODO:: Need to implement
        """

    """
    This method creates the button and score card section.
    """
    def create_control_panel(self, parent_frame):
        """
        TODO:: Need to implement
        """

    """
    This method creates a status message area.
    """
    def create_status_label(self, parent_frame):
        """
        TODO:: Need to implement
        """

    """
    This method creates the original and modified image section.
    """
    def create_image_section(self, parent_frame):
        """
        TODO:: Need to implement
        """