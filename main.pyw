import json
import os
import sys
from typing import Dict, Union

from PyQt5 import QtCore, QtGui, QtWidgets

# Define type alias for configuration
Config = Dict[str, Dict[str, str]]


def load_config(config_path: str) -> Config:
    """Load and validate the configuration file."""
    if not os.path.exists(config_path):
        print("Config file not found!")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    if not isinstance(config, dict) or not all(isinstance(v, dict) and all(isinstance(i, str) for i in v.values()) for v in config.values()):
        print("Invalid config structure! Expected Dict[str, Dict[str, str]]")
        sys.exit(1)

    return config


class Overlay(QtWidgets.QWidget):
    def __init__(self, config: Config):
        super().__init__()

        # Load the PNG image
        self.image_path = config["file"]["display"]
        if not os.path.exists(self.image_path):
            print(f"Not Available: {self.image_path}")
            sys.exit(1)
        self.load_image(self.image_path)

        # Set window title and icon for taskbar
        self.setWindowTitle(config["file"]["display"])
        self.setWindowIcon(QtGui.QIcon(config["file"]["icon"]))

        # no Frame, Alwsys Top, Input Transparent (Click-Through), No taskbar, standalone
        self.setWindowFlags(
            QtCore.Qt.WindowType(
                # Note: Technically this QtCore.Qt.WindowType() is unnecessary
                #       However the definition of WindowType is WindowType(int),
                #       Pylance see operator "|" and think the result can only be int
                #       Which might be solve by defining WindowType operation.
                # Flags should be pass at a time, seperating the bracket leads to malfunction
                QtCore.Qt.WindowType.FramelessWindowHint
                | QtCore.Qt.WindowType.WindowStaysOnTopHint
                | QtCore.Qt.WindowType.WindowTransparentForInput
                | QtCore.Qt.WindowType.Tool
                | QtCore.Qt.WindowType.Window
            )
        )

        # Enable a transparent background (Differ from the upper Type Hint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # Resize to screen size
        if (QScreen := QtWidgets.QApplication.primaryScreen()):
            screen_geometry = QScreen.geometry()
            self.setGeometry(screen_geometry)

        self.showFullScreen()

    # Redrawn Event triggered (Automatic, Function name must be named exactly like this)
    def paintEvent(self, event):
        """Handles painting the PNG onto the transparent window."""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing, True)

        if (QScreen := QtWidgets.QApplication.primaryScreen()):
            screen_geometry = QScreen.geometry()
            screen_width, screen_height = screen_geometry.width(), screen_geometry.height()

        img_width, img_height = self.image.width(), self.image.height()

        display_width = img_width
        display_height = img_height

        # Center the image
        x = (screen_width - img_width) // 2
        y = (screen_height - img_height) // 2

        print(f"IMG    : {self.image_path} : {img_width} x {img_height}")
        print(f"DISPLAY: {screen_width} x {screen_height}")
        print(f"PAINT  : {x} ,{y} ,{display_width} x {display_height}")

        # Draw the PNG image at the center
        painter.drawPixmap(x, y, display_width, display_height, self.image)

    def load_image(self, image_path):
        """Load image and update image path"""
        self.image_path = image_path
        self.image = QtGui.QPixmap(image_path)
        # Redraw window to display new image
        self.update()


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, config: Config, overlay=None, parent=None):
        # Create tray icon
        super().__init__(QtGui.QIcon(config["file"]["icon"]), parent)
        self.setToolTip("Overlay Image")
        self.config = config
        self.overlay = overlay

        # Create menu for tray
        menu = QtWidgets.QMenu()

        # Add switch image submenu
        self.switch_menu = QtWidgets.QMenu("Switch Image")
        menu.addMenu(self.switch_menu)
        self.update_image_menu()

        # Add exit option
        if (exit_action := menu.addAction("Exit")):
            exit_action.triggered.connect(QtWidgets.QApplication.quit)
            self.setContextMenu(menu)

        # Connect to tray activate function
        self.activated.connect(self.on_tray_icon_activated)

        self.show()

    def update_image_menu(self):
        self.switch_menu.clear()
        # get all png files in current directory
        png_files = [f for f in os.listdir("./") if f.lower().endswith(".png")]

        for png_file in png_files:
            # extract file name without extension
            file_name = os.path.splitext(png_file)[0]
            action = self.switch_menu.addAction(file_name)
            action.triggered.connect(lambda checked, file=png_file: self.switch_image(file))

    def switch_image(self, image_file):
        if self.overlay:
            image_path = os.path.join(os.getcwd(), image_file)
            self.config["file"]["display"] = image_path
            # Load new image and redraw
            self.overlay.load_image(image_path)
            print(f"Image switched to: {image_path}")

    def on_tray_icon_activated(self, reason):
        # Double click tray icon also leads to exit.
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.DoubleClick:
            QtWidgets.QApplication.quit()


if __name__ == "__main__":
    # Create QT base
    app = QtWidgets.QApplication(sys.argv)

    # Read configuration file
    config_path = "config.json"
    config = load_config(config_path)

    overlay = Overlay(config)
    tray_icon = SystemTrayIcon(config, overlay)

    # Main loop
    sys.exit(app.exec_())
