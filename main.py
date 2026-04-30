import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

catalog = {
    "1": {"name": "Ajazz AK820 White"},
    "2": {"name": "Ajazz AK820 Grey White"},
    "3": {"name": "AJAZZ NK61 Black"},
    "4": {"name": "AJAZZ NK61 White"},
    "5": {"name": "FREEWOLF M75 Grey-White"},
    "6": {"name": "Attack Shark X68 HE"},
}
   

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! 👋\nНапиши /catalog для просмотра товаров")

async def catalog_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[cat] for cat in catalog.keys()]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выбери категорию:", reply_markup=reply_markup)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in catalog:
        product = catalog[text]
        msg = f"📦 {product['name']}"
        await update.message.reply_text(msg)
        await update.message.reply_text("Напиши /catalog для выбора другой категории")
    else:
        await update.message.reply_text("Напиши /catalog для просмотра каталога")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("catalog", catalog_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
