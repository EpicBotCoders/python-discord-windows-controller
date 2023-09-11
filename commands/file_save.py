async def execute_file_save(client, message, config):
    LOG_CHANNEL_ID = config["log_channel_id"]

    split_v1 = str(message.attachments).split("filename='")[1]
    filename = str(split_v1).split("' ")[0]
    await message.guild.get_channel(LOG_CHANNEL_ID).send(f"File Detected: {filename}")
    try:
        await message.attachments[0].save(
            fp="files/{}".format(filename)
        )  # saves the file
        await message.guild.get_channel(LOG_CHANNEL_ID).send("File Sucessfully saved")
        print(f"[file_save_LOG] - File Sucessfully saved.")
    except Exception as e:
        await message.guild.get_channel(LOG_CHANNEL_ID).send(f"Error while saving: {e}")
        print(f"[file_save_LOG] - Error while saving: {e}")
