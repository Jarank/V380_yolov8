from customtkinter import *
from v380_camera_gui import V380Camera


def main():
    # Set appearance mode and color theme
    set_appearance_mode("dark")
    set_default_color_theme("blue")

    # Create main window
    root = CTk()
    root.resizable(True, True)

    # Instantiate the V380Camera class
    app = V380Camera(root)

    # Handle window close event
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    main()
