async def execute_ping_command(client, message):
    config = client.load_config()
    LOG_CHANNEL_ID = config["log_channel_id"]

    response = await message.channel.send("Pong !")
    await message.guild.get_channel(LOG_CHANNEL_ID).send("Pinged!")