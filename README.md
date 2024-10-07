# Simple Telegram Bot

<p align="center">
    <img src="image.png" alt="Phone Mockup">
</p>



This project is a Telegram bot that responds to text messages. 
Based on:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot): A library that provides a pure Python interface for the Telegram Bot API.
- [python-sagemcom-api](https://github.com/iMicknl/python-sagemcom-api): A library to interact with Sagemcom devices.


## Requirements

Before running the bot, ensure you have the following:

- Python 3.7 or higher.
- Pip (Python package manager).

## Installation

1. Clone this repository to your machine:

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository
   ```

2. Install the necessary dependencies:

    ```bash
    pip install python-telegram-bot==21.6 sagemcom-api psutil   
    ```

## Creating a Telegram Bot

1. Open Telegram and search for the user **BotFather**.
2. Start a conversation with BotFather and use the command `/newbot` to create a new bot.
3. Follow the prompts to name your bot and give it a unique username. After creation, you will receive a token that you will need to access the Telegram Bot API.
4. To enable the bot to receive messages in groups, you need to disable privacy mode. You can do this by sending the command `/setprivacy` to BotFather and selecting the bot you created. Choose the option to disable privacy mode.

## Running the Bot

1. Open the bot script (e.g., `bot.py`) and replace `YOUR_BOT_TOKEN` with the token you received from BotFather.
2. To run the bot, use the following command:

   ```bash
   python telegram_bot.py
   ```

## Adding the Bot as a Service

To run your bot as a service at system startup, you can create a systemd service file.

1. Create a new service file:

   ```bash
   sudo nano /etc/systemd/system/telegram-bot.service
   ```

2. Add the following content to the file, replacing `/path/to/your/bot.py` with the actual path to your bot script:

   ```ini
   [Unit]
   Description=Telegram Bot

   [Service]
   ExecStart=/usr/bin/python3 /path/to/your/bot.py
   WorkingDirectory=/path/to/your/dir
   Restart=always
   User=your_username

   [Install]
   WantedBy=multi-user.target
   ```

3. Save the file and exit the editor.

4. Enable and start the service:

   ```bash
   sudo systemctl enable telegram-bot.service
   sudo systemctl start telegram-bot.service
   ```

5. To check the status of your bot, you can run:

   ```bash
   sudo systemctl status telegram-bot.service
   ```
