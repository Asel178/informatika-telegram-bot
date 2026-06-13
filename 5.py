import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Сұрақтар базасы (Әріптердің регистріне сезімтал болмауы үшін жауаптарды кіші әріппен жазамыз)
QUESTIONS = {
    "квадрат теңдеу": [
        {"q": "ax²+bx+c=0 теңдеуінің дискриминанты қандай формуламен есептеледі?", "a": "d=b²-4ac"},
        {"q": "Дискриминант нольге тең болса, теңдеудің неше шешімі болады?", "a": "бір"},
        {"q": "Дискриминант нөлден кіші болса, теңдеудің неше нақты түбірі болады?", "a": "нөл"},
    ],
}

# 2. Пайдаланушы прогресін сақтау (Жауапты және тақырыпты сақтаймыз)
user_progress = {}

# 3. /start командасы
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Сәлем! Мен математикадан көмекші ботпын.\n\n"
        "Тапсырма алу үшін **/topic [тақырып аты]** командасын енгізіңіз.\n"
        "Мысалы: `/topic квадрат теңдеу`",
        parse_mode="Markdown"
    )

# 4. Тақырып таңдау және сұрақ беру
async def topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Тақырыпты жазыңыз. Мысалы: /topic квадрат теңдеу")
        return
    
    subject = " ".join(context.args).lower().strip()
    
    if subject not in QUESTIONS:
        await update.message.reply_text(f"«{subject}» тақырыбы табылмады. Қазіргі қолжетімді тақырыптар: квадрат теңдеу")
        return

    # Кездейсоқ сұрақ таңдау
    q = random.choice(QUESTIONS[subject])
    uid = update.effective_user.id
    
    # Пайдаланушының ағымдағы күйін жаңарту
    user_progress[uid] = {
        "current_answer": q["a"].lower().strip(),
        "subject": subject
    }
    
    await update.message.reply_text(f"Сұрақ:\n{q['q']}")

# 5. Пайдаланушы жауабын тексеру (Жаңадан қосылды)
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_text = update.message.text.lower().strip() # Бос орындар мен регистрді теңестіру

    # Егер пайдаланушы әлі тақырып таңдамаған болса
    if uid not in user_progress or "current_answer" not in user_progress[uid]:
        await update.message.reply_text("Алдымен сұрақ алу үшін /topic [тақырып] командасын орындаңыз.")
        return

    correct_answer = user_progress[uid]["current_answer"]

    # Жауапты салыстыру
    if user_text == correct_answer:
        await update.message.reply_text("✅ Дұрыс! Жарарайсыз! Келесі сұрақ үшін қайтадан /topic командасын жазыңыз.")
        # Сұрақ жауап берілген соң тазартылады
        del user_progress[uid]
    else:
        await update.message.reply_text("❌ Қате. Қайтадан көріңіз немесе басқа сұрақ алу үшін /topic командасын енгізіңіз.")

# Негізгі қосымшаны іске қосу
if __name__ == '__main__':
    # ТОКЕНДІ орнату
    app = ApplicationBuilder().token("8409827784:AAHC395uwJLVRZcusiSiQSU3bKXAKoAtVmQ").build()
    
    # Хэндлерлерді (командаларды) тіркеу
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("topic", topic))
    
    # Мәтіндік хабарламаларды (жауаптарды) ұстап алу үшін MessageHandler қосамыз
    # filters.TEXT & ~filters.COMMAND — бұл команда емес, жай мәтіндерді ғана тексереді
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))
    
    # Ботты іске қосу және оның үздіксіз жұмысын қамтамасыз ету
    print("Бот іске қосылды...")
    app.run_polling()
