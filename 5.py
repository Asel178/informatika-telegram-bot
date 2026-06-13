import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Сұрақтар базасы
QUESTIONS = {
    "квадрат теңдеу": [
        {"q": "ax²+bx+c=0 теңдеуінің дискриминанты қандай формуламен есептеледі?", "a": "d=b²-4ac"},
        {"q": "Дискриминант нольге тең болса, теңдеудің неше шешімі болады?", "a": "бір"},
    ],
}

# 2. Пайдаланушы прогресін сақтау
user_progress = {}

# 3. /start командасы
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сәлем! /topic [тақырып] командасымен тапсырма алыңыз.")

# 4. Тақырып таңдау және сұрақ беру
async def topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Тақырыпты жазыңыз: /topic квадрат теңдеу")
        return
    
    subject = " ".join(context.args).lower()
    if subject not in QUESTIONS:
        await update.message.reply_text(f"«{subject}» тақырыбы табылмады.")
        return

    q = random.choice(QUESTIONS[subject])
    uid = update.effective_user.id
    
    # Пайдаланушының ағымдағы күйін жаңарту
    user_progress[uid] = {"current_answer": q["a"]}
    await update.message.reply_text(f"Сұрақ: {q['q']}")

# Негізгі қосымшаны іске қосу (құрылымы)
if __name__ == '__main__':
    app = ApplicationBuilder().token("8409827784:AAHC395uwJLVRZcusiSiQSU3bKXAKoAtVmQ").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("topic", topic))
    # Ботты іске қосу: app.run_polling()
