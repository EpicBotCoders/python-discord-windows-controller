import subprocess


async def execute_lock_command(client, message, config):
    """
    Locks the computer screen.
    
    Usage: !lock
    """
    LOG_CHANNEL_ID = config["log_channel_id"]

    command = "rundll32.exe user32.dll,LockWorkStation"
    subprocess.run(command, shell=True)
    channel = message.guild.get_channel(LOG_CHANNEL_ID)
    print(f"[lock_command_LOG] - : Lockstation Lock Command executed.")
    await channel.send("Locked workstation successfully")
    await message.delete()
