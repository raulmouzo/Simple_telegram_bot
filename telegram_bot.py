# This code is based on the example from the python-telegram-bot documentation:
# https://docs.python-telegram-bot.org/en/v21.6/examples.echobot.html

import logging
import subprocess   
import os
import psutil

from router import get_devices
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


# Enable logging

logging.basicConfig(

    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO

)

# set higher logging level for httpx to avoid all GET and POST requests being logged

logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)



# Define a few command handlers. These usually take the two arguments update and

# context.


async def devices_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Connecting to router...")
    devices = await get_devices()  

    if devices:
        devices_list = "\n".join(f"{device}" for device in devices)  
        message = f"Connected Devices:\n{devices_list}"
    else:
        message = "No devices found."


    await update.message.reply_text(message, parse_mode="MarkdownV2")


async def vpn_status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = subprocess.run('bash /usr/local/bin/wireguard-manager.sh --list | grep -v -E "[0-9].*\\)" | tail -n +2', 
        shell=True, capture_output=True, text=True)
    
    if result.stdout:
        message = result.stdout
    else:
        message = "Error getting status. (Service executed as root?)"
        
    await update.message.reply_text(message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "\n\nℹ️ *INFO*\n\n"
        "🖥️ *Commands:*\n\n"
        "  \\* /devices \\- _Show devices connected on the LAN_\n"
        "  \\* /vpn\\_status \\- _Check the current status of the VPN_\n"
        "  \\* /shutdown \\- _Shut down the system_\n"
        "  \\* /reboot \\- _Reboot the system_\n"
        "  \\* /system\\_usage \\- _Show current CPU, RAM, and Disk usage_\n"  # Comando añadido
        "  \\* /help \\- _Show this help message_\n\n"
    )
    await update.message.reply_text(help_text, parse_mode="MarkdownV2")

async def shutdown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global shutdown_pending
    shutdown_pending = True
    await update.message.reply_text("Are you sure you want to shut down the system? [yes/no]")

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global shutdown_pending
    user_response = update.message.text.lower()

    if shutdown_pending:
        if user_response == 'yes':
            await update.message.reply_text("Shutting down the system...")
            os.system('shutdown now') 
            shutdown_pending = False  
        elif user_response == 'no':
            await update.message.reply_text("Shutdown canceled.")
            shutdown_pending = False 

async def reboot_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    os.system('reboot') 
    await update.message.reply_text("Rebooting...")

async def get_system_usage() -> str:
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    return (
        f"🖥️ CPU Usage: {cpu_usage}%\n"
        f"🧠 RAM Usage: {ram_usage}%\n"
        f"💾 Disk Usage: {disk_usage}%"
    )

async def system_usage_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Getting information...")
    
    usage_info = await get_system_usage()
    await update.message.reply_text(usage_info)


def main() -> None:

    """Start the bot."""

    # Create the Application and pass it your bot's token.

    application = Application.builder().token("YOUR_TOKEN_HERE").build()


    # on different commands - answer in Telegram

    application.add_handler(CommandHandler("devices", devices_command))

    application.add_handler(CommandHandler("vpn_status", vpn_status_command))

    application.add_handler(CommandHandler("shutdown", shutdown_command))

    application.add_handler(CommandHandler("reboot", reboot_command))

    application.add_handler(CommandHandler("system_usage", system_usage_command))
        
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_response))

    application.add_handler(MessageHandler(filters.ALL, help_command))



    # Run the bot until the user presses Ctrl-C

    application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == "__main__":

    main()