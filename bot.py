import discord
import os
import json
import socket
import asyncio
import pyautogui
from commands.mouse_movement import monitor_mouse_movement

KEY_PATH = "D:\Coding\Discord bots\python-windows-bot\key.txt"
CONFIG_PATH = "D:\Coding\Discord bots\python-windows-bot\config.json"

def is_connected():
    try:
        # Try to resolve a common domain to check if the network is available
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def load_config():
    print("Loading configuration file...")
    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)
        return config

async def network_monitor():
    while True:
        if not is_connected():
            print("Network connection lost. Waiting for network...")
            while not is_connected():
                await asyncio.sleep(5)  # Wait for 5 seconds before checking again
            print("Network has been restored.")
        await asyncio.sleep(60)  # Check network status every 60 seconds

async def main():
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, "r") as f:
            TOKEN = f.read()
    else:
        TOKEN = ""

    intents = discord.Intents.default()
    intents.message_content = True
    config = load_config()

    client = discord.Client(intents=intents)

    # Start the network monitoring task in the background
    asyncio.create_task(network_monitor())

    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")
        starting_mouse_position = pyautogui.position()
        asyncio.create_task(
            monitor_mouse_movement(client, config, starting_mouse_position)
        )  # Call the function

    @client.event
    async def on_message(message):
        msg = str(message.content).lower().split(' ')[0]
        args = message.content.split(" ")[1:]

        if (
            message.author == client.user
            or message.channel.id != config["command_channel_id"]
        ):
            return

        if message.author.bot or message.author.id != config["author_id"]:
            return
        
        if str(message.attachments) != "[]":
            from commands.file_save import execute_file_save

            await execute_file_save(client, message, config)

        if msg == "lock":
            from commands.lock_command import execute_lock_command

            await execute_lock_command(client, message, config)

        if msg == "ping":
            from commands.ping_command import execute_ping_command

            await execute_ping_command(client, message, config)
        
        if msg == "ss" or msg == "screenshot":
            from commands.screenshot_command import execute_screenshot_command
            await execute_screenshot_command(message, args)

    await client.start(TOKEN)

asyncio.run(main())
