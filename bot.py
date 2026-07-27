from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import threading
from flask import Flask

# 1. ለRender መኝታ መከላከያ የሚሆን አነስተኛ የዌብ ሰርቨር (Flask)
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "ቦቱ በትክክል እየሰራ ነው!"

def run_flask():
    # Render በሚሰጠን ፖርት (Port) ላይ ሰርቨሩን ያስነሳል
    flask_app.run(host='0.0.0.0', port=10000)

# ፎቶ ID
HELP_PHOTO_FILE_ID = "AgACAgQAAxkBAANKame5OVlplhFhrxOas4F_fB9yoMAAAroSaxuhTDhTP1aL7KydZNcBAAMCAAN5AAM9BA"

# /start ሲባል የኪቦርድ ቁልፎችን ማሳያ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("🍞 ዳቦ ሻጭ"), KeyboardButton("🍌 ሙዝ ሻጭ")],
        [KeyboardButton("📞 ስልክ ቁጥር ለመላክ", request_contact=True), KeyboardButton("🆘 የእርዳታ ጥሪ")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        text="👋 ሰላም! እንኳን ደህና መጡ።\nከታች ያሉትን የኪቦርድ ቁልፎች በመጫን የሚፈልጉትን ማግኘት ይችላሉ፡",
        reply_markup=reply_markup
    )

# መልዕክት ሲላክ ምላሽ የሚሰጥበት
async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.photo:
        return
    if update.message.contact:
        first_name = update.message.contact.first_name
        await update.message.reply_text(f"✅ እናመሰግናለን {first_name}! ስልክ ቁጥርዎ በትክክል ደርሶናል።")
        return

    user_text = update.message.text.strip() if update.message.text else ""
    
    if user_text == "🍞 ዳቦ ሻጭ":
        await update.message.reply_text("🛒 ቀጥታ ዳቦ ሻጩን ለማግኘት @Dara10245901888 ያነጋግሩ፤ ያሉበት እናደርሳለን።")
    elif user_text == "🍌 ሙዝ ሻጭ":
        await update.message.reply_text("🏢 የሙዝ አቅራቢ ለማግኘት @Fadder_7 ያነጋግሩ።")
    elif user_text == "🆘 የእርዳታ ጥሪ":
        try:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=HELP_PHOTO_FILE_ID,
                caption="📖 ይህ የእርዳታ ጥሪ ነው። ፎቶው ላይ የምታዩት ወንድማችን መናገር አይችልም፤ ማንነታቸው ባልታወቁ ሰዎች ተደፍሮ የተጣለ ሰው ነው እባካችሁ እርዱት። ቀጥታ እሱን ለማግኘት @Fadder_7 ያነጋግሩ።"
            )
        except Exception as e:
            await update.message.reply_text("❌ ፎቶውን መላክ አልተቻለም።")
    elif user_text:
        await update.message.reply_text("🤔 ምን ፈለጉ? ወጥ ይጨመር?")

def main():
    # 🚀 የዌብ ሰርቨሩን በስተጀርባ በተናጠል ማስጀመር
    threading.Thread(target=run_flask, daemon=True).start()

    # የቴሌግራም ቦቱን ማስጀመር
    TOKEN = "8727117294:AAHrTR1TW-rKS81RIKpKvnHRJJAYJ7rTFh8"
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT | filters.CONTACT | filters.PHOTO & ~filters.COMMAND, reply_message))

    print("ቦቱ እና የዌብ ሰርቨሩ እየሰሩ ነው...")
    app.run_polling()

if __name__ == '__main__':
    main()
