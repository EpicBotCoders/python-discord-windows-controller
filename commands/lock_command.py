import subprocess

async def execute_lock_command(client, message):
    config = client.load_config()
    LOG_CHANNEL_ID = config["log_channel_id"]

    command = 'rundll32.exe user32.dll,LockWorkStation'
    subprocess.run(command, shell=True)
    channel = message.guild.get_channel(LOG_CHANNEL_ID)
    await channel.send("Locked workstation successfully")
    await message.delete()
