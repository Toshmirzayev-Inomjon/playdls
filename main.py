# main.py
import telebot
from telebot import types
from config import BOT_TOKEN, REQUIRED_CHANNELS
from menus import main_menu, main_social_inline,telegram_inline_menu , send_photo, coins_menu, gems_menu, season_menu, stadium_kb, club_kb, sticker_kb
from donate import quick_donate, create_order_and_notify, ITEMS
from crm import get_order
bot = telebot.TeleBot(BOT_TOKEN)

# Function to check if user is subscribed to all required channels
def check_subscription(user_id):
    if not REQUIRED_CHANNELS:
        return True  # No channels required
    
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception as e:
            # If bot cannot check (e.g., not admin), allow access
            print(f"Warning: Cannot check subscription for {channel}: {e}")
            continue
    return True

# Function to send subscription prompt if user is not subscribed
def prompt_subscription_if_needed(user_id, chat_id):
    if check_subscription(user_id):
        return False  # User is subscribed
    
    # User is not subscribed, show subscription prompt
    markup = types.InlineKeyboardMarkup()
    for channel in REQUIRED_CHANNELS:
        # Handle both usernames and IDs
        if isinstance(channel, str) and channel.startswith('@'):
            channel_link = channel.replace('@', '')
            markup.add(types.InlineKeyboardButton("Obuna bo'lish: kanal", url=f"https://t.me/{channel_link}"))
        elif isinstance(channel, str):
            markup.add(types.InlineKeyboardButton("Obuna bo'lish: kanal", url=f"https://t.me/{channel}"))
    markup.add(types.InlineKeyboardButton("✅ Tekshirish", callback_data="check_subs"))
    
    bot.send_message(
        chat_id,
        "📢 *Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:*\n\n" +
        "Obunalar bizning eng yangi yangiliklarni bilib olishingiz uchun muhim! 🔔",
        reply_markup=markup,
        parse_mode="Markdown"
    )
    return True  # User was not subscribed (subscription prompt shown)

# /start
@bot.message_handler(commands=["start"])
def cmd_start(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        # User is not subscribed to required channels
        markup = types.InlineKeyboardMarkup()
        for channel in REQUIRED_CHANNELS:
            # Handle both usernames and IDs
            if isinstance(channel, str) and channel.startswith('@'):
                channel_link = channel.replace('@', '')
                markup.add(types.InlineKeyboardButton("Obuna bo'lish: kanal", url=f"https://t.me/{channel_link}"))
            elif isinstance(channel, str):
                markup.add(types.InlineKeyboardButton("Obuna bo'lish: kanal", url=f"https://t.me/{channel}"))
        markup.add(types.InlineKeyboardButton("✅ Tekshirish", callback_data="check_subs"))
        
        bot.send_message(
            message.chat.id,
            "📢 *Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:*\n\n" +
            "Obunalar bizning eng yangi yangiliklarni bilib olishingiz uchun muhim! 🔔",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return
    
    name = message.from_user.first_name or "User"
    welcome_text = f"""🎮 *Salom {name}!*

Mega DLS Botga xush kelibsiz! 🎉

Bu yerda siz DLS uchun eng yaxshi narxlardagi:
💰 Coins
💎 Gems  
💳 Season Pass
🏟 Stadionlar
⚡ Dream Club
🎟 Stikerlar

va ko'p qo'shimchalarni topishingiz mumkin!
    """
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(message.from_user.id), parse_mode="Markdown")

@bot.message_handler(commands=["help"])
def cmd_help(message):
    name = message.from_user.first_name or "User"
    help_text = f"""❓ *Yordam bo'limi*

Assalomu alaykum hurmatli {name}! 👋

*Bot nima qiladi?*
🎮 DLS uchun eng yaxshi narxlardagi barcha tovarlarni taqdim etamiz
💳 Tez va ishonchli xizmat
👨‍💻 Maluk admin: @Bahrom777 ☑️

*Qo'shimcha savollar uchun:*
👉 Adminni yozing yoki /menu buyrug'idan foydalaning
    """
    bot.send_message(message.chat.id, help_text, reply_markup=main_menu(message.from_user.id), parse_mode="Markdown")

# menu
@bot.message_handler(commands=["menu"])
def cmd_menu(message):
    bot.send_message(message.chat.id, "Asosiy menyu:", reply_markup=main_menu(message.from_user.id))

# Matnli menu handler
@bot.message_handler(func=lambda m: True)
def handler(message):
    text = message.text
    chat = message.chat.id
    user_id = message.from_user.id
    
    # Check subscription first, before doing anything
    if prompt_subscription_if_needed(user_id, chat):
        return

    # ORQAGA
    if text == "⬅️ Orqaga":
        bot.send_message(chat, "Asosiy menyu:", reply_markup=main_menu(message.from_user.id))
        return

    # IJTIMOIY TARMOQLAR
    if text == "🌐 Ijtimoiy tarmoqlar":
        social_text = """*🌍 Ijtimoiy tarmoqlarimizga azolik qo'ling:*

Bizni kuzatib turing va eng yangi yangiliklarni bilib oling! 📱
        """
        bot.send_message(chat, social_text, reply_markup=main_social_inline(), parse_mode="Markdown")
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
            "tanga olmoz yig'dirish yangitdan yulga quydim hozirda eng kam narxdagi shu\n"
            "murojat uchun: @Bahrom777 ☑️"
        )
        send_photo(bot, chat, "Tanga.jpg", message_text)
        return
    # DLS MA'LUMOT
    if text == "🤖 Bot yaratuvchisi":
        bot.send_message(chat, "https://t.me/toshmirzayevinomjon")
        return

    # Default
    bot.send_message(chat, "Noto‘g‘ri buyruq yoki menyudan tanlang.", reply_markup=main_menu(message.from_user.id))

