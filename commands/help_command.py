import os
import discord

async def execute_help_command(client, message, config):
    """
    Displays a list of all available commands and their descriptions.
    
    Usage: !help or !?
    """
    commands_dir = os.path.dirname(__file__)
    command_files = [f for f in os.listdir(commands_dir) if f.endswith('.py') and f != '__init__.py']

    embed = discord.Embed(title="🤖 Bot Commands", description="Here are all available commands:", color=discord.Color.blue())

    for file in sorted(command_files):
        command_name = file[:-3]  # Remove .py extension
        display_name = command_name.replace("_command", "")
        try:
            module = __import__(f"commands.{command_name}", fromlist=[''])
            func = getattr(module, f"execute_{command_name}_command")
            description = func.__doc__ or "No description available."
        except Exception:
            description = "No description available."

        embed.add_field(name=f"!{display_name}", value=description.strip(), inline=False)

    await message.channel.send(embed=embed)
    print(f"[help_command_LOG] - Help command executed.")
    try:
        await message.delete()
    except Exception:
        pass