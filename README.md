# HIT137 Assignment 3 – README

## Group Members

- Dinuka Dhaneshani Mathangaweera – S404352
- Sehan Hansaja Udayakantha Panik Mudiyanselage – S401456
- Balatripurasundari Polineni – S401680
- Prabodha Sathsarani Aththanayake Aththanayake Boralage – S401279

---

# Overview

This assignment is a **Spot the Difference desktop game** developed using Python.

The application allows the user to load an image, automatically creates a modified version of that image with hidden differences, and lets the player identify the differences by clicking on the modified image.

The project uses:

- **Tkinter** for the graphical user interface
- **OpenCV** for image processing
- **Pillow** for displaying OpenCV images in Tkinter
- **Object-Oriented Programming** for clean project structure

---

# Project Features

## Main Game Features

- Load an image from the computer
- Automatically generate a modified image
- Create 5 hidden differences
- Display original and modified images side by side
- Allow the player to click on the modified image
- Detect correct and incorrect clicks
- Show remaining differences
- Track mistakes
- Track round score and total score
- Lock the round after maximum mistakes
- Show completion message when all differences are found
- Reveal all unfound differences
- Draw circles around found and revealed differences

---

# Image Processing Features

The application uses OpenCV to generate different types of image changes.

## Image Effects Used

- Colour shift effect
- Blur effect
- Brightness effect
- Greyscale effect
- Pixelation effect
- Contrast effect

# Object-Oriented Programming Usage

This project uses OOP to separate responsibilities into different classes.

## Main Classes

### `SpotTheDifferenceApplication`

Controls the main application flow and connects the GUI, image processing, and game logic.

### `MainLayout`

Creates and manages the Tkinter GUI layout, including buttons, labels, status messages, and image display areas.

### `ImageDisplayHelper`

Handles image resizing, conversion from OpenCV images to Tkinter-compatible images, and drawing difference circles.

### `GameManager`

Manages the game state, including loaded images, scores, mistakes, remaining differences, round lock status, click validation, and reveal logic.

### `Difference`

Stores one hidden difference region, including its position, size, alteration type, and state.

### `DifferenceClickDetector`

Checks whether a player click matches an already found or unresolved difference.

### `ImageLoader`

Loads and validates image files.

### `ModifiedImageBuilder`

Creates the modified image, generates difference areas, checks overlap, selects effects, and applies image changes.

### `ImageEffect`

Base class for image effects.

Child classes include:

- `ColourEffect`
- `BlurEffect`
- `BrightnessEffect`
- `GreyscaleEffect`
- `PixelateEffect`
- `ContrastEffect`

---

# OOP Concepts Demonstrated

- *Encapsulation* – related data and behaviour are kept inside classes.
- *Abstraction* – complex logic is hidden behind meaningful methods.
- *Inheritance* – image effect classes inherit from the base ImageEffect class.
- *Polymorphism* – each image effect class implements its own apply() method.
- *Composition* – main classes use objects from other classes.
- *Dataclass usage* – the Difference model stores difference region data cleanly.
- *Separation of responsibilities* – GUI, game logic, image processing, and utilities are separated.

---

# Project Structure

```text
HIT137-Assignment-3/
│
├── main.py
│
├── core/
│   ├── _init_.py
│   ├── difference.py
│   ├── difference_click_detector.py
│   └── game_manager.py
│
├── gui/
│   ├── _init_.py
│   ├── app.py
│   ├── layout.py
│   └── image_display_helper.py
│
├── image_processing/
│   ├── _init_.py
│   ├── image_loader.py
│   ├── image_modifier.py
│   └── image_effect.py
│
├── utils/
│   ├── _init_.py
│   ├── constants.py
│   ├── helpers.py
│   └── status_messages.py
│
├── requirements.txt
└── README.md