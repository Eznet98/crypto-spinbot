class User:
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
        self.balance = 0.0             # Real crypto balance
        self.demo_balance = 1000.0     # Starting demo coins
        self.is_demo = True            # Default mode is demo
        self.streak = 0
        self.referrals = 0
        self.referred_by = None

    def reset_demo(self):
        self.demo_balance = 1000.0

    def get_current_balance(self):
        return self.demo_balance if self.is_demo else self.balance

    def adjust_balance(self, amount):
        if self.is_demo:
            self.demo_balance += amount
        else:
            self.balance += amount

    def can_spin(self, spin_cost):
        return self.get_current_balance() >= spin_cost
