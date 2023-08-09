import discord
import os
import subprocess
if(os.path.exists("key.txt")):
    with open("key.txt","r") as f:
        TOKEN = f.read()
else:
    TOKEN = ""


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
    elif message.channel.id != 1137776176451039374:
        print("Wrong channel")
        return
    elif message.author.bot:
        return
    elif message.author.id != 637911567920529409:
        print("Wrong author")
        return

    if msg == "lock":
        print(f"Received message from {message.author}: {message.content}")

        # Command to execute
        command = 'rundll32.exe user32.dll,LockWorkStation'
        # Execute the command
        subprocess.run(command, shell=True)
        channel = client.get_channel(1137697616101122128)
        await channel.send("Locked workstation sucessfully")
        await message.delete()

client.run(TOKEN)