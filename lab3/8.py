class Account:
    owner = "someone"

    def deposit(self, balance):
        self.balance = int(balance)

    def withdraw(self, amount):
        self.amount = int(amount)
        if self.amount > self.balance:
            return "Insufficient Funds"
        else:
            return self.balance - self.amount
        
o = Account()
b, a = [x for x in input().split()]
o.deposit(b)
print(o.withdraw(a))