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
# ማሳሰቢያ፡ 2ኛውን እና 3ኛውን ፎቶ ለቦቱ በመላክ የምታገኘውን ረጅም ID እዚህ ቦታ ላይ ተካው!
PHOTO_1_ID = "AgACAgQAAxkBAANKame5OVlplhFhrxOas4F_fB9yoMAAAroSaxuhTDhTP1aL7KydZNcBAAMCAAN5AAM9BA"
PHOTO_2_ID = "የሁለተኛው_ፎቶ_ID_እዚህ_ይግባ" 
PHOTO_3_ID = "የሦስተኛው_ፎቶ_ID_እዚህ_ይግባ"

# /start ሲባል የኪቦርድ ቁልፎችን ማሳያ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("🍞 ዳቦ ሻጭ"), KeyboardButton("🍌 ሙዝ ሻጭ")],
        [KeyboardButton("🆘 የእርዳታ ጥሪ")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        text="👋 ሰላም! እንኳን ደህና መጡ。\nከታች ያሉትን የኪቦርድ ቁልፎች በመጫን የሚፈልጉትን ማግኘት ይችላሉ፡",
        reply_markup=reply_markup
    )

# መልዕክት ሲላክ ምላሽ የሚሰጥበት
async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 📸 አዲስ ፎቶ ወደ ቦቱ ሲላክ የፎቶውን File ID መልሶ ይነግረናል (ID ለማውጣት ይጠቅማል)
    if update.message.photo:
        photo_file_id = update.message.photo[-1].file_id
        await update.message.reply_text(f"📸 የላኩት ፎቶ File ID ይህ ነው፦\n\n`{photo_file_id}`", parse_mode="Markdown")
        return

    # ስልክ ቁጥር ሲላክ
    if update.message.contact:
        first_name = update.message.contact.first_name
        await update.message.reply_text(f"✅ እናመሰግናለን {first_name}! ስልክ ቁጥርዎ በትክክል ደርሶናል።")
        return

    user_text = update.message.text.strip() if update.message.text else ""
    
    # የዳቦ ሻጭ ቁልፍ
    if user_text == "🍞 ዳቦ ሻጭ":
        await update.message.reply_text("🛒 ቀጥታ ዳቦ ሻጩን ለማግኘት @Dara10245901888 ያነጋግሩ፤ ያሉበት እናደርሳለን።")
    
    # የሙዝ ሻጭ ቁልፍ
    elif user_text == "🍌 ሙዝ ሻጭ":
        await update.message.reply_text("🏢 የሙዝ አቅራቢ ለማግኘት @Fadder_7 ያነጋግሩ。")
        
    # የእርዳታ ጥሪ ቁልፍ (3ቱንም ፎቶዎች በአንድ ላይ በአልበም ይልካል)
    elif user_text == "🆘 የእርዳታ ጥሪ":
        try:
            media_group = [
                InputMediaPhoto(
                    media=PHOTO_1_ID, 
                    caption="📖 ይህ የእርዳታ ጥሪ ነው። ፎቶው ላይ የምታዩት ወንድማችን መናገር አይችልም፤ ማንነታቸው ባልታወቁ ሰዎች ተደፍሮ የተጣለ ሰው ነው እባካችሁ እርዱት። ቀጥታ እሱን ለማግኘት @Fadder_7 ያነጋግሩ。"
                ),
                InputMediaPhoto(media=PHOTO_2_ID),
                InputMediaPhoto(media=PHOTO_3_ID)
            ]
            
            await context.bot.send_media_group(
                chat_id=update.effective_chat.id,
                media=media_group
            )
        except Exception as e:
            await update.message.reply_text("❌ ፎቶዎቹን በአንድ ላይ መላክ አልተቻለም። (እባክህ የፎቶዎቹን File ID በትክክል መተካትህን አረጋግጥ)")
            
    elif user_text:
        await update.message.reply_text("🤔 ምን ፈለጉ? ወጥ ይጨመር?")

async def main_async():
    # ቶከኑን ከ Render Environment Variable ያነባል፣ ከሌለ ደግሞ ከታች ያለውን ይጠቀማል
    TOKEN = os.environ.get("BOT_TOKEN", "8727117294:AAHrTR1TW-rKS81RIKpKvnHRJJAYJ7rTFh8")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    
    # ማጣሪያው በቅንፍ ተስተካክሏል
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
    # Flask ሰርቨሩን በስተጀርባ ማስጀመር
    threading.Thread(target=run_flask, daemon=True).start()

    # Asyncio loop ማስተካከያ
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main_async())
