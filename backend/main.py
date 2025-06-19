import logging
import random
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import *
from models import User

TOKEN = os.getenv("BOT_TOKEN")  # Or paste your bot token directly for now

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

users = {}

def get_user(user_id, username):
    if user_id not in users:
        users[user_id] = User(user_id, username)
    return users[user_id]

def pick_weighted_prize():
    return random.choices(REAL_PRIZES, weights=PRIZE_WEIGHTS, k=1)[0]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id, update.effective_user.username)
    keyboard = [["🎮 Play Demo Mode"], ["💰 Switch to Real Mode"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        f"🎉 Welcome {user.username or 'Player'}! Use /spin to play.\n"
        f"Demo balance: {user.demo_balance} coins\n"
        f"Use /refill to reset demo.\n"
        f"Use /deposit for real mode. Spin cost: {SPIN_COST} USDT.",
        reply_markup=reply_markup
    )

async def spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id, update.effective_user.username)

    if not user.can_spin(SPIN_COST):
        await update.message.reply_text("❌ Not enough balance.")
        return

    # Deduct spin cost
    user.adjust_balance(-SPIN_COST)

    # RTP logic
    won = random.random() < RTP
    prize = pick_weighted_prize() if won else 0

    if won:
        user.adjust_balance(prize)
        user.streak += 1
        msg = f"🎉 You WON {prize} coins!"
        if user.streak % STREAK_TRIGGER == 0:
            user.adjust_balance(STREAK_BONUS)
            msg += f"\n🔥 Streak bonus: +{STREAK_BONUS}!"
    else:
        user.streak = 0
        msg = "😢 You lost this spin."

    msg += f"\n💰 Balance: {user.get_current_balance()}"
    await update.message.reply_text(msg)

    # Fake win broadcast
    if random.random() < 0.25:
        fake_name = random.choice(FAKE_NAMES)
        fake_amount = random.choice(FAKE_WIN_AMOUNTS)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"📢 {fake_name} just won {fake_amount} coins! 🔥"
        )

async def refill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id, update.effective_user.username)
    if user.is_demo:
        user.reset_demo()
        await update.message.reply_text("✅ Demo balance refilled to 1000.")
    else:
        await update.message.reply_text("❌ You are in real mode. Deposit real crypto to play.")

async def set_demo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id, update.effective_user.username)
    user.is_demo = True
    await update.message.reply_text("🎮 Switched to Demo Mode.")

async def set_real(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id, update.effective_user.username)
    user.is_demo = False
    await update.message.reply_text(f"💰 Switched to Real Mode.\nPlease deposit minimum {MIN_DEPOSIT} USDT to play.")

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id, update.effective_user.username)
    await update.message.reply_text(
        f"🔗 Share your referral link:\n"
        f"https://t.me/{context.bot.username}?start={user.id}"
    )

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top = sorted(users.values(), key=lambda u: u.get_current_balance(), reverse=True)[:5]
    msg = "🏆 Leaderboard (Top 5):\n"
    for i, u in enumerate(top, 1):
        name = u.username or f"User{u.id}"
        msg += f"{i}. {name} — {u.get_current_balance():.2f} coins\n"
    await update.message.reply_text(msg)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spin", spin))
    app.add_handler(CommandHandler("refill", refill))
    app.add_handler(CommandHandler("referral", referral))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("demo", set_demo))
    app.add_handler(CommandHandler("real", set_real))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
