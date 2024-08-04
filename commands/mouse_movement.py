import discord
import asyncio
import pyautogui
import json
import datetime
from PIL import ImageGrab
import time
import cv2
import os

DATA_JSON_PATH = "data/data.json"
SCREENSHOT_PATH = "data/mouse-ss.png"
WEBCAM_CAPTURE_PATH = "data/webcam-capture.jpg"
COMBINED_IMAGE_PATH = "data/combined_image.png"

async def monitor_mouse_movement(client, config, starting_mouse_position):
    log_channel_id = config["mouse_log_channel_id"]
    log_channel = client.get_channel(log_channel_id)
    last_message = None
    image_message_id = None
    last_movement_time = None
    image_message = None

    previous_mouse_position = starting_mouse_position

    try:
        with open(DATA_JSON_PATH, "r") as data_file:
            data = json.load(data_file)
            last_message_id = data.get("last_message_id")
            image_message_id = data.get("image_message_id")
            if last_message_id:
                last_message = await log_channel.fetch_message(last_message_id)
            if image_message_id:
                try:
                    image_message = await log_channel.fetch_message(image_message_id)
                except discord.NotFound:
                    image_message = None
            last_movement_time = data.get("last_movement_time")
            if last_movement_time:
                last_movement_time = datetime.datetime.strptime(
                    last_movement_time, "%d-%m-%Y %H:%M:%S"
                )
    except (FileNotFoundError, json.JSONDecodeError, discord.NotFound, ValueError):
        pass

    while True:
        current_mouse_position = pyautogui.position()

        if current_mouse_position != previous_mouse_position:
            current_time = int(time.time())
            print(f"[mouse_movement_LOG] - {last_movement_time} : Mouse Movement Detected.")
            message = f"Mouse moved to `{current_mouse_position[0]}`, `{current_mouse_position[1]}` at "+f'<t:{current_time}>'
            last_movement_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            try:
                screenshot = ImageGrab.grab()
                screenshot.save(SCREENSHOT_PATH)
            except OSError as e:
                print(f"[mouse_movement_LOG] - Error capturing screenshot: {e}")
                await asyncio.sleep(5)
                continue

            # Capture webcam image
            webcam = cv2.VideoCapture(0)
            ret, frame = webcam.read()
            webcam.release()

            if ret:
                cv2.imwrite(WEBCAM_CAPTURE_PATH, frame)
                webcam_capture = cv2.imread(WEBCAM_CAPTURE_PATH)
                
                if webcam_capture is not None:
                    screenshot = cv2.imread(SCREENSHOT_PATH)
                    
                    if screenshot is not None:
                        max_width = 200
                        max_height = 150
                        scale_ratio = min(max_width / webcam_capture.shape[1], max_height / webcam_capture.shape[0])

                        webcam_capture_resized = cv2.resize(webcam_capture, (0, 0), fx=scale_ratio, fy=scale_ratio)

                        x_offset = 10
                        y_offset = 10

                        screenshot[y_offset:y_offset+webcam_capture_resized.shape[0], x_offset:x_offset+webcam_capture_resized.shape[1]] = webcam_capture_resized

                        cv2.imwrite(COMBINED_IMAGE_PATH, screenshot)

                        image_message = await log_channel.send(
                            message, file=discord.File(COMBINED_IMAGE_PATH)
                        )
                        print(f"[mouse_movement_LOG] - {last_movement_time} : Mouse SS sent.")
                    else:
                        print("[mouse_movement_LOG] - Error reading screenshot.")
                        image_message = await log_channel.send(message)
                else:
                    print("[mouse_movement_LOG] - Error reading webcam capture.")
                    image_message = await log_channel.send(message)
            else:
                print("[mouse_movement_LOG] - Error capturing webcam image.")
                image_message = await log_channel.send(message)

            if last_message:
                await last_message.edit(content=message)
            else:
                last_message = await log_channel.send(message)

            with open(DATA_JSON_PATH, "w") as data_file:
                json.dump(
                    {
                        "last_message_id": last_message.id,
                        "image_message_id": image_message.id,
                        "last_movement_time": last_movement_time,
                    },
                    data_file,
                )
        else:
            message = f"No mouse movement detected. Last movement at `{last_movement_time}`\nCurrent Position: `{current_mouse_position[0]}`, `{current_mouse_position[1]}`"
            if last_message:
                await last_message.edit(content=message)
            else:
                last_message = await log_channel.send(message)

        previous_mouse_position = current_mouse_position
        await asyncio.sleep(5)