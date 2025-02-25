from telegram.ext import Application, CommandHandler
import asyncio

from fetch_exam_date import fetch_data
from date import is_less_than_x_days


# Sends a message to Telegram
async def send_telegram_message(message, bot, CHAT_ID):
    await bot.send_message(chat_id=CHAT_ID, text=message)

# Fetches the exam date and sends a message if conditions are met
async def get_exam_date(bot, CHAT_ID, LOGIN, PASSWORD):
    term_text = fetch_data(LOGIN, PASSWORD)

    # Practical exam
    if is_less_than_x_days(term_text[0][-5:], 25):
        await send_telegram_message(f"DATA EGZAMINU PRAKTYCZNEGO: {term_text[0]}", bot, CHAT_ID)
        print("Message sent")
    else:
        print("Message not sent, the exam date is too far away")

    # Theoretical exam
    if is_less_than_x_days(term_text[1][-5:], 7):
        await send_telegram_message(f"DATA EGZAMINU TEORYTYCZNEGO: {term_text[1]}", bot, CHAT_ID)
        print("Message sent")
    else:
        print("Message not sent, the exam date is too far away")

# Periodic task execution
async def periodic_task(bot, CHAT_ID, LOGIN, PASSWORD):
    while True:
        await get_exam_date(bot, CHAT_ID, LOGIN, PASSWORD)
        await asyncio.sleep(600)  # Runs every 15 minutes

# Bot start command
async def start(update, context):
    await update.message.reply_text("The bot is now active and ready to go!😎")

# Command to check exam date manually
async def check_exam(update, context):
    bot = context.bot
    await get_exam_date(bot)

# Main function to start the bot
def main():
    config = {}

    with open("config.txt", "r", encoding="utf-8") as file:
        for line in file:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                config[key.strip()] = value.strip().strip("'")

    TELEGRAM_TOKEN = config.get("TELEGRAM_TOKEN")
    CHAT_ID = config.get("CHAT_ID")
    LOGIN = config.get("LOGIN")
    PASSWORD = config.get("PASSWORD")

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check_exam", check_exam))

    bot = application.bot
    loop = asyncio.get_event_loop()

    loop.create_task(periodic_task(bot, CHAT_ID, LOGIN, PASSWORD))
    loop.run_until_complete(application.run_polling())

if __name__ == '__main__':
    main()