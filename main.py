import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")

catalog = {
    "Ajazz AK820 White": {"desc": "Механическая клавиатура с белым корпусом"},
    "Ajazz AK820 Grey White": {"desc": "Механическая клавиатура серо-белая"},
    "AJAZZ NK61 Black": {"desc": "Компактная механическая клавиатура черная"},
    "AJAZZ NK61 White": {"desc": "Компактная механическая клавиатура белая"},
    "FREEWOLF M75 Grey-White": {"desc": "Игровая механическая клавиатура серо-белая"},
    "Attack Shark X68 HE": {"desc": "Профессиональная игровая клавиатура"},
}
   

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! 👋\nНапиши /catalog для просмотра товаров")

async def catalog_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keys = list(catalog.keys())
    keyboard = [[keys[i], keys[i+1]] for i in range(0, len(keys), 2)]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выбери категорию:", reply_markup=reply_markup)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in catalog:
        product = catalog[text]
        msg = f"⌨️ {text}\n\n📝 {product['desc']}"
        await update.message.reply_text(msg)
        await update.message.reply_text("Напиши /catalog для выбора другого товара")
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
