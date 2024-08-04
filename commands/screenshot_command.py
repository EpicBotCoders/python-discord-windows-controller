import discord
import datetime
from PIL import ImageGrab

SCREENSHOT_PATH = "data\screenshot.png"

def get_ss():
    screenshot = ImageGrab.grab()
    screenshot.save(SCREENSHOT_PATH)
    return SCREENSHOT_PATH

async def execute_screenshot_command(message,args):
    """
    Takes a screenshot of the current screen and sends it.
    
    Usage: !ss or !screenshot
    """
    time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    MESSAGE = f"Screenshot at {time}"
    PATH = get_ss()
    ss_message = await message.channel.send(MESSAGE, file=discord.File(PATH))
    await message.delete()
    print(f"[screenshot_command_LOG] - Screenshot taken at {time}.")
    if("-p" in args):
        print("Persistent screenshot requested")
    else:
        time.sleep(5)
        await ss_message.delete()
        print("Screenshot Deleted")
