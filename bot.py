from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# የፎቶው ID በትክክል እዚህ ተቀምጧል
HELP_PHOTO_FILE_ID = "AgACAgQAAxkBAANKame5OVlplhFhrxOas4F_fB9yoMAAAroSaxuhTDhTP1aL7KydZNcBAAMCAAN5AAM9BA"

# 1. /start ሲባል የኪቦርድ ቁልፎችን ማሳያ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # የቁልፉ ስም "🆘 የእርዳታ ጥሪ" ተብሎ ይበልጥ ጎልቶ ተስተካክሏል
    keyboard = [
        [KeyboardButton("🍞 ዳቦ ሻጭ"), KeyboardButton("🍌 ሙዝ ሻጭ")],
        [KeyboardButton("📞 ስልክ ቁጥር ለመላክ", request_contact=True), KeyboardButton("🆘 የእርዳታ ጥሪ")]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        text="👋 ሰላም! እንኳን ደህና መጡ።\nከታች ያሉትን የኪቦርድ ቁልፎች በመጫን የሚፈልጉትን ማግኘት ይችላሉ፡",
        reply_markup=reply_markup
    )

# 2. ደንበኛው ኪቦርዱን ሲጫን ወይም መልዕክት ሲልክ ምላሽ የሚሰጥበት ተግባር
async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    # 📸 ሀ. አዲስ ፎቶ ሲመጣ ID ማሳያ (ይህ እንዳለ ይቆያል)
    if update.message.photo:
        photo_id = update.message.photo[-1].file_id
        print(f"\n📸 የላከው ፎቶ File ID፦\n{photo_id}\n")
        await update.message.reply_text("✅ የፎቶው ID በSublime ማሳያ ላይ ታትሟል።")
        return

    # 📞 ለ. ደንበኛው ስልክ ቁጥሩን በቁልፉ በኩል ከላከ
    if update.message.contact:
        first_name = update.message.contact.first_name
        await update.message.reply_text(f"✅ እናመሰግናለን {first_name}! ስልክ ቁጥርዎ በትክክል ደርሶናል።")
        return

    # ✍️ ሐ. ደንበኛው የላከው መደበኛ ጽሑፍ ከሆነ
    user_text = update.message.text.strip() if update.message.text else ""
    
    if user_text == "🍞 ዳቦ ሻጭ":
        await update.message.reply_text("🛒 ቀጥታ ዳቦ ሻጩን ለማግኘት @Dara10245901888 ያነጋግሩ፤ ያሉበት እናደርሳለን።")
        
    elif user_text == "🍌 ሙዝ ሻጭ":
        await update.message.reply_text("🏢 የሙዝ አቅራቢ ለማግኘት @Fadder_7 ያነጋግሩ።")
        
    # 🚀 የተስተካከለ፦ የቁልፉ ስም ከጽሑፉ ጋር ተጣጥሟል፤ ቀጥታ ፎቶውን ይልካል
    elif user_text == "🆘 የእርዳታ ጥሪ":
        try:
            # ቦቱ ፎቶውን ከነማብራሪያው መልሶ ለደንበኛው ይልካል
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=HELP_PHOTO_FILE_ID,
                caption="📖 ይህ የእርዳታ ጥሪ ነው። ፎቶው ላይ የምታዩት ወንድማችን መናገር አይችልም፤ ማንነታቸው ባልታወቁ ሰዎች ተደፍሮ የተጣለ ሰው ነው እባካችሁ እርዱት። ቀጥታ እሱን ለማግኘት @Fadder_7 ያነጋግሩ።"
            )
        except Exception as e:
            await update.message.reply_text("❌ ፎቶውን መላክ አልተቻለም። እባክህ የፎቶው ID ወይም ቦትህ ላይ ችግር አለመኖሩን አረጋግጥ።")
        
    elif user_text:
        await update.message.reply_text("🤔 ምን ፈለጉ? ወጥ ይጨመር?")

def main():
    # ቦቱን በToken ማገናኘት
    TOKEN = "8727117294:AAHrTR1TW-rKS81RIKpKvnHRJJAYJ7rTFh8"
    app = Application.builder().token(TOKEN).build()

    # ትዕዛዞችን መያዝ
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT | filters.CONTACT | filters.PHOTO & ~filters.COMMAND, reply_message))

    # ቦቱን ማንቀሳቀስ
    print("ቦቱ እየሰራ ነው...")
    app.run_polling()

if __name__ == '__main__':
    main()
