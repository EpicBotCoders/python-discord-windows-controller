import discord
import os
import json
import socket
import asyncio

def is_connected():
    try:
        # Try to resolve a common domain to check if network is available
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def load_config():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        return config

async def main():
    while True:
        if is_connected():
            break
        print("Waiting for network...")
        await asyncio.sleep(5)  # Wait for 5 seconds before checking again

    if os.path.exists("key.txt"):
        with open("key.txt", "r") as f:
            TOKEN = f.read()
    else:
        TOKEN = ""

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")

    @client.event
    async def on_message(message):
        msg = str(message.content).lower()
        config = load_config()

        if message.author == client.user or message.channel.id != config["command_channel_id"]:
            return

        if message.author.bot or message.author.id != config["author_id"]:
            return

        if str(message.attachments) != "[]":
            print(message.attachments)
            from commands.file_save import execute_file_save
            await execute_file_save(client,message,config)

        if msg == "lock":
            from commands.lock_command import execute_lock_command
            await execute_lock_command(client, message, config)

        if msg == "ping":
            from commands.ping_command import execute_ping_command
            await execute_ping_command(client, message, config)

    await client.start(TOKEN)

asyncio.run(main())