async def execute_ping_command(client, message, config):
    LOG_CHANNEL_ID = config["log_channel_id"]

    await message.channel.send("Pong !")
    await message.guild.get_channel(LOG_CHANNEL_ID).send("Pinged!")
