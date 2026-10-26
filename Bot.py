import asyncio
import logging
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = "Token Here"

VIDEO_PATH = "welcome_video.mp4"

VIDEO_CAPTION = (
    "سلام! خوش آمدید.\n"
    "این ویدیو موقت است و پس از ۱ دقیقه به‌صورت خودکار پاک خواهد شد."
)


async def delete_message_after_delay(
    bot, chat_id: int, message_id: int, delay_seconds: int = 60
):
    """تاخیر به مدت مشخص و سپس پاک کردن پیام"""
    await asyncio.sleep(delay_seconds)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        logging.info(f"پیام {message_id} با موفقیت حذف شد.")
    except TelegramError as e:
        logging.warning(f"خطا در پاک کردن پیام: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    try:
        # ارسال ویدیو به همراه متن توضیحات
        with open(VIDEO_PATH, "rb") as video_file:
            sent_message = await context.bot.send_video(
                chat_id=chat_id,
                video=video_file,
                caption=VIDEO_CAPTION,
                parse_mode="Markdown", 
            )

        asyncio.create_task(
            delete_message_after_delay(
                bot=context.bot,
                chat_id=chat_id,
                message_id=sent_message.message_id,
                delay_seconds=60,
            )
        )

    except FileNotFoundError:
        await context.bot.send_message(
            chat_id=chat_id,
            text="خطا: فایل ویدیو در مسیر مشخص‌شده پیدا نشد.",
        )
    except TelegramError as e:
        logging.error(f"خطا در ارسال ویدیو: {e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("ربات در حال اجرا است...")
    app.run_polling()


if __name__ == "__main__":
    main()