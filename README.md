# Telegram Crypto SpinBot

🎰 Telegram gambling-style spin bot with streaks, RTP control, leaderboards, and referrals.

## Features
- `/start` – Register user and show balance
- `/spin` – Spin the wheel with RTP 70%
- `/referral` – Share your invite link
- `/leaderboard` – Show top 5 players
- Fake win broadcasts, streak bonus (+25 every 3 wins)

## How to Deploy on Render
1. Fork this repo to your GitHub
2. Go to [https://render.com](https://render.com)
3. Click **New Web Service** → Connect your GitHub → Select this repo
4. Set **Bot Token**:
   - Go to **Environment Variables** in Render dashboard
   - Add key: `TOKEN` and value: `your_bot_token`
5. Hit **Deploy**

Your bot will now run 24/7 for free (under Render's free plan).
