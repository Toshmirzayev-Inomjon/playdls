# menus.py
from telebot import types
from config import MEDIA_PATH, ITEMS

def main_menu(user_id=None):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🌐 Ijtimoiy tarmoqlar", "🛍 Donat Servis", "Tanga🪙-olmos💎 yigʻdirish")
    keyboard.add("🏟 Stadion", "⚡ Dream Club", "🎟 Sitikerlar")
    keyboard.row("Telegram 📱", "🤖 Bot yaratuvchisi")
    return keyboard




from telebot import types

def main_social_inline():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Instagram 📸", url="https://www.instagram.com/inomjon.lvl/"))
    kb.add(types.InlineKeyboardButton("YouTube ▶️", url="https://youtube.com/@dls_yangiliklari-n5o"))
    return kb


def telegram_inline_menu():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Kanal 📢", url="https://t.me/DLS25KANAL"))
    kb.add(types.InlineKeyboardButton("Guruh 💬", url="https://t.me/DLS_RASMIY_GRUPPASI"))
    kb.add(types.InlineKeyboardButton("Akkountlar 🔑", url="https://t.me/dlsakkountlar"))
    return kb



# Donat bo'limlari uchun ichki inline menyular (variantlar)
def _generate_item_menu(prefix):
    kb = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for key, val in ITEMS.items():
        if key.startswith(prefix):
            buttons.append(types.InlineKeyboardButton(val[0], callback_data=f"item|{key}"))
    if buttons:
        kb.add(*buttons)
    kb.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main"))
    return kb

def coins_menu():
    return _generate_item_menu("coins_")

def gems_menu():
    return _generate_item_menu("gems_")

def season_menu():
    return _generate_item_menu("season_")

def stadium_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("🏟 Stadionni yaxshilash", callback_data="item|stadium_upgrade"))
    kb.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main"))
    return kb

def club_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("⚡ Dream Club sotib olish", callback_data="item|club_info"))
    kb.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main"))
    return kb

def sticker_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("🎟 Stiker sotib olish", callback_data="item|sticker_buy"))
    kb.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main"))
    return kb

def send_photo(bot, chat_id, filename, caption, inline_kb=None):
    path = f"{MEDIA_PATH}{filename}"
    try:
        with open(path, "rb") as ph:
            bot.send_photo(chat_id, ph, caption=caption, reply_markup=inline_kb, parse_mode="Markdown")
    except FileNotFoundError:
        bot.send_message(chat_id, f"Rasm topilmadi: {filename}\n{caption}", reply_markup=inline_kb)
