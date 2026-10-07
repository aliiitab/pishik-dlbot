import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.environ["BOT_TOKEN"]


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message or not message.video:
        return

    await message.reply_text("⏳ ویدئو دریافت شد، در حال آماده‌سازی...")

    try:
        video = await message.video.get_file()

        filename = f"/tmp/{message.video.file_unique_id}.mp4"

        await video.download_to_drive(filename)

        await message.reply_text(
            "✅ فایل دریافت شد.\n\n"
            "این نسخه فعلاً فایل را روی سرور موقت ذخیره می‌کند."
        )

        os.remove(filename)

    except Exception as e:
        await message.reply_text(f"❌ خطا:\n{e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "ویدئوت رو بفرست تا دریافتش کنم."
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.COMMAND & filters.Regex("^/start$"), start))
app.add_handler(MessageHandler(filters.VIDEO, handle_video))

print("Bot is running...")
app.run_polling()
