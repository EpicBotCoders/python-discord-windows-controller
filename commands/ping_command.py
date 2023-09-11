import time


async def execute_ping_command(client, message, config):
    LOG_CHANNEL_ID = config["log_channel_id"]

    ping_message = await message.channel.send("Pong !")
    await message.delete()
    time.sleep(5)
    await ping_message.delete()
