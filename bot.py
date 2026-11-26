
import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN = os.getenv("BOT_TOKEN")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! 🎓\n\n"
        "I'm your Education and Quiz Bot.\n\n"
        "Use /quiz to try a sample question."
    )

# Sample educational quiz
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_poll(
        question="Which planet is known as the Red Planet?",
        options=["Earth", "Mars", "Jupiter", "Venus"],
        type="quiz",
        correct_option_id=1,
        explanation="Mars is known as the Red Planet because of its reddish appearance.",
    )

# Basic spam moderation
async def remove_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if not message:
        return

    text = message.text or message.caption or ""
    blocked_words = ["free money", "click here to earn", "crypto giveaway"]

    if any(word in text.lower() for word in blocked_words):
        try:
            await message.delete()
        except Exception:
            logging.exception("Could not delete a spam message")

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is missing. Add it in Railway Variables.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(
        MessageHandler(
            filters.TEXT | filters.CAPTION,
            remove_spam,
        )
    )

    app.run_polling()

if __name__ == "__main__":
    main()
