import os
import asyncio
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = os.getenv("TELEGRAM_TOKEN")

catalog = {
    "1": {
        "name": "Ajazz AK820 White",
        "desc": "Механическая клавиатура с белым корпусом",
        "price": 1450
    },
    "2": {
        "name": "Ajazz AK820 Grey-White",
        "desc": "Серо-белая версия популярной модели",
        "price": 1450
    },
    "3": {
        "name": "Ajazz NK61 Black",
        "desc": "Компактная 60% клавиатура",
        "price": 1050
    },
    "4": {
        "name": "Ajazz NK61 White",
        "desc": "Белая компактная клавиатура",
        "price": 1050
    },
    "5": {
        "name": "Freewolf M75 Grey-White",
        "desc": "Игровая клавиатура с подсветкой",
        "price": 1050
    },
    "6": {
        "name": "Attack Shark X68 HE",
        "desc": "Премиум клавиатура для гейминга",
        "price": 2290
    },
}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛍 Открыть каталог", callback_data="catalog")]
    ]
    await update.message.reply_text(
        "👋 Добро пожаловать в магазин клавиатур",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# показать каталог
async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = []
    for pid, item in catalog.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{item['name']} — {item['price']} грн",
                callback_data=f"product_{pid}"
            )
        ])

    await query.message.edit_text(
        "🛍 Каталог товаров:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# показать товар
async def show_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    pid = query.data.split("_")[1]
    item = catalog[pid]

    text = (
        f"⌨️ <b>{item['name']}</b>\n\n"
        f"📝 {item['desc']}\n\n"
        f"💰 Цена: {item['price']} грн"
    )

    keyboard = [
        [InlineKeyboardButton("🛒 Купить", callback_data=f"buy_{pid}")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="catalog")]
    ]

    await query.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# покупка
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    pid = query.data.split("_")[1]
    item = catalog[pid]

    await query.message.edit_text(
        f"✅ Ты выбрал: {item['name']}\n\n"
        f"Напиши свой ник и номер для связи 👇"
    )

# запуск
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_catalog, pattern="catalog"))
    app.add_handler(CallbackQueryHandler(show_product, pattern="product_"))
    app.add_handler(CallbackQueryHandler(buy, pattern="buy_"))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
