# Creating and Running a Discord Bot - Step-by-Step Guide

This guide will walk you through the process of setting up and running a Discord bot that performs specific tasks using the repository "python-discord-windows-controller." Follow these steps to get your bot up and running!

## Step 1: Clone the Repository

First, clone the repository to your local machine. Open a terminal or command prompt and navigate to the folder where you want to store your bot's files. Then, use the following command:

```bash
git clone https://github.com/EpicBotCoders/python-discord-windows-controller.git
```

## Step 2: Set Up Your Project

Navigate to the cloned repository's folder using the `cd` command:

```bash
cd python-discord-windows-controller
```

## Step 3: Create and Activate a Virtual Environment (__Optional but Recommended__)

Set up a virtual environment to manage your project's dependencies. This step is optional but recommended:

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```bash
  source venv/bin/activate
  ```

## Step 4: Install Required Libraries

Install the necessary libraries for your bot using the following command:

```bash
pip install -r requirements.txt
```

## Step 5: Create a Discord Bot

1. Go to the Discord Developer Portal: [Discord Developer Portal](https://discord.com/developers/applications)
2. Click on "New Application" and give your bot a name.

   ![NewApplication](https://github.com/EpicBotCoders/python-discord-windows-controller/blob/main/images/1.png?raw=true)

3. Under the "Token" section, click "Reset Token" then copy your bot's token.

   ![Copy Token](https://github.com/EpicBotCoders/python-discord-windows-controller/blob/main/images/2.png?raw=true)

4. Under the "Privileged Gateway Intents," select "MESSAGE CONTENT INTENT"

   ![Copy Token](https://github.com/EpicBotCoders/python-discord-windows-controller/blob/main/images/5.png?raw=true)
    

## Step 6: Configure the keys and IDs

1. In the project folder, create a text file named "key.txt."
2. Paste the copied bot token into the "key.txt" file and save it.
3. Get your Channel ID and your own ID from discord, and paste them into the "config.json" file.

Example
```json
{
    "command_channel_id": 1137276176451079374,
    "author_id": 637917562920429309,
    "log_channel_id": 1137693326543122128
}
```


## Step 7: Test the Bot

1. Invite your bot to a Discord server:

   - In the Developer Portal, go to the "OAuth2" section.
   - Under "OAuth2 URL Generator," select the "bot" scope and the required permissions.
   - Copy the generated URL and open it in a browser. Follow the prompts to add the bot to a server.

   ![Add Bot to Server](https://github.com/EpicBotCoders/python-discord-windows-controller/blob/main/images/3.png?raw=true)
   ![Add Select Perms](https://github.com/EpicBotCoders/python-discord-windows-controller/blob/main/images/4.png?raw=true)

## Step 8: Run the Bot

1. In the terminal, navigate to the project folder and activate the virtual environment if you created one.
2. Run the bot using the following command:
   ```bash
   python bot.py
   ```
## Step 9: Test the Functionality

1. In the server where your bot is added, send a message with the content "lock" in the designated channel.
3. The bot should respond by locking the workstation and sending a confirmation message.
