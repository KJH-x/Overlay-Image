# Overlay Image Script

## Description

This script creates a transparent, click-through overlay that displays an image centered on the screen. It utilizes PyQt5 to render the image and provides a system tray icon for easy management and control.

## Features

- Displays an image as an always-on-top overlay
- Click-through functionality (input transparency)
- System tray icon for easy management
- Image switching functionality through system tray menu
  - Groups images with same prefix and different resolutions (e.g., <image@1x.png>, <image@2x.png>)
  - Single images appear directly in the main menu
- Configurable through `config.json`

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

- `display`: Path to the image file to be shown as an overlay (on startup).
- `icon`: Path to the system tray icon image.

## Usage

1. Ensure config.json is properly set up with valid image paths
2. Place your PNG images in the same directory as the script
3. Run the script:

   ```sh
   python main.pyw
    ```

4. Use the system tray icon to:
    - Switch between different PNG images in the directory
      - Images with same prefix are grouped (e.g., <logo@1x.png>, <logo@2x.png>)
      - Single images appear directly in the main menu
    - Exit the application (via menu or double-click)

## License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

## Disclaimer

This script is provided "as is" without warranty of any kind. Use at your own risk.
