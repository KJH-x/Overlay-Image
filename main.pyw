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
        self.image = QtGui.QPixmap(config["file"]["display"])

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


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, config: Config, parent=None):
        # Create tray icon
        super().__init__(QtGui.QIcon(config["file"]["icon"]), parent)
        self.setToolTip("Overlay Image")

        # Create menu for tray (Exit)
        menu = QtWidgets.QMenu()
        if (exit_action := menu.addAction("Exit")):
            exit_action.triggered.connect(QtWidgets.QApplication.quit)
            self.setContextMenu(menu)

        # Connect to tray activate function
        self.activated.connect(self.on_tray_icon_activated)

        self.show()

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
    tray_icon = SystemTrayIcon(config)

    # Main loop
    sys.exit(app.exec_())