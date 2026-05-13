"""
This module is the entry point for the Spot the Difference application
"""

try:
    import tkinter as tk
    from gui.app import SpotTheDifferenceApplication

except Exception as import_error:
    print("A required library or project file could not be loaded.")
    print("Install requirements with: python3 -m pip install -r requirements.txt")
    print("Exact error:", import_error)
    raise SystemExit(1)


def main():
    """
    This function starts the Spot the Difference application
    It creates the main Tkinter window, initializes the application controller and starts the Tkinter event loop
    """
    root = tk.Tk()
    SpotTheDifferenceApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()