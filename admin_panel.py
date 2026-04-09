from telebot import types
from crm import all_orders, get_order, update_order_status

# =======================
# Admin ReplyKeyboard (asosiy menyu)
# =======================
def admin_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(
        types.KeyboardButton("📦 Barcha buyurtmalar"),
        types.KeyboardButton("📊 Statistikalar")
    )
    kb.row(
        types.KeyboardButton("⬅️ Orqaga")
    )
    return kb

# =======================
# Inline tugmalar bilan buyurtmalar ro'yxati
# =======================
def list_orders(bot, chat_id):
    orders = all_orders()
    if not orders:
        bot.send_message(chat_id, "Hozircha buyurtma yo‘q.")
        return

    for oid, data in orders.items():
        text = (
            f"ID: `{oid}`\n"
            f"User: @{data.get('username')} ({data.get('user_id')})\n"
            f"Item: {data.get('item')}\n"
            f"Amount: {data.get('amount')}\n"
            f"Payment: {data.get('payment_method')}\n"
            f"Status: {data.get('status')}\n"
            f"Created: {data.get('created_at')}"
        )

        # Inline tugmalar
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(
            types.InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"admin_accept|{oid}"),
            types.InlineKeyboardButton("❌ Bekor qilish", callback_data=f"admin_reject|{oid}")
        )
        kb.add(types.InlineKeyboardButton("✳ Qo'shimcha ma'lumot", callback_data=f"admin_info|{oid}"))

        bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=kb)

# =======================
# Admin callbacklardan action bajarish
# =======================
def admin_update_from_callback(bot, callback_data, admin_id):
    try:
        action, oid = callback_data.split("|", 1)
    except Exception:
        return "Xato: callback format noto‘g‘ri."

    if action == "admin_accept":
        update_order_status(oid, "tasdiqlandi", admin_id)
        return f"Buyurtma {oid} tasdiqlandi."

    if action == "admin_reject":
        update_order_status(oid, "bekor qilindi", admin_id)
        return f"Buyurtma {oid} bekor qilindi."

    if action == "admin_info":
        order = get_order(oid)
        if not order:
            return "Buyurtma topilmadi."

        return (
            f"ID: `{oid}`\n"
            f"User: @{order.get('username')} ({order.get('user_id')})\n"
            f"Item: {order.get('item')}\n"
            f"Amount: {order.get('amount')}\n"
            f"Payment: {order.get('payment_method')}\n"
            f"Status: {order.get('status')}\n"
            f"Note: {order.get('note', 'Yo‘q')}"
        )

    return "Noma'lum harakat."

def get_stats():
    orders = all_orders()
    total = len(orders)
    success = len([o for o in orders.values() if o.get('status') == 'tasdiqlandi'])
    rejected = len([o for o in orders.values() if o.get('status') == 'bekor qilindi'])
    pending = len([o for o in orders.values() if o.get('status') == 'yangi'])

    stats_text = (
        "📊 *Bot statistikasi*\n\n"
        f"📦 Jami buyurtmalar: {total}\n"
        f"✅ Tasdiqlangan: {success}\n"
        f"❌ Bekor qilingan: {rejected}\n"
        f"⏳ Kutilmoqda: {pending}\n"
    )
    return stats_text

# =======================
# Oddiy Reply tugmalar orqali admin harakatlari
# =======================
def handle_admin_message(bot, message, admin_id):
    text = message.text
    chat_id = message.chat.id

    if text == "📦 Barcha buyurtmalar":
        list_orders(bot, chat_id)
    elif text == "📊 Statistikalar" or text == "🧾 Statistikalar":
        bot.send_message(chat_id, get_stats(), parse_mode="Markdown")
    elif text == "⬅️ Orqaga":
        from menus import main_menu
        bot.send_message(chat_id, "Asosiy menyuga qaytdingiz.", reply_markup=main_menu(admin_id))
    elif text == "💻 Admin panel":
        bot.send_message(chat_id, "Admin panel:", reply_markup=admin_keyboard())
    else:
        return False # main.py ga qaytarish uchun
    return True
