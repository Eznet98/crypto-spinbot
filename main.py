import logging
import random
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

TOKEN = "8198937260:AAFC0sN8QWDLXmFoA6IzXIke90PTBWZ1cXw"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

users = {}
fake_names = ["CryptoKing", "WheelWarrior", "BitBandit", "SpinQueen", "LuckyETH"]
fake_prizes = [200, 500, 1000, 300, 750]
RTP = 0.7

def get_or_create_user(user_id):
    if user_id not in users:
        users[user_id] = {"balance": 1000, "streak": 0, "referrals": 0, "name": f"User{user_id}"}
    return users[user_id]

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

WEBAPP_URL = "https://crypto-spinbot.netlify.app/"  # ✅ Your Netlify spinwheel link

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_or_create_user(update.effective_user.id)

    welcome_msg = (
        f"🎉 Welcome {update.effective_user.first_name}! "
        f"Your balance: {user['balance']} coins.\n\n"
        f"Use /spin to play text version.\n"
        f"Or tap below to launch the 🎰 visual casino:"
    )

    # Web App button that opens your Mini App inside Telegram
    button = KeyboardButton(
        text="🎰 Launch Casino",
        web_app={"url": WEBAPP_URL}
    )

    reply_markup = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True
    )

    await update.message.reply_text(welcome_msg, reply_markup=reply_markup)

async def spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_or_create_user(user_id)

    if user["balance"] < 100:
        await update.message.reply_text("❌ Not enough balance. You need at least 100 coins.")
        return

    user["balance"] -= 100
    win_chance = RTP
    won = random.random() < win_chance
    prize = random.choice([100, 200, 300, 400, 500]) if won else 0

    if won:
        user["balance"] += prize
        user["streak"] += 1
        msg = f"✅ You WON {prize} coins!"
        if user["streak"] % 3 == 0:
            user["balance"] += 25
            msg += f"\n🔥 Streak bonus! +25 coins"
    else:
        user["streak"] = 0
        msg = "😢 You lost this spin."

    msg += f"\n💰 Balance: {user['balance']}"

    await update.message.reply_text(msg)

    # Occasionally send fake broadcast
    if random.random() < 0.3:
        fake_name = random.choice(fake_names)
        fake_amount = random.choice(fake_prizes)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"📢 {fake_name} just won {fake_amount} coins! 🔥"
        )

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_or_create_user(update.effective_user.id)
    await update.message.reply_text(f"🔗 Your referral link: t.me/{context.bot.username}?start={update.effective_user.id}")

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sorted_users = sorted(users.items(), key=lambda x: x[1]["balance"], reverse=True)
    top = sorted_users[:5]
    msg = "🏆 Top 5 Players:\n"
    for i, (uid, u) in enumerate(top, 1):
        msg += f"{i}. {u['name']} - {u['balance']} coins\n"
    await update.message.reply_text(msg)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spin", spin))
    app.add_handler(CommandHandler("referral", referral))
    app.add_handler(CommandHandler("leaderboard", leaderboard))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
