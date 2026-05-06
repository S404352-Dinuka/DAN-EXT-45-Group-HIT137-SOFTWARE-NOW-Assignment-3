"""
This module contains the Tkinter layout for the Spot the Difference game.
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

class MainLayout:
    """
    This class creates and manages the main Tkinter user interface.

    It builds the header, control panel, status label, and image display
    sections used by the Spot the Difference game.
    """

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

    def build_layout(self):
        """
        This method builds the main GUI widgets.
        """
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

    def create_header(self, parent_frame):
        """
        This method creates the application header section.
        It adds the game title and subtitle to the given parent frame.

        :param parent_frame: The frame where the header section will be placed.
        """
        header_frame = tk.Frame(
            parent_frame,
            bg=APP_BACKGROUND_COLOUR
        )
        header_frame.pack(fill=tk.X, pady=(0, 14))
        title_label = tk.Label(
            header_frame,
            text="Spot the Difference",
            font=APP_FONT_TITLE,
            fg=TEXT_COLOUR,
            bg=APP_BACKGROUND_COLOUR
        )
        title_label.pack(anchor="w")
        subtitle_label = tk.Label(
            header_frame,
            text="Find all 5 hidden changes in the modified image.",
            font=APP_FONT_SUBTITLE,
            fg=MUTED_TEXT_COLOUR,
            bg=APP_BACKGROUND_COLOUR
        )
        subtitle_label.pack(anchor="w", pady=(3, 0))

    def create_control_panel(self, parent_frame):
        """
        This method creates the main control panel.
        It adds the image action buttons and the game statistic cards.

        :param parent_frame: The frame where the control panel will be placed.
        """
        panel_frame = tk.Frame(
            parent_frame,
            bg=CARD_BACKGROUND_COLOUR,
            padx=14,
            pady=12,
            highlightbackground=BORDER_COLOUR,
            highlightthickness=1
        )
        panel_frame.pack(fill=tk.X, pady=(0, 12))
        button_frame = tk.Frame(
            panel_frame,
            bg=CARD_BACKGROUND_COLOUR
        )
        button_frame.pack(side=tk.LEFT)
        load_button = self.create_button(
            button_frame,
            "Load Image",
            self.load_command,
            SECONDARY_COLOUR,
            SECONDARY_HOVER_COLOUR
        )
        load_button.pack(side=tk.LEFT, padx=(0, 8))
        reveal_button = self.create_button(
            button_frame,
            "Reveal Differences",
            self.reveal_command,
            SECONDARY_COLOUR,
            SECONDARY_HOVER_COLOUR
        )
        reveal_button.pack(side=tk.LEFT)
        stats_frame = tk.Frame(
            panel_frame,
            bg=CARD_BACKGROUND_COLOUR
        )
        stats_frame.pack(side=tk.RIGHT)
        self.create_stat_card(stats_frame, "Remaining", self.remaining_text)
        self.create_stat_card(stats_frame, "Mistakes", self.mistakes_text)
        self.create_stat_card(stats_frame, "Score", self.score_text)

    def create_button(self, parent_frame, text, command, normal_colour, hover_colour):
        """
        This method creates a styled button with a hover effect.

        :param parent_frame: The frame where the button will be placed.
        :param text: The text displayed on the button.
        :param command: The function that runs when the button is clicked.
        :param normal_colour: The default background colour of the button.
        :param hover_colour: The background colour used when the mouse is over the button.
        :return: A configured Tkinter Button widget.
        """
        button = tk.Button(
            parent_frame,
            text=text,
            command=command,
            font=APP_FONT_BUTTON,
            fg=hover_colour,
            bg=normal_colour,
            activeforeground=normal_colour,
            activebackground=hover_colour,
            relief=tk.FLAT,
            bd=0,
            padx=BUTTON_PADDING_X,
            pady=BUTTON_PADDING_Y,
            cursor="hand2",
            highlightthickness=0
        )
        button.bind(
            "<Enter>",
            lambda event: button.configure(bg=hover_colour)
        )
        button.bind(
            "<Leave>",
            lambda event: button.configure(bg=normal_colour)
        )
        return button

    def create_stat_card(self, parent_frame, title, text_variable):
        """
        This method creates a small statistic card.
        It displays a statistic title and its related value.

        :param parent_frame: The frame where the statistic card will be placed.
        :param title: The title shown at the top of the card.
        :param text_variable: The Tkinter StringVar used to display the statistic value.
        """
        card_frame = tk.Frame(
            parent_frame,
            bg="#F9FAFB",
            padx=12,
            pady=6,
            highlightbackground=BORDER_COLOUR,
            highlightthickness=1
        )
        card_frame.pack(side=tk.LEFT, padx=(8, 0))
        title_label = tk.Label(
            card_frame,
            text=title,
            font=APP_FONT_NORMAL,
            fg=MUTED_TEXT_COLOUR,
            bg="#F9FAFB"
        )
        title_label.pack(anchor="w")
        value_label = tk.Label(
            card_frame,
            textvariable=text_variable,
            font=APP_FONT_BOLD,
            fg=TEXT_COLOUR,
            bg="#F9FAFB"
        )
        value_label.pack(anchor="w")

    def create_status_label(self, parent_frame):
        """
        This method creates the status message area.
        It displays game messages inside a highlighted status bar.

        :param parent_frame: The frame where the status message area will be placed.
        """
        status_frame = tk.Frame(
            parent_frame,
            bg=STATUS_BACKGROUND_COLOUR,
            highlightbackground=STATUS_BACKGROUND_COLOUR,
            highlightthickness=1
        )
        status_frame.pack(fill=tk.X, pady=(0, 12))
        accent_bar = tk.Frame(
            status_frame,
            bg=STATUS_ACCENT_COLOUR,
            width=5
        )
        accent_bar.pack(side=tk.LEFT, fill=tk.Y)
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_text,
            font=APP_FONT_STATUS,
            fg=STATUS_TEXT_COLOUR,
            bg=STATUS_BACKGROUND_COLOUR,
            padx=12,
            pady=9,
            wraplength=900,
            justify=tk.LEFT,
            anchor="w"
        )
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def create_image_section(self, parent_frame):
        """
        This method creates the image display section.
        It adds separate cards for the original image and the modified image.

        :param parent_frame: The frame where the image section will be placed.
        """
        images_frame = tk.Frame(
            parent_frame,
            bg=APP_BACKGROUND_COLOUR
        )
        images_frame.pack(fill=tk.BOTH, expand=True)
        self.original_image_area, self.original_label = self.create_image_card(
            images_frame,
            "Original Image",
            "Original image will appear here"
        )
        self.modified_image_area, self.modified_label = self.create_image_card(
            images_frame,
            "Modified Image",
            "Click the image to find differences"
        )
        self.modified_label.config(cursor="hand2")
        self.modified_label.bind("<Button-1>", self.click_command)

    def create_image_card(self, parent_frame, title, placeholder_text):
        """
        This method creates an image display card with a title and placeholder label.

        :param parent_frame: The frame where the image card will be placed.
        :param title: The title shown at the top of the image card.
        :param placeholder_text: The text displayed before an image is loaded.
        :return: The image area frame and the image label inside it.
        """
        card_frame = tk.Frame(
            parent_frame,
            bg=CARD_BACKGROUND_COLOUR,
            padx=12,
            pady=12,
            highlightbackground=BORDER_COLOUR,
            highlightthickness=1
        )
        card_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
        title_label = tk.Label(
            card_frame,
            text=title,
            font=APP_FONT_CARD_TITLE,
            fg=TEXT_COLOUR,
            bg=CARD_BACKGROUND_COLOUR
        )
        title_label.pack(anchor="w", pady=(0, 8))
        image_area = tk.Frame(
            card_frame,
            bg=IMAGE_PLACEHOLDER_BACKGROUND,
            width=IMAGE_AREA_MIN_WIDTH,
            height=IMAGE_AREA_MIN_HEIGHT
        )
        image_area.pack(fill=tk.BOTH, expand=True)
        image_area.pack_propagate(False)
        image_label = tk.Label(
            image_area,
            text=placeholder_text,
            font=APP_FONT_NORMAL,
            fg=MUTED_TEXT_COLOUR,
            bg=IMAGE_PLACEHOLDER_BACKGROUND,
            bd=0,
            padx=PLACEHOLDER_PADDING_X,
            pady=PLACEHOLDER_PADDING_Y,
            highlightthickness=0,
            anchor="center",
            justify=tk.CENTER,
            wraplength=PLACEHOLDER_WRAP_LENGTH
        )
        image_label.pack(expand=True)
        return image_area, image_label