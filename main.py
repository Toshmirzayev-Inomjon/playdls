# main.py
import telebot
from telebot import types
from config import BOT_TOKEN, ADMINS
from menus import main_menu, main_social_inline,telegram_inline_menu , send_photo, coins_menu, gems_menu, season_menu, stadium_kb, club_kb, sticker_kb
from donate import quick_donate, create_order_and_notify, ITEMS
from admin_panel import admin_keyboard, list_orders, admin_update_from_callback,handle_admin_message
from crm import get_order
bot = telebot.TeleBot(BOT_TOKEN)

# /start
@bot.message_handler(commands=["start"])
def cmd_start(message):
    name = message.from_user.first_name or "User"
    bot.send_message(message.chat.id, f"Salom {name}! Mega DLS Botga xush kelibsiz 🎮", reply_markup=main_menu())

@bot.message_handler(commands=["help"])
def cmd_help(message):
    name = message.from_user.first_name or "User"
    bot.send_message(message.chat.id, f"Assalomu alaykum hurmatli {name} bot haqida tushuncha bot dls buyicha danat qiladi admin ishonchli Admin:@Bahrom777 ☑️.", reply_markup=main_menu())

# menu
@bot.message_handler(commands=["menu"])
def cmd_menu(message):
    bot.send_message(message.chat.id, "Asosiy menyu:", reply_markup=main_menu())

# Matnli menu handler
@bot.message_handler(func=lambda m: True)
def handler(message):
    text = message.text
    chat = message.chat.id

    # ORQAGA
    if text == "⬅️ Orqaga":
        bot.send_message(chat, "Asosiy menyu:", reply_markup=main_menu())
        return

    # IJTIMOIY TARMOQLAR
    if text == "🌐 Ijtimoiy tarmoqlar":
        bot.send_message(chat, "Ijtimoiy tarmoqlarimiz:", reply_markup=main_social_inline())
        return

    if text ==  "Telegram 📱":
        bot.send_message(chat, "Ijtimoiy tarmoqlarimiz:", reply_markup=telegram_inline_menu())
        return


    # DONAT SERVIS (matn orqali ichki menyu chiqaramiz)
    if text == "🛍 Donat Servis" or text == "💰 Donat bo‘limi":
        # bitta xabar ichida inline tugmalar orqali bo'limni tanlash
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(types.InlineKeyboardButton("💰 Coins", callback_data="donate_coins"))
        kb.add(types.InlineKeyboardButton("💎 Gems", callback_data="donate_gems"))
        kb.add(types.InlineKeyboardButton("💳 Season Pass", callback_data="donate_season"))
        kb.add(types.InlineKeyboardButton("🏟 Stadion", callback_data="donate_stadium"))
        kb.add(types.InlineKeyboardButton("⚡ Dream Club", callback_data="donate_club"))
        kb.add(types.InlineKeyboardButton("🎟 Sitikerlar", callback_data="donate_sticker"))
        bot.send_message(chat, "🛍 Donat bo‘limlarini tanlang:", reply_markup=kb)
        return

    # STADIUM
    if text == "🏟 Stadion":
        message_text = (
            "🏟 *Stadionlar ro'yxati*\n\n"
            "1️⃣ *CHAMPIONS ARENA* 💸\n"
            "   Narxi: 400.000 ✅\n\n"
            "2️⃣ *CENTURY PARK* 💸\n"
            "   Narxi: 300.000 ✅\n\n"
            "👨‍💻 Admin: @Bahrom777 ☑️\n"
            "📢 Qo‘shimcha ma’lumot uchun murojaat qiling."
        )
        send_photo(bot, chat, "stadium.jpg", message_text, stadium_kb())
        return

    # CLUB
    if text == "⚡ Dream Club":
        message_text = (
            "⚡ *Dream Club a’zolik paketlari*\n\n"
            "🔋 *EPIC CLUB MEMBER* – 10 kunlik\n"
            "   Narxi: 280.000 ✅\n\n"
            "🔋 *LEGENDARNY CLUB MEMBER* – 30 kunlik\n"
            "   Narxi: 380.000 ✅\n\n"
            "👨‍💻 Admin: @Bahrom777 ☑️\n"
        )
        send_photo(bot, chat, "dream club.jpg", message_text, club_kb())
        return

    # STICKER
    if text == "🎟 Sitikerlar":
        message_text = (
            "🎟 *Stikerlar ro'yxati*\n\n"
            "💰 Narxi: 50.000\n"
            "😍 Barcha stikerlar bir xil narxda\n\n"
            "👨‍💻 Admin: @Bahrom777 ✅\n"
        )
        send_photo(bot, chat, "sitiker.jpg", message_text, sticker_kb())
        return
    if text == "Tanga🪙-olmos💎 yigʻdirish":
        message_text = (
            "tanga olmoz yig'dirish yangitdan yulga quydim hozirda eng kam narxdagi shu"
            "murojat uchun: @Bahrom777 ☑️"
        )
        send_photo(bot, chat, "Tanga.jpg", message_text)
        return
    # DLS MA'LUMOT
    if text == "🤖 Bot yaratuvchisi":
        bot.send_message(chat, "https://t.me/toshmirzayevinomjon")
        return
    # admin
    if text == "🧑‍💻 admin":
        bot.send_message(chat, "Admin:@Bahrom777")
        bot.send_message(chat, "Admin ni asabi yomon boʻlganligi uchun ortiqcha yozish maslahat berilmaydi📵\n"
                               "Ayniqsa👇👇\n"
                               "Shaxsiy maʼlumotlar soʻramang❌\n"
                               "Alo alo deb koʻp yozmang❌\n"
                               "Tekin akk bering demang❌\n"
                               "Admin oling demang❌\n"
                               "Akkimni sotib oling demang❌\n"
                               "Koʻp savollar bermang va savollaringizgizga bot orqali javobni olishga harakat qiling❗️\n"
                               "Bot:🤖 @PLAYDLSNEWBOT 🤖"
                         )
        return

    # ADMIN PANEL (faqat adminlarga)
    if chat in ADMINS:
        if text == "Admin panel":
            bot.send_message(chat, "Admin menyu:", reply_markup=admin_keyboard())
            return
        if text == "📦 Barcha buyurtmalar":
            list_orders(bot, chat)
            return

    # Default
    bot.send_message(chat, "Noto‘g‘ri buyruq yoki menyudan tanlang.", reply_markup=main_menu())

