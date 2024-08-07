import time


async def execute_ping_command(client, message, config):
    """
    Responds with 'Pong!' to check if the bot is responsive.
    
    Usage: !ping
    """
    LOG_CHANNEL_ID = config["log_channel_id"]

    ping_message = await message.channel.send("Pong !")
    print(f"[ping_command_LOG] - Pinged.")
    await message.delete()
    time.sleep(5)
    await ping_message.delete()
