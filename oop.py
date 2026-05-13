# 1. Student Class:-
# class Student:
#     def __init__(self,name,marks):
#         self.name = name
#         self.marks = marks

#     def grade(self):
#         if self.marks >= 80:
#             return "A"
#         elif self.marks >= 60:
#             return "B"
#         else:
#             return "C"  
#     def display(self):
#         print(f"Name: {self.name}")
#         print(f"Marks: {self.marks}")
#         print(f"Grade: {self.grade()}")  
# s1 = Student("Azhar", 85)
# s1.display()      


#2. BankAccount:-
# class BankAccount:
#     def __init__(self,name,balance=0):
#         self.name = name
#         self.___balance = balance
#     def deposit(self,amount):
#         self.___balance += amount
#         print("Deposited:", amount)
#     def withdraw(self,amount):
#         if amount <= self.___balance:
#             self.___balance -= amount
#             print("Withdraw:", amount)
#         else:
#             print("Insufficient balance")
#     def check_balance(self):
#         return self.___balance
# # object
# acc = BankAccount("Azhar", 10000)

# acc.deposit(5000)
# acc.withdraw(3000)

# print("Blance:", acc.check_balance())                    


#3. Inheritance Example:- 
# class Animal:
#     def speak(self):
#         print("Animal makes sound")

# class Dog(Animal):
#     def speak(self):
#         print("Dog braks")
# class Cat(Animal):
#     def speak(self):
#         print("Cat meows")

# d = Dog()
# c = Cat()

# d.speak()
# c.speak()                         



# class Student:
#     def __init__(self,name,marks):
#         self.name = name
#         self.marks = marks

#     def grade(self):
#         if self.marks >= 90:
#             return "A"
#         elif self.marks >= 70:
#             return "B"
#         elif self.marks >= 50:
#             return "C"    
#         else:
#             return "C" 

#     def percentage(self):
#         return self.marks
        
#     def display(self):
#         print(f"Name: {self.name}")
#         print(f"Marks: {self.marks}")
#         print(f"Grade: {self.grade()}") 
#         print(f"Percentage:", {self.percentage()}) 
# s1 = Student("Azhar", 88)
# s1.display()      


# class Animal:
#     def speak(self):
#         print("sound")

# class Dog(Animal):
#     def speak(self):
#         print("Brak") 

# d = Dog()
# d.speak()



# Object oriented approch
#class in oop:-
# class SharmaVishnu:
#     a = 10 # Attribute
#     def show(slef): # Method
#         print("chhole bhature")

# mp_nagar = SharmaVishnu()
# mp_nagar.show()
# print(mp_nagar.a)
# indrapuri = SharmaVishnu()
# indrapuri.show()
# print(indrapuri.a)


# class SagarGaire:
#     def show(self):
#         print("chhole bhature")

# patel_nagar = SagarGaire()
# patel_nagar.show()
# print(mp_nagar.a)        
# SharmaVishnu.show()


# you guys have to create a class as informartion and accept name and age frome user and just print the name and the age of user :-
# class Info:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#     def show(self):
#         print(f"The name is {self.name} and age is {self.age}") 

# obj = info("Azhar",21)
# obj.show()           


#Bank
# class Bank:
#     def __init__(self,amount):
#         self.balance = balance
#         print(f"The balance is {self.balance}")

#     def deposit(self,amount):
#         self.balance += amount
#         print(f"The update amount is {self.balance}")
# obj2 = Bank(5000) 
# obj2.deposit(2000)          

# class RajHans:
#     def __init__(self,name):
#         self.name = name
#     def __str__(self):
#         print(self.name) 
# obj = RajHans("BagadBilla") 
# obj.__str__() 
# obj.show()   

 
 
# class Student:
#     college = "SIRT" #CLASS ATTRIBUTE

#     @classmethod #Decorators
#     def change_college(cls,new_name):
#         cls.college = new_name
#         print(f"college is {new_name}")

# stud1 = Student()
# print(stud1.college)
# stud1.change_college("LNCT")
       


# Polymorephism:- 
# import random

# # Parent class
# class Animal:
#     def attack(self):
#         pass


# # Child classes (Polymorphism)
# class Dog(Animal):
#     def attack(self):
#         return "Dog bites 🐶"


# class Cat(Animal):
#     def attack(self):
#         return "Cat scratches 🐱"


# class Lion(Animal):
#     def attack(self):
#         return "Lion roars loudly 🦁"


# class Tiger(Animal):
#     def attack(self):  
#         return "Tiger croud" 


# class Elephant(Animal):
#     def attack(self):
#         return "Elephant flue"             


# # Game logic
# animals = [Dog(), Cat(), Lion(), Tiger(), Elephant()]

# print("🎮 Welcome to Animal Attack Game")
# print("Your Health:", health)
# print("Press Enter to continue | q to quit\n")



# while health > 0:

#     choice = input("Press Enter to fight: ")

#     if choice == "q":
#         break

#     fighter = random.choice(animals)

#     message, damage = fighter.attack()   # polymorphism

#     health -= damage
#     score += 1

#     print(message)
#     print("Damage:", damage)
#     print("Health left:", health)
#     print("Score:", score)
#     print("-" * 25)


# print("\n💀 Game Over")
# print("Final Score:", score)


# while True:
#     choice = input(">> ")

#     if choice == "q":
#         print("Game Over 👋")
#         break

#     fighter = random.choice(animals)
#     print(fighter.attack())       





import random

# -------------------
# Parent class
# -------------------
class Animal:
    def attack(self):
        pass


# -------------------
# Normal Animals
# -------------------
class Dog(Animal):
    def attack(self):
        dmg = random.randint(5, 12)
        return "Dog bites 🐶", dmg


class Cat(Animal):
    def attack(self):
        dmg = random.randint(4, 10)
        return "Cat scratches 🐱", dmg


class Lion(Animal):
    def attack(self):
        dmg = random.randint(15, 30)
        return "Lion roars & attacks 🦁", dmg


class Tiger(Animal):
    def attack(self):
        dmg = random.randint(12, 22)
        return "Tiger claws 🐯", dmg


class Elephant(Animal):
    def attack(self):
        dmg = random.randint(10, 20)
        return "Elephant stomps 🐘", dmg


# -------------------
# Boss Animal 💀
# -------------------
class Boss(Animal):
    def attack(self):
        dmg = random.randint(30, 45)
        return "🔥 BOSS SMASH ATTACK 🔥", dmg


# -------------------
# Game setup
# -------------------
animals = [Dog(), Cat(), Lion(), Tiger(), Elephant()]
boss = Boss()

health = 100
score = 0
level = 1

print("🎮 Animal Battle Game Started")


# -------------------
# Game loop
# -------------------
while health > 0:

    print(f"\n⭐ Level: {level} | ❤️ Health: {health} | 🏆 Score: {score}")

    choice = input("Press Enter to fight | h = heal | q = quit: ")

    if choice == "q":
        break

    # -------------------
    # Healing system ❤️
    # -------------------
    if choice == "h":
        heal = random.randint(10, 25)
        health += heal
        print(f"✨ You healed +{heal} health!")
        continue

    # -------------------
    # Boss every 5 levels
    # -------------------
    if level % 5 == 0:
        fighter = boss
        print("💀 BOSS FIGHT 💀")
    else:
        fighter = random.choice(animals)

    message, damage = fighter.attack()

    health -= damage
    score += 1

    print(message)
    print("Damage:", damage)

    level += 1


# -------------------
# Game Over
# -------------------
print("\n💀 Game Over")
print("Final Score:", score)