# Subscription check callback
@bot.callback_query_handler(func=lambda call: call.data == "check_subs")
def check_subscription_callback(call):
    user_id = call.from_user.id
    if check_subscription(user_id):
        bot.answer_callback_query(call.id, "✅ Obuna tasdiqlendiy!")
        bot.send_message(call.message.chat.id, "Endi botdan foydalanishingiz mumkin!", reply_markup=main_menu(user_id))
    else:
        bot.answer_callback_query(call.id, "❌ Hali ham obuna bo'lmagansiz!", show_alert=True)

# Callback handler (inline tugmalar)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data
    chat = call.message.chat.id
    user_id = call.from_user.id
    
    # Check subscription first (skip for check_subs callback since that's for confirming subscription)
    if data != "check_subs" and prompt_subscription_if_needed(user_id, chat):
        bot.answer_callback_query(call.id)
        return

    # Asosiyga qaytish
    if data == "back_main":
        bot.send_message(chat, "Asosiy menyu:", reply_markup=main_menu(call.from_user.id))
        bot.answer_callback_query(call.id)
        return

    # Donat bo'limlari
    if data == "donate_coins":
        # coins section: send banner + coins menu
        caption = (
            "💰 *Coins Buyurtma*\n\n"
            "📦 *Paketlar:*\n\n"
            "🟡 Bundle: 35.000 so'm ✅\n"
            "🟠 Stack: 70.000 so'm ✅\n"
            "🔴 Cup: 115.000 so'm ✅\n"
            "⭐ Case: 190.000 so'm ✅\n"
            "💎 Locker: 330.000 so'm ✅\n"
            "👑 Vault: 700.000 so'm ✅\n\n"
            "👨‍💻 Admin: @Bahrom777 ☑️\n"
            "💬 Savollaringiz bo'lsa, adminni yozing"
        )
        send_photo(bot, chat, "coins.jpg", caption, coins_menu())
        bot.answer_callback_query(call.id)
        return

    if data == "donate_gems":
        caption = (
            "💎 *Gems Buyurtma*\n\n"
            "� *Paketlar:*\n\n"
            "💎 90 Gems = 35.000 so'm ✅\n"
            "💎 400 Gems = 130.000 so'm ✅\n"
            "💎 910 Gems = 275.000 so'm ✅\n"
            "💎 2.700 Gems = 700.000 so'm ✅\n"
            "👑 6.000 Gems = 1.600.000 so'm ✅\n\n"
            "👨‍💻 Admin: @Bahrom777 ☑️"
        )
        send_photo(bot, chat, "gems.jpg", caption, gems_menu())
        bot.answer_callback_query(call.id)
        return

    if data == "donate_season":
        caption = (
            "💳 *Season Pass Buyurtma*\n\n"
            "🎁 *Variantlar:*\n\n"
            "✨ Aksiya bilan Pass: 25.000 so'm 💵 (chegirma!!)\n"
            "🔥 Odiy Pass: 38.000 so'm 💵\n"
            "👑 Premium Pass: 150.000 so'm 💵 (eng yaxshi)\n\n"
            "👨‍💻 Admin: @Bahrom777 ☑️"
        )
        send_photo(bot, chat, "season pass.jpg", caption, season_menu())
        bot.answer_callback_query(call.id)
        return

    if data == "donate_stadium":
        caption = (
            "🏟 *Stadionlar Katalogi*\n\n"
            "⚽ *Mavjud Variantlar:*\n\n"
            "1️⃣ *CHAMPIONS ARENA* 🏆\n"
            "   Narxi: 400.000 so'm ✅\n"
            "   Eng malluq stadion!\n\n"
            "2️⃣ *CENTURY PARK* 🌟\n"
            "   Narxi: 300.000 so'm ✅\n\n"
            "💬 Batafsil ma'lumot: @Bahrom777 ☑️\n"
            "📢 Bugun buyurtma qilsangiz, bonuslar bor!"
        )
        send_photo(bot, chat, "stadium.jpg", caption, stadium_kb())
        bot.answer_callback_query(call.id)
        return

    if data == "donate_club":
        caption = (
            "⚡ *Dream Club Membership*\n\n"
            "🎯 *A'zolik Paketlari:*\n\n"
            "🔋 *EPIC CLUB MEMBER* – 10 kunlik\n"
            "   Narxi: 280.000 so'm ✅\n"
            "   Standart imtiyozlar\n\n"
            "🔋 *LEGENDARY CLUB MEMBER* – 30 kunlik\n"
            "   Narxi: 380.000 so'm ✅\n"
            "   PREMIUM imtiyozlar + BONUSLAR!\n\n"
            "👨‍💻 Admin: @Bahrom777 ☑️"
        )
        send_photo(bot, chat, "dream club.jpg", caption, club_kb())
        bot.answer_callback_query(call.id)
        return

    if data == "donate_sticker":
        caption = (
            "🎟 *Stikerlar Katalogi*\n\n"
            "😍 *Barcha Stikerlar:*\n\n"
            "💠 Narxi: 50.000 so'm (bir stiker)\n"
            "✨ Barcha stikerlar bir xil mahalimatda!\n\n"
            "🎨 Chap-choq dizayn va rang-barang stikerlar\n\n"
            "👨‍💻 Admin: @Bahrom777 ☑️\n"
            "🛒 Hozir buyurtma qilish mumkin!"
        )
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

    bot.answer_callback_query(call.id, "Noma'lum tugma.")
    return

if __name__ == "__main__":
    print("Bot ishga tushdi")
    bot.infinity_polling(skip_pending=True)


