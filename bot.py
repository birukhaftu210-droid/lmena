import asyncio
import threading
import os
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 1. ለRender መኝታ መከላከያ የሚሆን አነስተኛ የዌብ ሰርቨር (Flask)
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "ቦቱ በትክክል እየሰራ ነው!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host='0.0.0.0', port=port)

# 📸 የ 3ቱ ፎቶዎች File ID
PHOTO_1_ID = "AgACAgQAAxkBAAPiamnlNMH9g9fSv5Q9wLltm1sBTK8AArkOaxvW2VFTd2JSrJn2Y7QBAAMCAAN5AAM9BA"
PHOTO_2_ID = "AgACAgQAAxkBAAPgamnlIb1Qg9Cjr2gWJ79qi4JVWP0AArcOaxvW2VFTCR4SjEYvz-cBAAMCAAN5AAM9BA" 
PHOTO_3_ID = "AgACAgQAAxkBAAPhamnlJfgJZi9rs_S79UvIe6U5_6EAArgOaxvW2VFTQE3Mn8cpD0gBAAMCAAN5AAM9BA"

# /start ሲባል አዲሶቹን የኪቦርድ ቁልፎች ማሳያ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 4 ጠቃሚ ቁልፎች በ 3 ረድፍ ተደራጅተዋል
    keyboard = [
        [KeyboardButton("🆘 የእርዳታ ጥሪ")],
        [KeyboardButton("🏦 የባንክ አካውንት መረጃ"), KeyboardButton("💬 ቀጥታ አድራሻ")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        text="👋 ሰላም! እንኳን ደህና መጡ。\nከታች ያሉትን የኪቦርድ ቁልፎች በመጫን መረጃ ማግኘት ወይም እገዛ ማድረግ ይችላሉ፦",
        reply_markup=reply_markup
    )

# መልዕክት ሲላክ ምላሽ የሚሰጥበት
async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.photo:
        return

    # ተጠቃሚው "📞 ስልክ ቁጥር ያጋሩ" የሚለውን ተጭኖ ስልኩን ሲልክ
    if update.message.contact:
        first_name = update.message.contact.first_name
        phone_number = update.message.contact.phone_number
        await update.message.reply_text(
            f"✅ እናመሰግናለን {first_name}! ስልክ ቁጥርዎ ({phone_number}) በትክክል ደርሶናል። በቅርቡ እናገኝዎታለን።"
        )
        return

    user_text = update.message.text.strip() if update.message.text else ""
    
    # 1. የእርዳታ ጥሪ ቁልፍ
    if user_text == "🆘 የእርዳታ ጥሪ":
        try:
            media_group = [
                InputMediaPhoto(
                    media=PHOTO_1_ID, 
                    caption="📖 ይህ የእርዳታ ጥሪ ነው። ፎቶው ላይ የምታዩት ወንድማችን መናገር አይችልም፤ ማንነታቸው ባልታወቁ ሰዎች ተደፍሮ የተጣለ ሰው ነው እባካችሁ እርዱት የ ግራ መቀመጫው ከ አገልግሎት ውጪ ነው መጸዳዳት አይችልም በምትችሉት እርዱት አሁን ላይ ዳይፐር መግዛት አቅቶት እላዩ ላይ እየተጸዳዳ ይግኛል😭።እባካችሁ ከመሞቱ በፊት ድረሱለት"
                ),
                InputMediaPhoto(media=PHOTO_2_ID),
                InputMediaPhoto(media=PHOTO_3_ID)
            ]
            await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media_group)
        except Exception as e:
            await update.message.reply_text("❌ ፎቶዎቹን በአንድ ላይ መላክ አልተቻለም።")
            
    # 2. የባንክ አካውንት መረጃ ቁልፍ (አካውንት ቁጥሩን በራስዎ መቀየር ይችላሉ)
    elif user_text == "🏦 የባንክ አካውንት መረጃ":
        bank_info = (
            "🏦 **የገንዘብ እርዳታ ለማድረግ የባንክ አካውንቶች፦**\n\n"
            "📌 **የኢትዮጵያ ንግድ ባንክ (CBE)**\n"
            "🔹 የሂሳብ ቁጥር፦ `100012334566`\n"
            "🔹 ስም፦ አብዲ\n\n"
            "📌 **አቢሲኒያ ባንክ (BoA)**\n"
            "🔹 የሂሳብ ቁጥር፦ `1002933443`\n"
            "🔹 ስም፦ አብዲ\n\n"
            "🙏 ለምታደርጉት ትብብር ከልብ እናመሰግናለን!"
        )
        await update.message.reply_text(bank_info, parse_mode="Markdown")

    # 3. ቀጥታ አድራሻ ቁልፍ
    elif user_text == "💬 ቀጥታ አድራሻ":
        await update.message.reply_text("👤 ቀጥታ አደራሻውን ለማግኘት እና መረጃ ለመለዋወጥ 0908789012 ያነጋግሩ።")
            
    elif user_text:
        await update.message.reply_text("🤔 እባክዎ ከታች ካሉት የኪቦርድ ቁልፎች አንዱን በመጫን የሚፈልጉትን መረጃ ያግኙ።")

async def main_async():
    TOKEN = os.environ.get("BOT_TOKEN", "8727117294:AAHrTR1TW-rKS81RIKpKvnHRJJAYJ7rTFh8")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    
    combined_filter = (filters.TEXT | filters.CONTACT | filters.PHOTO) & ~filters.COMMAND
    app.add_handler(MessageHandler(combined_filter, reply_message))

    print("ቦቱ እና የዌብ ሰርቨሩ እየሰሩ ነው...")
    
    await app.initialize()
    await app.updater.start_polling()
    await app.start()
    
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        await app.stop()
        await app.updater.stop()

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main_async())
