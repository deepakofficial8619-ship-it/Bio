import os
import telebot

# Secrets se le raha hai (Railway mein daalenge)
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(BOT_TOKEN)
pending_questions = {}

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == ADMIN_ID:
        bot.reply_to(message, "✅ Admin mode ON\nAb questions aane par reply karke jawab dena.")
    else:
        bot.reply_to(message, "📩 Message bhejo, admin ko anonymously pahunch jayega!")

@bot.message_handler(func=lambda msg: True)
def handle_all(message):
    user_id = message.from_user.id
    
    if user_id == ADMIN_ID:
        if message.reply_to_message and message.reply_to_message.message_id in pending_questions:
            target = pending_questions[message.reply_to_message.message_id]
            try:
                bot.send_message(target, message.text)
                bot.reply_to(message, f"✅ Reply bhej diya!")
                del pending_questions[message.reply_to_message.message_id]
            except:
                bot.reply_to(message, "❌ User ne bot block kiya.")
        else:
            bot.reply_to(message, "👆 Kisi question ko reply karke jawab do.")
    else:
        try:
            sent = bot.send_message(ADMIN_ID, f"🔔 New from {user_id}:\n\n{message.text}")
            pending_questions[sent.message_id] = user_id
            bot.reply_to(message, "✅ Message admin tak pahunch gaya!")
        except:
            bot.reply_to(message, "⚠️ Thodi der baad try karo.")

print("🤖 Bot shuru ho gaya... 24/7 chalega!")
bot.infinity_polling()
