# Set the working directory
$workingDir = "D:\Coding\Discord bots\python-windows-bot"
Set-Location $workingDir

# Define paths
$venvScript = Join-Path $workingDir ".venv\Scripts\Activate.ps1"
$botScript = Join-Path $workingDir "bot.py"

# Activate the virtual environment
if (Test-Path $venvScript) {
    & $venvScript
} else {
    Write-Error "Virtual environment activation script not found at $venvScript"
    exit 1
}

# Check if config.json exists
$configPath = Join-Path $workingDir "config.json"
if (-not (Test-Path $configPath)) {
    Write-Error "config.json not found in $workingDir"
    exit 1
}

# Run the bot script
if (Test-Path $botScript) {
    python $botScript
} else {
    Write-Error "Bot script not found at $botScript"
    exit 1
}