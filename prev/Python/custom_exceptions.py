class WithdrawalError(Exception):
    """Exception raised for errors in the withdrawal process."""
    def __init__(self, balance, amount, message="Insufficient funds for withdrawal"):
        self.balance = balance
        self.amount = amount
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} -> Balance: {self.balance}, Requested: {self.amount}'

def withdraw_money(balance, amount):
    if amount > balance:
        raise WithdrawalError(balance, amount)
    return balance - amount

if __name__ == "__main__":
    try:
        current_balance = 100
        withdrawal_amount = 150
        print(f"Attempting to withdraw ${withdrawal_amount} from ${current_balance}...")
        new_balance = withdraw_money(current_balance, withdrawal_amount)
    except WithdrawalError as e:
        print(f"Transaction Failed: {e}")
