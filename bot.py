import discord
import os
import subprocess
import json
import asyncio

if(os.path.exists("key.txt")):
    with open("key.txt","r") as f:
        TOKEN = f.read()
else:
    TOKEN = ""

    
with open("config.json", "r") as config_file:
    config = json.load(config_file)
    CMD_CHANNEL_ID = config["command_channel_id"]
    AUTHOR_ID = config["author_id"]
    LOG_CHANNEL_ID = config["log_channel_id"]

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    msg = str(message.content).lower()
    if message.author == client.user:
        return
    elif message.channel.id != CMD_CHANNEL_ID:
        print("Wrong channel")
        return
    elif message.author.bot:
        return
    elif message.author.id != AUTHOR_ID:
        print("Wrong author")
        return

    if msg == "lock":
        print(f"Received message from {message.author}: {message.content}")

        # Command to execute
        command = 'rundll32.exe user32.dll,LockWorkStation'
        # Execute the command
        subprocess.run(command, shell=True)
        channel = client.get_channel(LOG_CHANNEL_ID)
        await channel.send("Locked workstation sucessfully")
        await message.delete()
    
    if msg == "ping":
        response = await message.channel.send("Pong !")
        await client.get_channel(LOG_CHANNEL_ID).send("Pinged!")

        await asyncio.sleep(2)

client.run(TOKEN)