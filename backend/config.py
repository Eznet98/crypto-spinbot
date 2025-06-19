# Prize segments
VISIBLE_PRIZES = [0, 0.5, 1, 1.2, 1.5, 2, 2.5, 5, 10, 25, 50, 100]
REAL_PRIZES = [0, 0.5, 1, 1.2, 1.5, 2, 2.5, 5, 10]  # 25, 50, 100 are fake (never land)

# Weights: 90% from first group, 10% from second group
PRIZE_WEIGHTS = [
    0.30,  # 0
    0.25,  # 0.5
    0.15,  # 1
    0.10,  # 1.2
    0.10,  # 1.5
    0.035, # 2
    0.025, # 2.5
    0.007, # 5
    0.003  # 10
]

# Return to player (approximate average payout %)
RTP = 0.7

# Spin cost (minimum stake)
SPIN_COST = 5.0  # in USDT or equivalent crypto

# Minimum deposit to play
MIN_DEPOSIT = 10.0  # in USDT or equivalent

# Demo mode settings
DEMO_START_BALANCE = 1000  # Refillable demo coins

# Streak reward
STREAK_BONUS = 25
STREAK_TRIGGER = 3

# Fake win broadcast pool
FAKE_NAMES = ["CryptoKing", "SpinQueen", "BitBandit", "LuckyETH"]
FAKE_WIN_AMOUNTS = [200, 300, 500, 1000]
