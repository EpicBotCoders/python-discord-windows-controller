import json
import os

async def execute_file_save(client, message, config):
    LOG_CHANNEL_ID = config["log_channel_id"]
    
    # Load the configuration file
    with open('config.json', 'r') as config_file:
        full_config = json.load(config_file)
    
    # Get the file save path from the config
    file_save_path = full_config.get("file_save_path", "")
    
    if not file_save_path:
        await message.guild.get_channel(LOG_CHANNEL_ID).send("Error: file_save_path not configured in config.json")
        print("[file_save_LOG] - Error: file_save_path not configured in config.json")
        return

    split_v1 = str(message.attachments).split("filename='")[1]
    filename = str(split_v1).split("' ")[0]
    await message.guild.get_channel(LOG_CHANNEL_ID).send(f"File Detected: {filename}")
    
    try:
        # Ensure the directory exists
        os.makedirs(file_save_path, exist_ok=True)
        
        # Construct the full file path
        full_file_path = os.path.join(file_save_path, filename)
        
        await message.attachments[0].save(fp=full_file_path)  # saves the file
        await message.guild.get_channel(LOG_CHANNEL_ID).send("File Successfully saved")
        print(f"[file_save_LOG] - File Successfully saved to {full_file_path}")
    except Exception as e:
        await message.guild.get_channel(LOG_CHANNEL_ID).send(f"Error while saving: {e}")
        print(f"[file_save_LOG] - Error while saving: {e}")