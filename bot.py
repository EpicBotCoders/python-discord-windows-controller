import discord
import os
import json
import socket
import asyncio
import pyautogui
from commands.mouse_movement import monitor_mouse_movement
from aiohttp.client_exceptions import ClientConnectorError

KEY_PATH = "key.txt"
CONFIG_PATH = "config.json"

def is_connected():
    try:
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
                await asyncio.sleep(5)
            print("Network has been restored.")
        await asyncio.sleep(60)

async def main():
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, "r") as f:
            TOKEN = f.read().strip()
    else:
        TOKEN = ""

    intents = discord.Intents.default()
    intents.message_content = True
    config = load_config()

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")
        starting_mouse_position = pyautogui.position()
        asyncio.create_task(
            monitor_mouse_movement(client, config, starting_mouse_position)
        )

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
        
        if msg == "help" or msg == "?":
            from commands.help_command import execute_help_command
            await execute_help_command(client, message, config)

    async def start_bot():
        while True:
            try:
                # Start the network monitoring task
                network_task = asyncio.create_task(network_monitor())
                
                # Start the client
                await client.start(TOKEN)
            except ClientConnectorError:
                print("Failed to connect to Discord. Retrying in 30 seconds...")
                await asyncio.sleep(30)
            except KeyboardInterrupt:
                print("Interrupt received. Shutting down gracefully...")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print("Restarting the bot in 30 seconds...")
                await asyncio.sleep(30)

    try:
        await start_bot()
    finally:
        # Cancel all running tasks
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        
        # Wait for all tasks to complete
        await asyncio.gather(*tasks, return_exceptions=True)
        
        # Close the client connection
        await client.close()
        
        print("Bot has been shut down.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")