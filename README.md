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