# Callback handler (inline tugmalar)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data
    chat = call.message.chat.id

    # Asosiyga qaytish
    if data == "back_main":
        bot.send_message(chat, "Asosiy menyu:", reply_markup=main_menu())
        bot.answer_callback_query(call.id)
        return

    # Donat bo'limlari
    if data == "donate_coins":
        # coins section: send banner + coins menu
        caption = (
            "💰 *Coins Buyurtma*\n\n"
            "• Bundle : 35.000 ✅\n"
            "• Stack  : 70.000 ✅\n"
            "• Cup    : 115.000 ✅\n"
            "• Case   : 190.000 ✅\n"
            "• Locker : 330.000 ✅\n"
            "• Vault  : 700.000 ✅\n\n"
            "👨‍💻 Admin: @Bahrom777 ☑️"
        )
        send_photo(bot, chat, "coins.jpg", caption, coins_menu())
        bot.answer_callback_query(call.id)
        return

    if data == "donate_gems":
        caption = (
            "💎 *Gems Buyurtma*\n\n"
            "💎 90 = 35.000 ✅\n"
            "💎 400 = 130.000 ✅\n"
            "💎 910 = 275.000 ✅\n"
            "💎 2.700 = 700.000 ✅\n"
            "💎 6.000 = 1.600.000 ✅\n\n"
            "👨‍💻 Admin: @Bahrom777 ☑️"
        )
        send_photo(bot, chat, "gems.jpg", caption, gems_menu())
        bot.answer_callback_query(call.id)
        return

    if data == "donate_season":
        caption = (
            "💳 *Season Pass*\n\n"
            "• Aksiya kelgani: 25 000 so‘m 💵\n"
            "• Aksiya kelmagani: 38 000 so‘m 💵\n"
            "• Premium pass: 150 000 so‘m 💵\n\n"
            "👨‍💻 Admin: @Bahrom777 ☑️"
        )
        send_photo(bot, chat, "season pass.jpg", caption, season_menu())
        bot.answer_callback_query(call.id)
        return

    if data == "donate_stadium":
        caption = ("🏟 *Stadionlar ro'yxati*\n\n"
                   "1️⃣ *CHAMPIONS ARENA* 💸\n"
                   "   Narxi: 400.000 ✅\n\n"
                   "2️⃣ *CENTURY PARK* 💸\n"
                   "   Narxi: 300.000 ✅\n\n"
                   "👨‍💻 Admin: @Bahrom777 ☑️\n"
                   "📢 Qo‘shimcha ma’lumot uchun murojaat qiling.")
        send_photo(bot, chat, "stadium.jpg", caption, stadium_kb())
        bot.answer_callback_query(call.id)
        return

    if data == "donate_club":
        caption = "⚡ *Dream Club a’zolik paketlari*\n\n"\
                  "🔋 *EPIC CLUB MEMBER* – 10 kunlik\n"\
            "   Narxi: 280.000 ✅\n\n"\
            "🔋 *LEGENDARNY CLUB MEMBER* – 30 kunlik\n"\
            "   Narxi: 380.000 ✅\n\n"\
            "👨‍💻 Admin: @Bahrom777 ☑️\n"
        send_photo(bot, chat, "dream club.jpg", caption, club_kb())
        bot.answer_callback_query(call.id)
        return

    if data == "donate_sticker":
        caption = "🎟 *Stikerlar ro'yxati*\n\n"\
                  "💰 Narxi: 50.000\n"\
                  "😍 Barcha stikerlar bir xil narxda\n\n"\
                  "👨‍💻 Admin: @Bahrom777 ✅\n"
        send_photo(bot, chat, "sitiker.jpg", caption, sticker_kb())
        bot.answer_callback_query(call.id)
        return

    # Item buyurtma tugmalari (format: item|<key>)
    if data.startswith("item|"):
        _, key = data.split("|", 1)
        # show item detail + buy button
        item = ITEMS.get(key)
        if not item:
            bot.answer_callback_query(call.id, "Item topilmadi.")
            return
        title, price, image, desc = item
        caption = f"*{title}*\n\n{desc}\n\nNarx: {price}"
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🛒 Buyurtma berish", callback_data=f"order|{key}"))
        kb.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main"))
        send_photo(bot, chat, image, caption, kb)
        bot.answer_callback_query(call.id)
        return

    # Order yaratish: order|<item_key>
    if data.startswith("order|"):
        _, item_key = data.split("|", 1)
        create_order_and_notify(bot, call, item_key)
        return

    # Admin callback prefiksi
    if data.startswith("admin_"):
        res = admin_update_from_callback(bot, data, call.from_user.id)
        if res:
            # send result to admin who clicked
            bot.send_message(call.from_user.id, res)
        bot.answer_callback_query(call.id)
        return

    bot.answer_callback_query(call.id, "Noma'lum tugma.")
    return

if __name__ == "__main__":
    print("Bot ishga tushdi")
    bot.infinity_polling(skip_pending=True)


