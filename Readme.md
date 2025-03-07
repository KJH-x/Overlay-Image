# Overlay Image Script

## Description

This script creates a transparent, click-through overlay that displays an image centered on the screen. It utilizes PyQt5 to render the image and provides a system tray icon for easy exit functionality.

## Features

- Displays an image as an always-on-top overlay.
- Click-through functionality (input transparency).
- System tray icon for easy exit.
- Configurable through `config.json`.

## Prerequisites

Ensure you have the following installed:

- Python 3.8+
- PyQt5 (`pip install PyQt5`)

## Configuration

Create a `config.json` file in the same directory as the script. The file should be structured as follows:

```json
{
    "file": {
        "display": "example.png",
        "icon": "icon.png"
    }
}
```

- `display`: Path to the image file to be shown as an overlay.
- `icon`: Path to the system tray icon image.

## Usage

1. Ensure `config.json` is properly set up with valid image paths.
2. Run the script:

   ```sh
   python main.pyw
   ```

3. To exit, use the system tray menu or double-click the icon.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This script is provided "as is" without warranty of any kind. Use at your own risk.
