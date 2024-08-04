import os
import discord
from discord.ext import commands

async def execute_help_command(client, message, config):
    """
    Displays a list of all available commands and their descriptions.
    
    Usage: !help or !?
    """
    LOG_CHANNEL_ID = config["log_channel_id"]

    commands_dir = r"D:\Coding\python-discord-windows-controller\commands"
    command_files = [f for f in os.listdir(commands_dir) if f.endswith('.py') and f != '__init__.py']

    embed = discord.Embed(title="Bot Commands", description="Here are all available commands:", color=discord.Color.blue())

    for file in command_files:
        command_name = file[:-3]  # Remove .py extension
        module = __import__(f"commands.{command_name}", fromlist=[''])
        
        # Try to get the docstring of the execute function
        try:
            func = getattr(module, f"execute_{command_name}_command")
            description = func.__doc__ or "No description available."
        except AttributeError:
            description = "No description available."

        embed.add_field(name=f"!{command_name}", value=description, inline=False)

    await message.channel.send(embed=embed)
    print(f"[help_command_LOG] - Help command executed.")
    await message.delete()