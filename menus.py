# menus.py
from telebot import types
from config import MEDIA_PATH

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🌐 Ijtimoiy tarmoqlar", "🛍 Donat Servis","Tanga🪙-olmos💎 yigʻdirish")
    keyboard.add("🏟 Stadion", "⚡ Dream Club","🎟 Sitikerlar")
    keyboard.row( "🧑‍💻 admin", "🤖 Bot yaratuvchisi")
    return keyboard

def social_inline():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Telegram 📲", url="https://t.me/toshmirzay_inomjon"))
    kb.add(types.InlineKeyboardButton("Instagram 📸", url="https://www.instagram.com/inomjon.lvl/"))
    kb.add(types.InlineKeyboardButton("YouTube ▶️", url="https://youtube.com/@new_rek_kanal"))
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
