import os
import sys
import time
import ctypes
from PIL import Image, ImageGrab

def is_admin() -> bool:
    """Check if the current python process is running with Administrator privileges on Windows."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def capture_screenshot_fallback(output_path: str) -> tuple[bool, str, str]:
    """
    Attempts to capture a full screen image using multiple fallback strategies
    to overcome potential Antivirus blocks or OS permissions issues.

    Returns:
        (success: bool, output_path_or_error: str, method_name: str)
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    errors = []

    # Strategy 1: PIL ImageGrab (Standard GDI grab)
    try:
        img = ImageGrab.grab(all_screens=True)
        if img is not None:
            img.save(output_path)
            return True, output_path, "PIL ImageGrab"
    except Exception as e:
        errors.append(f"PIL.ImageGrab failed: {e}")

    # Strategy 2: MSS (Direct DXGI / Windows API monitor capture)
    try:
        import mss
        with mss.mss() as sct:
            # Grab full virtual screen (monitor 0 is all monitors combined)
            monitor = sct.monitors[0]
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img.save(output_path)
            return True, output_path, "MSS DXGI"
    except Exception as e:
        errors.append(f"MSS failed: {e}")

    # Strategy 3: Low-level Win32 GDI BitBlt via ctypes
    try:
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32

        # Get virtual screen metrics
        SM_XVIRTUALSCREEN = 76
        SM_YVIRTUALSCREEN = 77
        SM_CXVIRTUALSCREEN = 78
        SM_CYVIRTUALSCREEN = 79

        left = user32.GetSystemMetrics(SM_XVIRTUALSCREEN)
        top = user32.GetSystemMetrics(SM_YVIRTUALSCREEN)
        width = user32.GetSystemMetrics(SM_CXVIRTUALSCREEN)
        height = user32.GetSystemMetrics(SM_CYVIRTUALSCREEN)

        if width == 0 or height == 0:
            left, top = 0, 0
            width = user32.GetSystemMetrics(0) # SM_CXSCREEN
            height = user32.GetSystemMetrics(1) # SM_CYSCREEN

        hdesktop = user32.GetDesktopWindow()
        desktop_dc = user32.GetWindowDC(hdesktop)
        img_dc = gdi32.CreateCompatibleDC(desktop_dc)
        mem_bitmap = gdi32.CreateCompatibleBitmap(desktop_dc, width, height)
        gdi32.SelectObject(img_dc, mem_bitmap)

        SRCCOPY = 0x00CC0020
        # BitBlt screen to memory bitmap DC
        bitblt_result = gdi32.BitBlt(img_dc, 0, 0, width, height, desktop_dc, left, top, SRCCOPY)

        if bitblt_result != 0:
            class BITMAPINFOHEADER(ctypes.Structure):
                _fields_ = [
                    ('biSize', ctypes.c_uint32),
                    ('biWidth', ctypes.c_int32),
                    ('biHeight', ctypes.c_int32),
                    ('biPlanes', ctypes.c_uint16),
                    ('biBitCount', ctypes.c_uint16),
                    ('biCompression', ctypes.c_uint32),
                    ('biSizeImage', ctypes.c_uint32),
                    ('biXPelsPerMeter', ctypes.c_int32),
                    ('biYPelsPerMeter', ctypes.c_int32),
                    ('biClrUsed', ctypes.c_uint32),
                    ('biClrImportant', ctypes.c_uint32)
                ]

            bmi = BITMAPINFOHEADER()
            bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
            bmi.biWidth = width
            bmi.biHeight = -height  # top-down image
            bmi.biPlanes = 1
            bmi.biBitCount = 32
            bmi.biCompression = 0 # BI_RGB

            buffer_size = width * height * 4
            buffer = ctypes.create_string_buffer(buffer_size)
            
            gdi32.GetDIBits(desktop_dc, mem_bitmap, 0, height, buffer, ctypes.byref(bmi), 0)
            
            img = Image.frombuffer("RGBA", (width, height), buffer, "raw", "BGRA", 0, 1).convert("RGB")
            img.save(output_path)

            # Cleanup GDI handles
            gdi32.DeleteObject(mem_bitmap)
            gdi32.DeleteDC(img_dc)
            user32.ReleaseDC(hdesktop, desktop_dc)

            return True, output_path, "Win32 GDI BitBlt"
        else:
            gdi32.DeleteObject(mem_bitmap)
            gdi32.DeleteDC(img_dc)
            user32.ReleaseDC(hdesktop, desktop_dc)
            errors.append("Win32 BitBlt returned 0")
    except Exception as e:
        errors.append(f"Win32 GDI BitBlt failed: {e}")

    # If all methods failed:
    admin_status = "Admin privileges ACTIVE" if is_admin() else "Admin privileges NOT ACTIVE (running as standard user)"
    err_summary = "; ".join(errors)
    return False, f"All screenshot capture methods failed. [{admin_status}]. Details: {err_summary}", "None"


def capture_photo_fallback(output_path: str) -> tuple[bool, str, str]:
    """
    Attempts to capture a photo from webcam using multiple OpenCV backends and device indices
    to handle potential Antivirus blocking or webcam device locks.

    Returns:
        (success: bool, output_path_or_error: str, method_name: str)
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    import cv2

    backends = [
        ("DirectShow", cv2.CAP_DSHOW),
        ("Media Foundation", cv2.CAP_MSMF),
        ("Default OpenCV Driver", cv2.CAP_ANY)
    ]

    camera_indices = [0, 1, 2]
    errors = []

    for cam_idx in camera_indices:
        for backend_name, backend_api in backends:
            cap = None
            try:
                cap = cv2.VideoCapture(cam_idx, backend_api)
                if not cap.isOpened():
                    cap.release()
                    continue

                # Give camera sensor a moment to initialize & adjust exposure
                time.sleep(0.3)
                
                # Warm-up frames
                for _ in range(3):
                    cap.read()

                ret, frame = cap.read()
                cap.release()

                if ret and frame is not None and frame.size > 0:
                    cv2.imwrite(output_path, frame)
                    return True, output_path, f"Webcam (Index {cam_idx}, {backend_name})"
            except Exception as e:
                if cap is not None:
                    try:
                        cap.release()
                    except Exception:
                        pass
                errors.append(f"Cam {cam_idx} with {backend_name} failed: {e}")

    admin_status = "Admin privileges ACTIVE" if is_admin() else "Admin privileges NOT ACTIVE (running as standard user)"
    err_msg = (
        f"Failed to capture photo from webcam. Camera might be in use, disabled, or blocked by Antivirus/Privacy settings. "
        f"[{admin_status}]. Details: {'; '.join(errors) if errors else 'No camera device responded.'}"
    )
    return False, err_msg, "None"
