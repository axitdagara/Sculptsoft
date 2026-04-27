# class bank :
#     def __init__(self , balance):
#         self.__balance = balance 
    
#     @property
#     def balance(self):
#         return self.__balance
    
#     @balance.setter
#     def balance(self , balance):
#         self.__balance += balance
    
    
#     # def __deposit(self , Amount):
#     #     self.balance += Amount
    
#     # def depo(self , Amount):
#     #     self.__deposit(Amount)
        
    
    
#     def get_balance(self ):
#         return self.balance
    
    
    
# b = bank(1000)
# # b.__deposit(500)
# # print(b.get_balance())
# print(b.balance)
# b.balance += 250
# # b.depo(500)
# print(b.balance)










# from abc import ABC , abstractmethod


# class vehical(ABC):
#     @abstractmethod
#     def start(self):
#         print("hello")
        

# class bmw(vehical):
#      pass
#     # def start(self):
#     #     print ("engine is running right now ")
    
# b = bmw()
# b.start()
    









# class Student:
#     def __init__(self, name):
#         self.name = name
    
#     def __repr__(self):
#        return f"Student('{self.name}')"

#     def __str__(self):
#         return f"Student Name: {self.name}"
#     # def  get_info(self):
#     #     return f"studdent name : {self.name}"
    


# s = Student("Harsh")
# print(s)
# print(repr(s))



# class Group:
#     def __init__(self, students):
#         self.students = students

#     def __len__(self):
#         return len(self.students)
    
# g = Group(["A", "B", "C"])
# print(g.__len__())






from abc import ABC , abstractmethod

class account(ABC):
    def __init__(self , owener  , balance):
        self.owener = owener 
        self.__balance = balance 
    
    
    @abstractmethod
    def get_accouttype(self) :
        pass
    
    
    
    def get_balance(self) : 
        return self.__balance
        
        
    def __str__(self):
        return f"{self.owener} balance is {self.__balance}"
    
    
class saving_account(account):
    def __init__(self, owener, balance):
        super().__init__(owener, balance)
        
    def get_accouttype(self ):
        # type = "savings"

        return "savings"
    


acc= saving_account("axit" , 50000)


print(acc)  
print(acc.get_accouttype())
print(acc.get_balance())


# from abc import ABC, abstractmethod

# class Account(ABC):
#     def __init__(self, owner, balance):
#         self.owner = owner
#         self.balance = balance

#     @abstractmethod
#     def get_account_type(self):
#         pass

#     def get_balance(self):
#         return self.balance

#     def __str__(self):
#         return f"{self.owner} balance is {self.balance}"


# class SavingAccount(Account):
#     def get_account_type(self):
#         return "Saving Account"


# # This will give error now
# # acc = Account("axit", 50000)

# # Correct way
# acc = SavingAccount("axit", 50000)

# print(acc)
# print(acc.get_account_type())
# print(acc.get_balance())

