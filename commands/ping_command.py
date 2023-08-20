import time

async def execute_ping_command(client, message, config):
    LOG_CHANNEL_ID = config["log_channel_id"]

    await message.channel.send("Pong !")
    sentmsg = await message.guild.get_channel(LOG_CHANNEL_ID).send("Pinged!")
    await message.delete()
    time.sleep(5)
    await sentmsg.delete()