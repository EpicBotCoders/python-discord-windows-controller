$venvScript = "d:/Coding/Discord bots/python-windows-bot/.venv/Scripts/Activate.ps1"
$botScript = "d:/Coding/Discord bots/python-windows-bot/bot.py"

# Activate the virtual environment
. $venvScript

# Run the bot script
python $botScript
