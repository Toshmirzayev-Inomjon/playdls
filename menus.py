# menus.py
from telebot import types
from config import MEDIA_PATH

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🌐 Ijtimoiy tarmoqlar", "🛍 Donat Servis","Tanga🪙-olmos💎 yigʻdirish")
    keyboard.add("🏟 Stadion", "⚡ Dream Club","🎟 Sitikerlar")
    keyboard.row( "Telegram 📱","🧑‍💻 admin", "🤖 Bot yaratuvchisi")
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
def coins_menu():
    kb = types.InlineKeyboardMarkup(row_width=1)
    return kb

def gems_menu():
    kb = types.InlineKeyboardMarkup(row_width=1)
    return kb

def season_menu():
    kb = types.InlineKeyboardMarkup(row_width=1)
    return kb

def stadium_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    return kb

def club_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    return kb

def sticker_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    return kb

def tanga_kp():
    kb = types.InlineKeyboardMarkup(row_width=1)
    return kb

def send_photo(bot, chat_id, filename, caption, inline_kb=None):
    path = f"{MEDIA_PATH}{filename}"
    try:
        with open(path, "rb") as ph:
            bot.send_photo(chat_id, ph, caption=caption, reply_markup=inline_kb, parse_mode="Markdown")
    except FileNotFoundError:
        bot.send_message(chat_id, f"Rasm topilmadi: {filename}\n{caption}", reply_markup=inline_kb)
