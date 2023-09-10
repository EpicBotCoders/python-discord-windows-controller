from PIL import ImageGrab
import pygetwindow as gw

def capture_screenshot():
    try:
        # Get the active window
        active_window = gw.getWindowsWithTitle("")[0]  # Pass an empty string to get the active window

        # Capture a low-resolution screenshot of the active window
        screenshot = ImageGrab.grab(bbox=(
            active_window.left, active_window.top,
            active_window.right, active_window.bottom
        ))

        return screenshot

    except Exception as e:
        print(f"Error capturing screenshot: {str(e)}")
        return None
