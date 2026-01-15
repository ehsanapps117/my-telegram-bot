import telebot
from telebot import types

# اطلاعات اصلی
TOKEN = '7958281455:AAFx0z-e-CZvudnknHLnQJeMfsqa9tFmjHg'
bot = telebot.TeleBot(TOKEN)
CREATOR_ID = "@Ehsan_hack_1"

# لیست کانال‌ها برای قفل اجباری
CHANNELS = ["@ehsanappsgroup117", "@ehsanapps117", "@ehsanhack117"]

def is_subscribed(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status == 'left':
                return False
        except Exception:
            continue 
    return True

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    
    if not is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📢 کانال اول", url="https://t.me/ehsanapps117"),
            types.InlineKeyboardButton("📢 کانال دوم", url="https://t.me/ehsanhack117"),
            types.InlineKeyboardButton("👥 گروه پشتیبانی", url="https://t.me/ehsanappsgroup117"),
            types.InlineKeyboardButton("✅ بررسی عضویت", callback_data="check_join")
        )

        bot.send_message(
            message.chat.id,
            "<b>🚫 دسترسی مسدود است!</b>\n\n"
            "لطفاً برای فعال‌سازی ربات ابتدا در منابع زیر عضو شوید:\n"
            "──────────────────",
            parse_mode='HTML',
            reply_markup=markup
        )
        return

    # استخراج اطلاعات برای قالب زیبا
    user = message.from_user
    name = user.first_name
    last = user.last_name if user.last_name else "---"
    uname = f"@{user.username}" if user.username else "بدون یوزرنیم"

    # قالب‌بندی متناسب با سایز چت تلگرام
    info_layout = (
        f"<b>┌─── ⋆『 USER DETAILS 』⋆ ───┐</b>\n\n"
        f"<b>👤 ɴᴀᴍᴇ:</b> <code>{name}</code>\n"
        f"<b>🆔 ғᴀᴍɪʟʏ:</b> <code>{last}</code>\n"
        f"<b>💎 ᴜsᴇʀɴᴀᴍᴇ:</b> {uname}\n"
        f"<b>🔢 ᴜsᴇʀ ɪᴅ:</b> <code>{user_id}</code>\n\n"
        f"<b>🔗 ᴘʀᴏғɪʟᴇ ʟɪɴᴋ:</b>\n"
        f"┗ <a href='tg://user?id={user_id}'>Open Account</a>\n\n"
        f"<b>└─────────────────┘</b>\n"
        f"<b>📡 Powered by: {CREATOR_ID}</b>"
    )

    # ایجاد دکمه‌های شیشه‌ای پایین پیام
    main_markup = types.InlineKeyboardMarkup(row_width=2)
    btn_copy = types.InlineKeyboardButton("🆔 کپی آیدی", callback_data=f"copy_{user_id}")
    btn_support = types.InlineKeyboardButton("👨‍💻 پشتیبانی", url=f"https://t.me/Ehsan_hack_1")
    btn_channel = types.InlineKeyboardButton("📢 کانال ما", url="https://t.me/ehsanapps117")
    
    main_markup.add(btn_copy)
    main_markup.add(btn_channel, btn_support)

    bot.send_message(message.chat.id, info_layout, parse_mode='HTML', reply_markup=main_markup)

# هندلر برای دکمه‌های شیشه‌ای
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "check_join":
        if is_subscribed(call.from_user.id):
            bot.answer_callback_query(call.id, "✅ عضویت تایید شد! دوباره /start بزنید.")
            bot.delete_message(call.message.chat.id, call.message.message_id)
        else:
            bot.answer_callback_query(call.id, "❌ هنوز عضو نشدید!", show_alert=True)
            
    elif call.data.startswith("copy_"):
        uid = call.data.split("_")[1]
        bot.answer_callback_query(call.id, f"آیدی {uid} در متون بالا (کد) آماده کپی است!", show_alert=False)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "<b>💡 برای نمایش پنل کاربری دستور /start را بفرستید.</b>", parse_mode='HTML')

print("--- 🤖 Bot is Online | @Ehsan_hack_1 ---")
bot.infinity_polling()
