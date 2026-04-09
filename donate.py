# donate.py
from telebot import types
from crm import add_order, get_order
from menus import send_photo
from config import ADMINS, ITEMS

def quick_donate(bot, chat_id, item_key):
    """ Directly send info + buy button for an item """
    item = ITEMS.get(item_key)
    if not item:
        bot.send_message(chat_id, "Item topilmadi.")
        return

    title, price, image, desc = item
    caption = f"*{title}*\n\n{desc}\n\nNarx: {price}\n\nAgar buyurtma berishni istasangiz, 'Buyurtma berish' tugmasini bosing."
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🛒 Buyurtma berish", callback_data=f"order|{item_key}"))
    kb.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main"))
    send_photo(bot, chat_id, image, caption, kb)

def create_order_and_notify(bot, call, item_key):
    """ Yangi order yaratib, userga va adminlarga xabar yuboradi """
    item = ITEMS.get(item_key)
    if not item:
        bot.answer_callback_query(call.id, "Item topilmadi.")
        return

    title, price, image, desc = item
    user = call.from_user
    username = user.username or f"{user.first_name or ''} {user.last_name or ''}".strip()
    oid = add_order(user.id, title, price, username=username, payment_method="Kontakt admin", note="Telegram orqali buyurtma")

    # notify user
    bot.send_message(user.id, f"Buyurtma qabul qilindi. ID: `{oid}`\nItem: {title}\nNarx: {price}", parse_mode="Markdown")

    # notify admins
    for admin in ADMINS:
        text = (
            f"Yangi buyurtma! ID: `{oid}`\n"
            f"User: @{username} ({user.id})\n"
            f"Item: {title}\n"
            f"Narx: {price}\n"
            f"Status: kutilmoqda"
        )
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"admin_accept|{oid}"))
        kb.add(types.InlineKeyboardButton("❌ Bekor qilish", callback_data=f"admin_reject|{oid}"))
        kb.add(types.InlineKeyboardButton("✳ Qo'shimcha ma'lumot", callback_data=f"admin_info|{oid}"))
        # send to admin
        try:
            bot.send_message(admin, text, reply_markup=kb, parse_mode="Markdown")
        except Exception:
            # agar adminga xabar yuborib bo'lmasa (privacy), shunchaki o'zimizga yuboramiz
            pass

    bot.answer_callback_query(call.id, "Buyurtma yuborildi. Adminlar bilan bog'laning.")
