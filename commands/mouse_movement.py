# commands/mouse_movement.py

import discord
import asyncio
import pyautogui
import json
import datetime
from PIL import ImageGrab

async def monitor_mouse_movement(client, config, starting_mouse_position):
    log_channel_id = config["mouse_log_channel_id"]
    log_channel = client.get_channel(log_channel_id)
    last_message = None
    image_message_id = None
    last_movement_time = None
    image_message = None  # Define image_message here to ensure it's initialized

    previous_mouse_position = starting_mouse_position

    try:
        with open("data/data.json", "r") as data_file:
            data = json.load(data_file)
            last_message_id = data.get("last_message_id")
            image_message_id = data.get("image_message_id")
            if last_message_id:
                last_message = await log_channel.fetch_message(last_message_id)
            if image_message_id:
                try:
                    image_message = await log_channel.fetch_message(image_message_id)
                except discord.NotFound:
                    image_message = None  # Set image_message to None if the message is not found
            last_movement_time = data.get("last_movement_time")
            if last_movement_time:
                last_movement_time = datetime.datetime.strptime(last_movement_time, "%d-%m-%Y %H:%M:%S")
    except (FileNotFoundError, json.JSONDecodeError, discord.NotFound, ValueError):
        pass

    while True:
        current_mouse_position = pyautogui.position()

        if current_mouse_position != previous_mouse_position:
            message = f"Mouse moved to `{current_mouse_position[0]}`, `{current_mouse_position[1]}`"
            last_movement_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            screenshot = ImageGrab.grab(bbox=(0, 0, 800, 600))

            screenshot.save("data/screenshot.png")

            # Check if image_message is not None and attempt to delete it if it exists
            if image_message:
                try:
                    await image_message.delete()
                except discord.NotFound:
                    pass  # Message already deleted or not found

            image_message = await log_channel.send(message, file=discord.File("data/screenshot.png"))

            if last_message:
                await last_message.edit(content=message)
            else:
                last_message = await log_channel.send(message)

            with open("data/data.json", "w") as data_file:
                json.dump({"last_message_id": last_message.id, "image_message_id": image_message.id, "last_movement_time": last_movement_time}, data_file)
        else:
            message = f"No mouse movement detected. Last movement at `{last_movement_time}`\nCurrent Position: `{current_mouse_position[0]}`, `{current_mouse_position[1]}`"
            if last_message:
                await last_message.edit(content=message)
            else:
                last_message = await log_channel.send(message)

        previous_mouse_position = current_mouse_position
        await asyncio.sleep(5)
