import asyncio

from telegram.ext import Application, CommandHandler

from date import is_less_than_x_days
from fetch_exam_date import fetch_data


# Sends a message to Telegram
async def send_telegram_message(message, bot, CHAT_ID):
    await bot.send_message(chat_id=CHAT_ID, text=message)


# Fetches the exam date and sends a message if conditions are met
async def get_exam_date(bot, CHAT_ID, LOGIN, PASSWORD, THEORETICAL_OR_PRACTICE, THEORETICAL_EXAM_ALERT_THRESHOLD, PRACTICAL_EXAM_ALERT_THRESHOLD, word_info, AUTO_BOOKING, user_info, CHROME_DRIVER_PATH):
    term_text = fetch_data(LOGIN=LOGIN, PASSWORD=PASSWORD, THEORETICAL_OR_PRACTICE=THEORETICAL_OR_PRACTICE, is_booking=AUTO_BOOKING,
                           PRACTICAL_EXAM_ALERT_THRESHOLD=PRACTICAL_EXAM_ALERT_THRESHOLD, THEORETICAL_EXAM_ALERT_THRESHOLD=THEORETICAL_EXAM_ALERT_THRESHOLD, word_info=word_info,
                           user_info=user_info,
                           CHROME_DRIVER_PATH=CHROME_DRIVER_PATH)

    if term_text is not None:
        # Practical exam
        if THEORETICAL_OR_PRACTICE == "p":
            if is_less_than_x_days(term_text[0][-5:], PRACTICAL_EXAM_ALERT_THRESHOLD):
                await send_telegram_message(
                    f"DATA EGZAMINU PRAKTYCZNEGO: {term_text[0]}\nGODZINY: {', '.join(term_text[1])}",
                    bot, CHAT_ID)
                print("Message sent")

        # Theoretical exam
        elif THEORETICAL_OR_PRACTICE == "t":
            if is_less_than_x_days(term_text[0][-5:], THEORETICAL_EXAM_ALERT_THRESHOLD):
                await send_telegram_message(f"DATA EGZAMINU TEORYTYCZNEGO: {term_text[0]}\nGODZINY: {', '.join(term_text[1])}",
                    bot, CHAT_ID)
                print("Message sent")
            else:
                print("Message not sent, the exam date is too far away")


# Periodic task execution
async def periodic_task(bot, CHAT_ID, LOGIN, PASSWORD, THEORETICAL_OR_PRACTICE, THEORETICAL_EXAM_ALERT_THRESHOLD, PRACTICAL_EXAM_ALERT_THRESHOLD, word_info, AUTO_BOOKING, user_info, CHROME_DRIVER_PATH):
    while True:
        await get_exam_date(bot=bot, CHAT_ID=CHAT_ID, LOGIN=LOGIN, PASSWORD=PASSWORD, THEORETICAL_OR_PRACTICE=THEORETICAL_OR_PRACTICE,
                           THEORETICAL_EXAM_ALERT_THRESHOLD=THEORETICAL_EXAM_ALERT_THRESHOLD, PRACTICAL_EXAM_ALERT_THRESHOLD=PRACTICAL_EXAM_ALERT_THRESHOLD,
                           word_info=word_info, AUTO_BOOKING=AUTO_BOOKING, user_info=user_info, CHROME_DRIVER_PATH=CHROME_DRIVER_PATH)


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

    CHROME_DRIVER_PATH = config.get("CHROME_DRIVER_PATH")
    TELEGRAM_TOKEN = config.get("TELEGRAM_TOKEN")
    CHAT_ID = config.get("CHAT_ID")
    LOGIN = config.get("LOGIN")
    PASSWORD = config.get("PASSWORD")

    THEORETICAL_OR_PRACTICE = config.get("THEORETICAL_OR_PRACTICE").lower()
    AUTO_BOOKING = True if config.get("AUTO_BOOKING") == 'True' else False
    THEORETICAL_EXAM_ALERT_THRESHOLD = int(config.get("THEORETICAL_EXAM_ALERT_THRESHOLD"))
    PRACTICAL_EXAM_ALERT_THRESHOLD = int(config.get("PRACTICAL_EXAM_ALERT_THRESHOLD"))

    FIRST_NAME = config.get("FIRST_NAME")
    LAST_NAME = config.get("LAST_NAME")
    PESEL = config.get("PESEL")
    PKK = config.get("PKK")
    CATEGORY = config.get("CATEGORY").lower()
    EMAIL = config.get("EMAIL")
    PHONE_NUMBER = config.get("PHONE_NUMBER")

    PROVINCE = config.get("PROVINCE")
    WORD = config.get("WORD")

    user_info = {
        "first_name": FIRST_NAME,
        "last_name": LAST_NAME,
        "pesel": PESEL,
        "pkk": PKK,
        "category": CATEGORY,
        "email": EMAIL,
        "phone_number": PHONE_NUMBER,
    }

    word_info = {
        "province": PROVINCE,
        "word": WORD,
        "category": CATEGORY,
    }

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check_exam", check_exam))

    bot = application.bot
    loop = asyncio.get_event_loop()

    loop.create_task(periodic_task(bot=bot, CHAT_ID=CHAT_ID, LOGIN=LOGIN, PASSWORD=PASSWORD, THEORETICAL_OR_PRACTICE=THEORETICAL_OR_PRACTICE,
                                   THEORETICAL_EXAM_ALERT_THRESHOLD=THEORETICAL_EXAM_ALERT_THRESHOLD, PRACTICAL_EXAM_ALERT_THRESHOLD=PRACTICAL_EXAM_ALERT_THRESHOLD,
                                   word_info=word_info, AUTO_BOOKING=AUTO_BOOKING, user_info=user_info, CHROME_DRIVER_PATH=CHROME_DRIVER_PATH))
    loop.run_until_complete(application.run_polling())


if __name__ == '__main__':
    main()
