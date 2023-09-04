# commands/mouse_movement.py

import discord
import asyncio
import pyautogui  # Import PyAutoGUI library
import json
import datetime

async def monitor_mouse_movement(client, config, starting_mouse_position):
    log_channel_id = config["mouse_log_channel_id"]  # Use the separate mouse log channel
    log_channel = client.get_channel(log_channel_id)
    last_message = None
    last_movement_time = None  # Variable to store the last movement time

    previous_mouse_position = starting_mouse_position  # Get the initial mouse position

    # Load the last_message and last_movement_time from data.json if available
    try:
        with open("data/data.json", "r") as data_file:
            data = json.load(data_file)
            last_message_id = data.get("last_message_id")
            if last_message_id:
                last_message = await log_channel.fetch_message(last_message_id)
            last_movement_time = data.get("last_movement_time")
            if last_movement_time:
                last_movement_time = datetime.datetime.strptime(last_movement_time, "%d-%m-%Y %H:%M:%S")
    except (FileNotFoundError, json.JSONDecodeError, discord.NotFound, ValueError):
        pass

    while True:
        current_mouse_position = pyautogui.position()  # Get the current mouse position

        # Check if the mouse has moved since the last check
        if current_mouse_position != previous_mouse_position:
            message = f"Mouse moved to `{current_mouse_position[0]}`, `{current_mouse_position[1]}`"
            last_movement_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            if last_message:
                # If a previous log message exists, edit it with the new message
                await last_message.edit(content=message)
            else:
                # If there's no previous log message, send a new one
                last_message = await log_channel.send(message)

            # Store the last_message_id and last_movement_time in data.json
            with open("data/data.json", "w") as data_file:
                json.dump({"last_message_id": last_message.id, "last_movement_time": last_movement_time}, data_file)
        else:
            message = f"No mouse movement detected. Last movement at `{last_movement_time}`\nCurrent Position: `{current_mouse_position[0]}`, `{current_mouse_position[1]}`"
            if last_message:
                # If a previous log message exists, edit it with the new message
                await last_message.edit(content=message)
            else:
                # If there's no previous log message, send a new one
                last_message = await log_channel.send(message)

        previous_mouse_position = current_mouse_position  # Update the previous position

        # Wait for 5 seconds before checking again
        await asyncio.sleep(5)
