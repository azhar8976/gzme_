#. BankAaccount:-
class BankAccount:
    def __init__(self,name,balance=0):
        self.name = name
        self.___balance = balance
    def deposit(self,amount):
        self.___balance += amount
        print("Deposited:", amount)
    def withdraw(self,amount):
        if amount <= self.___balance:
            self.___balance -= amount
            print("Withdraw:", amount)
        else:
            print("Insufficient balance")
    def check_balance(self):
        return self.___balance
# object
acc = BankAccount("Azhar", 10000)

acc.deposit(5000)
acc.withdraw(3000)

print("Blance:", acc.check_balance())                    
