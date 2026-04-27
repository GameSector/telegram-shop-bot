import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

catalog = {
    "Клавиатуры": [
        {"name": "Офисная клавиатура", "price": "500 грн", "desc": "Тиха, механическая"},
        {"name": "RGB клавиатура", "price": "1500 грн", "desc": "RGB, механическая"}
    ],
    "Мышки": [
        {"name": "Игровая мышь", "price": "800 грн", "desc": "Подсветка"},
        {"name": "Беспроводная мышь", "price": "600 грн", "desc": "Без проводов"}
    ]
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
        for product in catalog[text]:
            msg = f"📦 {product['name']}\n💰 {product['price']}\n📝 {product['desc']}"
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
