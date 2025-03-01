from telegram.ext import Application, CommandHandler
import asyncio
import datetime

from fetch_exam_date import fetch_data
from date import is_less_than_x_days


# Sends a message to Telegram
async def send_telegram_message(message, bot, CHAT_ID):
    await bot.send_message(chat_id=CHAT_ID, text=message)


# Fetches the exam date and sends a message if conditions are met
async def get_exam_date(bot, CHAT_ID, LOGIN, PASSWORD, THEORETICAL_TERMS):
    term_text = fetch_data(LOGIN, PASSWORD, THEORETICAL_TERMS)

    # Practical exam
    if is_less_than_x_days(term_text[0][0][-5:], 25):
        await send_telegram_message(
            f"DATA EGZAMINU PRAKTYCZNEGO: {term_text[0][0]}\nGODZINY: {', '.join(term_text[0][1])}",
            bot, CHAT_ID)
        print("Message sent")
    else:
        print("Message not sent, the exam date is too far away")

    if THEORETICAL_TERMS:
        # Theoretical exam
        if is_less_than_x_days(term_text[1][0][-5:], 7):
            await send_telegram_message(f"DATA EGZAMINU TEORYTYCZNEGO: {term_text[1][0]}\nGODZINY: {', '.join(term_text[1][1])}",
                bot, CHAT_ID)
            print("Message sent")
        else:
            print("Message not sent, the exam date is too far away")


# Determine sleep interval based on the time of day
def get_sleep_interval():
    now = datetime.datetime.now().time()

    if datetime.time(7, 0) <= now < datetime.time(9, 0):  # 07:00 - 9:00 → every 6 minutes
        return 360
    elif datetime.time(9, 0) <= now < datetime.time(12, 0): # 9:00 - 12:00 → every 10 minutes
        return 600
    elif datetime.time(12, 0) <= now < datetime.time(17, 0):  # 12:00 - 17:00 → every 15 minutes
        return 900
    else:  # 17:00 - 07:00 → every 30 minutes
        return 1800


# Periodic task execution
async def periodic_task(bot, CHAT_ID, LOGIN, PASSWORD, THEORETICAL_TERMS):
    while True:
        await get_exam_date(bot, CHAT_ID, LOGIN, PASSWORD, THEORETICAL_TERMS)
        sleep_time = get_sleep_interval()
        print(f"Sleeping for {sleep_time // 60} minutes...")
        await asyncio.sleep(sleep_time)


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
    THEORETICAL_TERMS = True if config.get("THEORETICAL_TERMS") == "1" else False

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check_exam", check_exam))

    bot = application.bot
    loop = asyncio.get_event_loop()

    loop.create_task(periodic_task(bot, CHAT_ID, LOGIN, PASSWORD, THEORETICAL_TERMS))
    loop.run_until_complete(application.run_polling())


if __name__ == '__main__':
    main()
