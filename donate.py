# donate.py
from telebot import types
from crm import add_order, get_order
from menus import send_photo
from config import ADMINS

# item mapping: key -> (display name, price, image file, long description)
ITEMS = {
    # Coins
    "coins_bundle": ("Bundle (Coins)", "35.000", "coins.jpg", "Bundle: qisqacha ta'rif..."),
    "coins_stack":  ("Stack (Coins)", "70.000", "coins.jpg", "Stack: qisqacha ta'rif..."),
    "coins_cup":    ("Cup (Coins)", "115.000", "coins.jpg", "Cup: qisqacha ta'rif..."),
    "coins_case":   ("Case (Coins)", "190.000", "coins.jpg", "Case: qisqacha ta'rif..."),
    "coins_locker": ("Locker (Coins)", "330.000", "coins.jpg", "Locker: qisqacha ta'rif..."),
    "coins_vault":  ("Vault (Coins)", "700.000", "coins.jpg", "Vault: qisqacha ta'rif..."),
    # Gems
    "gems_90":   ("90 Gems", "35.000", "gems.jpg", "90 Gems: qisqacha..."),
    "gems_400":  ("400 Gems", "130.000", "gems.jpg", "400 Gems: qisqacha..."),
    "gems_910":  ("910 Gems", "275.000", "gems.jpg", "910 Gems: qisqacha..."),
    "gems_2700": ("2700 Gems", "700.000", "gems.jpg", "2700 Gems: qisqacha..."),
    "gems_6000": ("6000 Gems", "1.600.000", "gems.jpg", "6000 Gems: qisqacha..."),
    # Season
    "season_sale":    ("Season Pass (Aksiya)", "25.000", "season pass.jpg", "Aksiya narxi: ..."),
    "season_normal":  ("Season Pass (Normal)", "38.000", "season pass.jpg", "Normal narxi: ..."),
    "season_premium": ("Season Pass (Premium)", "150.000", "season pass.jpg", "Premium: ..."),
    # Stadium / club / sticker
    "stadium_upgrade": ("Stadium Upgrade", "400.000", "stadium.jpg", "Stadionni yaxshilash..."),
    "club_info":       ("Dream Club", "—", "dream club.jpg", "Dream Club a'zo paketi..."),
    "sticker_buy":     ("Sticker", "50.000", "sitiker.jpg", "Stikerlar: ..."),
}

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
    oid = add_order(user.id, username, title, price, payment_method="Kontakt admin", note="Telegram orqali buyurtma")

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
