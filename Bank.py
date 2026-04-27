from abc import ABC , abstractmethod


class Account(ABC): 
    def __init__(self  , owner , balance):
        self.owner = owner 
        self.__balance = balance 
        
    def get_balance(self ):
        return self.__balance 

    def _set_balance(self, new_balance):               #### imp
        self.__balance = new_balance
    
    
    def deposit(self , amount):
        if amount <= 0:
            print("amount should be greater than 0")
            return False
        self.__balance += amount
        return True
    
    def withdraw(self , amount):
        if amount <= 0:
            print("amount should be greater than 0")
            return False
        if amount <= self.__balance:
            self.__balance -= amount
            return True
        print("balance is low")
        return False
            
    def __str__(self ):
        return f"{self.owner} has avilable balance is {self.__balance}"
    
    @abstractmethod
    def get_account_type(self ):
        pass 
    
    
    
    
class savings_type(Account):
    def __init__(self, owner, balance):
        super().__init__(owner, balance)
        
    def get_account_type(self ):
        return f"{self.owner} have saving tpye bank account"
    
class current_typr(Account):
    def get_account_type(self):
        return f"{self.owner} have current account type" 
    
    def __init__(self, owner, balance ) :
        super().__init__(owner, balance)
        self.overdraft = 5000
        
    def withdraw(self, amount):
        if amount <= 0:
            print("amount should be greater than 0")
            return False

        balance = self.get_balance()
        if amount <= balance:
            return super().withdraw(amount)

        extra_needed = amount - balance
        if extra_needed <= self.overdraft:
            self.overdraft -= extra_needed
            self._set_balance(0)
            return True

        print("overdraft limit reached")
        return False
        
        
    
def main():
    accounts = []

    def find_account(name):
        for acc in accounts:
            if acc.owner == name:
                return acc
        return None

    while True:
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. View All Accounts")
        print("6. Exit")
     
     
        try:
            choice = int(input("choice between 1 to 6 "))
        except ValueError:
            print("Invalid choice")
            continue

        if choice == 1 :
            name = input("Enter name: ")
            balance = int(input("Enter initial balance: "))
            acc_type = input("Type (1: Saving, 2: Current): ")
            if acc_type == "2":
                acc = current_typr(name, balance)
            else:
                acc = savings_type(name, balance)
            
          
            accounts.append(acc)
            print("account created")   
        
        elif choice == 2 :
            name = input("namee")
            acc = find_account(name)
            if acc is None:
                print("account not found")
                continue

            amount = int(input("enter ammount"))
            if acc.deposit(amount):
                print("deposit successful")
                    
        elif choice == 3 :
            name = input("namee")
            acc = find_account(name)
            if acc is None:
                print("account not found")
                continue

            amount = int(input("enter ammount"))
            if acc.withdraw(amount):
                print("withdraw successful")
                    
        elif choice == 4 :
            name = input ("name")
            acc = find_account(name)
            if acc is None:
                print("account not found")
                continue

            print("avilable " , acc.get_balance())
                    
        elif choice == 5:
            for acc in accounts:
                print(acc, "| Type:", acc.get_account_type())

  
        elif choice == 6:
            print("Exiting...")
            break

        else:
            print("Invalid choice")
    
if __name__ == "__main__":
    main()