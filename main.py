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
    MessageHandler,
    filters,
    ContextTypes
)

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = 8294397034

user_carts = {}

catalog = {
    "1": {"name": "Ajazz AK820 White", "desc": "Белый корпус", "price": 1450},
    "2": {"name": "Ajazz AK820 Grey-White", "desc": "Серо-белая версия", "price": 1450},
    "3": {"name": "Ajazz NK61 Black", "desc": "Компактная 60%", "price": 1050},
    "4": {"name": "Ajazz NK61 White", "desc": "Белая компактная", "price": 1050},
    "5": {"name": "Freewolf M75 Grey-White", "desc": "Игровая клавиатура", "price": 1050},
    "6": {"name": "Attack Shark X68 HE", "desc": "Премиум модель", "price": 2290},
    "7": {"name": "SmailWolf RS8 White", "desc": "Белая версия", "price": 900},
    "8": {"name": "SmailWolf RS8 Metal", "desc": "Металлический корпус", "price": 900},
    "9": {"name": "Attack Shark X8 SE", "desc": "Обновлённая модель", "price": 1250},
}

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛍 Каталог", callback_data="catalog")],
        [InlineKeyboardButton("🧺 Корзина", callback_data="cart")],
        [InlineKeyboardButton("📩 Связаться", url="https://t.me/GameSectorua")]
    ]

    await update.message.reply_text(
        "👋 Добро пожаловать в GameSector",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------- CATALOG ----------------
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

    keyboard.append([
        InlineKeyboardButton("🧺 Корзина", callback_data="cart")
    ])

    await query.message.edit_text(
        "🛍 Каталог товаров:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---------------- PRODUCT ----------------
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
        [InlineKeyboardButton("➕ В корзину", callback_data=f"add_{pid}")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="catalog")]
    ]

    # попытка отправить фото (если есть)
    try:
        photo_path = f"images/{pid}.jpg"
        if os.path.exists(photo_path):
            await query.message.delete()
            await query.message.chat.send_photo(
                photo=open(photo_path, "rb"),
                caption=text,
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await query.message.edit_text(
                text,
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    except:
        await query.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ---------------- ADD TO CART ----------------
async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    pid = query.data.split("_")[1]

    user_carts.setdefault(user_id, []).append(pid)

    await query.message.reply_text("✅ Добавлено в корзину")

# ---------------- CART ----------------
async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    cart = user_carts.get(user_id, [])

    if not cart:
        await query.message.edit_text("🧺 Корзина пуста")
        return

    text = "🧺 Твоя корзина:\n\n"
    total = 0

    for pid in cart:
        item = catalog[pid]
        text += f"• {item['name']} — {item['price']} грн\n"
        total += item['price']

    text += f"\n💰 Итого: {total} грн"

    keyboard = [
        [InlineKeyboardButton("✅ Оформить заказ", callback_data="checkout")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="catalog")]
    ]

    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# ---------------- CHECKOUT ----------------
async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["waiting_order"] = True

    await query.message.edit_text(
        "📩 Введи имя и номер телефона:"
    )

# ---------------- ORDER HANDLER ----------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_order"):
        return

    user = update.message.from_user
    user_id = user.id
    cart = user_carts.get(user_id, [])

    if not cart:
        await update.message.reply_text("Корзина пуста")
        return

    order_id = user_id % 100000

    text = f"🆕 Заказ #{order_id}\n\n"
    text += f"👤 @{user.username}\n📞 {update.message.text}\n\n"

    total = 0
    for pid in cart:
        item = catalog[pid]
        text += f"• {item['name']} — {item['price']} грн\n"
        total += item['price']

    text += f"\n💰 Итого: {total} грн"

    await context.bot.send_message(ADMIN_ID, text)

    await update.message.reply_text("✅ Заказ отправлен!")

    user_carts[user_id] = []
    context.user_data["waiting_order"] = False

# ---------------- MAIN ----------------
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(show_catalog, pattern="^catalog$"))
    app.add_handler(CallbackQueryHandler(show_product, pattern="^product_"))
    app.add_handler(CallbackQueryHandler(add_to_cart, pattern="^add_"))
    app.add_handler(CallbackQueryHandler(show_cart, pattern="^cart$"))
    app.add_handler(CallbackQueryHandler(checkout, pattern="checkout"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
