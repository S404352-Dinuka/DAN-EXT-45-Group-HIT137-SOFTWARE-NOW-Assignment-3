# HIT137 Assignment 3

# Group Members

- Dinuka Dhaneshani Mathangaweera – S404352
- Sehan Hansaja Udayakantha Panik Mudiyanselage – S401456
- Balatripurasundari Polineni – S401680
- Prabodha Sathsarani Aththanayake Aththanayake Boralage – S401279

---

# Python Version Requirement

This project was implemented using **Python 3.14.3**.

---
# How to Run the Application

Follow these steps from the project root folder


## 1. Install Required Libraries

```bash
python3 -m pip install -r requirements.txt
```

On Windows, use:

```bash
python -m pip install -r requirements.txt
```

## 2. Run the Application

```bash
python3 main.py
```

On Windows, use

```bash
python main.py
```

## 3. Start Playing

After the application opens:

1. Click **Load Image**
2. Select a supported image file
3. The original and modified images will be displayed side by side
4. Click on the modified image to find the differences
5. Correct clicks are marked with red circles
6. Wrong clicks increase the mistake count
7. The round is locked after the maximum number of mistakes
8. Click **Reveal Differences** to reveal all remaining unfound differences
9. Load a new image to start a new round

---

# Overview

This assignment is a **Spot the Difference desktop game** developed using Python.

The application allows the user to load an image, automatically creates a modified version of that image with hidden differences, and lets the player identify the differences by clicking on the modified image.

The project uses:

- **Tkinter** for the graphical user interface
- **OpenCV** for image processing
- **Object-Oriented Programming** for clean project structure

---

# Supported Image Formats

The application supports common image formats:

- JPG
- JPEG
- PNG
- BMP

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

The application uses OpenCV to generate different types of image changes

## Image Effects Used

- Colour shift effect
- Blur effect
- Brightness effect
- Greyscale effect
- Pixelation effect
- Contrast effect

---

# Object-Oriented Programming Usage

This project uses OOP to separate responsibilities into different classes

## Main Classes

### `SpotTheDifferenceApplication`

Controls the main application flow and connects the GUI, image processing, image loading, and game logic

### `MainLayout`

Creates and manages the Tkinter GUI layout, including buttons, labels, status messages, statistic cards, and image display areas

### `ImageDisplayHelper`

Handles image resizing, conversion from OpenCV images to Tkinter-compatible images, and drawing difference circles

### `GameStateManager`

Manages the game state, including loaded images, scores, mistakes, remaining differences, round lock status, click validation, and reveal logic

### `Difference`

Stores one hidden difference region, including its position, size, alteration type, found state, and revealed state

### `DifferenceClickDetector`

Checks whether a player click matches an already found or unresolved difference

### `ImageLoader`

Loads and validates image files selected by the user

### `ModifiedImageBuilder`

Creates the modified image, generates difference areas, checks overlap, selects effects, and applies image changes

### `ImageEffect`

Base class for image effects

Child classes include:

- `ColourEffect`
- `BlurEffect`
- `BrightnessEffect`
- `GreyscaleEffect`
- `PixelateEffect`
- `ContrastEffect`

---

# OOP Concepts 

- **Encapsulation** – related data and behaviour are kept inside classes
- **Abstraction** – complex logic is hidden behind meaningful methods
- **Inheritance** – image effect classes inherit from the base `ImageEffect` class
- **Polymorphism** – each image effect class implements its own `apply()` method
- **Composition** – main classes use objects from other classes
- **Dataclass usage** – the `Difference` model stores difference region data cleanly
- **Separation of responsibilities** – GUI, game logic, image processing, and utilities are separated

---

# Testing Completed

The following features were tested:

- Application opens before loading an image
- Image loading window opens when clicking Load Image
- Supported image types are shown in the file selection window
- Loading supported image formats
- Cancelling image selection
- Displaying original and modified images
- Generating exactly 5 differences
- Clicking correct differences
- Clicking already found differences
- Clicking incorrect areas
- Updating remaining count
- Updating score
- Updating mistake count
- Locking the round after 3 mistakes
- Revealing unfound differences
- Loading a new image after a round is completed or locked
- Ensuring difference regions do not overlap
- Ensuring difference marker circles do not overlap
- Ensuring image effects are visible but not too obvious

---

