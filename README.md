# HIT137 Assignment 3 – README
## Group Members
- Dinuka Dhaneshani Mathangaweera – S404352
- Sehan Hansaja Udayakantha Panik Mudiyanselage – S401456
- Balatripurasundari Polineni – S401680
- Prabodha Sathsarani Aththanayake Aththanayake Boralage – S401279

---


# Python Version Requirement

This project requires **Python 3.9 or above**.

This is because the implementation uses built-in generic type hints such as:

def evaluate_file(input_path: str) -> list[dict]:

The list[dict] syntax is only supported in Python 3.9 and later versions.

---

# Dependencies

Install the required libraries using pip:

```bash
pip install opencv-python pillow
```

Library                   Purpose                            
`tkinter`                 GUI framework (built into Python)  
`opencv-python`           Image processing and manipulation 
`Pillow`                  Displaying images in Tkinter       

---


# Overview

This is a desktop **Spot the Difference** game. It uses 
- **OOP** – Object-Oriented Programming principles
- **Tkinter** – GUI development
- **OpenCV** – Image processing

Two images are shown side by side. They look almost the same. One has **5 hidden differences**. You click on the image you think is different to find them. The app will then tell you if you are correct or not.

# Project Structure

```
spot_the_difference/
│
├── main.py                        # Entry point – launches the application        [Bala]
│
├── gui/                           # Tkinter GUI layer                             [Prabodha]
│   ├── __init__.py
│   ├── app.py                     # Main application window
│   ├── layout.py                  # UI layout and widget arrangement
│   └── canvas_view.py             # Canvas rendering for images and overlays
│
├── core/                          # Game logic layer                              [Dinuka]
│   ├── __init__.py
│   ├── game_manager.py            # Controls game state and round flow
│   ├── difference_detector.py     # Click validation against difference regions
│   └── models.py                  # Data models (DifferenceRegion, GameState, etc.)
│
├── image_processing/              # OpenCV image processing layer                 [Sehan]
│   ├── __init__.py
│   ├── image_loader.py            # Loads and scales images from disk
│   ├── modified_image_builder.py          # Generates the modified image with 5 differences
│   └── alterations.py             # Individual alteration types (colour shift, blur, etc.)
│
├── utils/                         # Shared utilities                              [Bala]
│   ├── __init__.py
│   ├── constants.py               # App-wide constants (e.g. max mistakes, region size)
│   └── helpers.py                 # Reusable helper functions
│
├── assets/
│   └── sample_images/             # Sample images for testing
│
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── github_link.txt                # GitHub repository URL
```
# Functional Requirements

## 1. Object-Oriented Programming

The code is split into classes that are put into separate parts, which shows that:
- **Encapsulation** - Each part of the code **keeps its own information and actions** to itself
- **Constructors and methods** - The code uses ** setup routines and actions** that are easy to understand
- **Class interaction** - The different parts of the code like the user interface, main program and image processing **talk to each other in a simple way**
- **Inheritance and polymorphism** - The code uses **a common base** for different types of changes like the ones, in the alterations file so they can work together easily.

## 2. Image Processing with OpenCV

When the image is loading the `modified_image_builder.py` script makes a copy of the image. Then it adds exactly **5 differences** at spots. These changes do not overlap with each other.

Type           -     Description 
Colour Shift         A rectangular area of the image has its colour changed. Can see the 
                     difference if you look closely but it is not obvious
Brightness Change    A part of the image is made a bit lighter or darker 
Blur                 A region is softened using Gaussian blur

# 3. Tkinter GUI

### Image Loading and Display

- A **Load Image** button helps to pick a JPG, PNG or BMP file from computer
- The **original image** is on the left just for you to look at
- The **modified image** is on the right and you can click on it

### Finding Differences

- A counter shows how differences still need to find (`Remaining: X`)
- When click correctly a **red circle** appears around the difference on **both** images
- When find all 5 differences, a pop-up tells you and you can load a new image

### Mistakes

- If click incorrectly it counts as a mistake. Can see the total on the screen
- Can make a maximum of **3 mistakes** per image
- If make 3 mistakes you can't click anymore. It clearly shows on the screen
- Then, can load an image to start over

### Reveal

- A **Reveal** button marks all remaining differences with a **blue circle** on both images
- After revealing you can load a new image to play again

---

# How to Run

```bash

python main.py

```

1. Click **Load Image**. Choose a JPG, PNG or BMP file
2. Look carefully at both images. Click the **right image** where you see a difference
3. A **red circle** means found it right; a wrong click adds a mistake
4. Use **Reveal** anytime to highlight remaining differences in
5. Load an image to play another round

---

# GitHub Repository

The GitHub repository link is, in `github_link.txt`.

All group work and version history are recorded there.

---

# Submission

- All programming files, outputs and `github_link.txt` are zipped and uploaded to **Learline**

- The GitHub repository is set to **public**

