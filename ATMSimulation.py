# -*- coding: utf-8 -*-
"""
Name: Ezriel Ciriaco
      Zachary Dulac
"""

import math
import redis
r = redis.Redis(host = "redis-18248.c15.us-east-1-2.ec2.cloud.redislabs.com", port = "18248", password = "P4eSETx01bA5elBJEDWkfvUmngXhZrbY")

def print_menu():
    print("""\n
    *****************
    *   ATM  Menu   *
    *****************
    *  1) Deposit   *
    *  2) Withdraw  *
    *  3) Transfer  *
    *  4) Exit      *
    *****************
    """)

def deposit(account_id):
    global r
    
    choice = str(input("\nAccount Type (C/S): "))
    while choice not in ['C','c','S','s']:
        choice = str(input("\nInvalid input! Account Type (C/S): "))
        
    while True:
        try:
            to_deposit = float(input("\nAmount to deposit: "))
            to_deposit *= 100
            math.trunc(to_deposit)
            to_deposit /= 100
            break
        except ValueError:
            print("Invalid input! Try again...")
            
    if choice == 'C' or choice == 'c':
        newBal = float(r.hget(account_id, "CheckingBalance")) + to_deposit
        r.hset(account_id, "CheckingBalance", newBal)
    elif choice == 'S' or choice == 's':
        newBal = float(r.hget(account_id, "SavingsBalance")) + to_deposit
        r.hset(account_id, "SavingsBalance", newBal)
        
    print("\nChecking Account Balance: $" + str(float(r.hget(account_id, "CheckingBalance"))))
    print("Savings Account Balance: $" + str(float(r.hget(account_id, "SavingsBalance"))))
    
    input_choice(account_id)

def withdraw(account_id):
    global r
    
    choice = str(input("\nAccount Type (C/S): "))
    while choice not in ['C','c','S','s']:
        choice = str(input("\nInvalid input! Account Type (C/S): "))
        
    while True:
        try:
            to_withdraw = float(input("\nAmount to withdraw: "))
            to_withdraw *= 100
            math.trunc(to_withdraw)
            to_withdraw /= 100
            break
        except ValueError:
            print("Invalid input! Try again...")
            
    if choice == 'C' or choice == 'c':
        if float(r.hget(account_id, "CheckingBalance")) >= to_withdraw:
            newBal = float(r.hget(account_id, "CheckingBalance")) - to_withdraw
            r.hset(account_id, "CheckingBalance", newBal)
        else:
            print("Insufficient Funds!")
    elif choice == 'S' or choice == 's':
        if float(r.hget(account_id, "SavingsBalance")) >= to_withdraw:
            newBal = float(r.hget(account_id, "SavingsBalance")) - to_withdraw
            r.hset(account_id, "SavingsBalance", newBal)
        else:
            print("Insufficient Funds!")
            
    print("\nChecking Account Balance: $" + str(float(r.hget(account_id, "CheckingBalance"))))
    print("Savings Account Balance: $" + str(float(r.hget(account_id, "SavingsBalance"))))
    
    input_choice(account_id)

def transfer(account_id):
    global r

    choice = str(input("\nAccount Type (C/S): "))
    while choice not in ['C','c','S','s']:
        choice = str(input("\nInvalid input! Account Type (C/S): "))

    while True:
        try:
            to_transfer = float(input("\nAmount to transfer: "))
            to_transfer *= 100
            math.trunc(to_transfer)
            to_transfer /= 100
            break
        except ValueError:
            print("Invalid input! Try again...")

    if choice == 'C' or choice == 'c':
        if float(r.hget(account_id, "CheckingBalance")) >= to_transfer:
            newBal = float(r.hget(account_id, "CheckingBalance")) - to_transfer
            r.hset(account_id, "CheckingBalance", newBal)
            newBal = float(r.hget(account_id, "SavingsBalance")) + to_transfer
            r.hset(account_id, "SavingsBalance", newBal)
        else:
            print("Insufficient Funds!")
    elif choice == 'S' or choice == 's':
        if float(r.hget(account_id, "SavingsBalance")) >= to_transfer:
            newBal = float(r.hget(account_id, "SavingsBalance")) - to_transfer
            r.hset(account_id, "SavingsBalance", newBal)
            newBal = float(r.hget(account_id, "CheckingBalance")) + to_transfer
            r.hset(account_id, "CheckingBalance", newBal)
        else:
            print("Insufficient Funds!")

    print("\nChecking Account Balance: $" + str(float(r.hget(account_id, "CheckingBalance"))))
    print("Savings Account Balance: $" + str(float(r.hget(account_id, "SavingsBalance"))))

    input_choice(account_id)

def exit_ATM():
    print("\nHave a nice day!")
    return 1

def input_choice(account_id):
    
    while True:
        try:
            option = int(input("\nPick a number corresponding to the desired option: "))
            break
        except ValueError:
            print("Invalid input! Try again...")

    if option == 1:
        deposit(account_id)
    elif option == 2:
        withdraw(account_id)
    elif option == 3:
        transfer(account_id)
    elif option == 4:
        exit_ATM()
    else:
        print("\nInvalid input!")
        input_choice(account_id)

if __name__ == "__main__":
    #money_check = 1000
    #money_save = 500
    
    flag = False
    while flag == False:
        try:
            account_id = int(input("Please input your Account Number: "))
            pin = int(r.hget(account_id, "PIN"))
            if(pin == None):
                print("Invalid Account Number!")
                continue
            pinput = int(input("Please input your PIN: "))
            
            if(pinput == pin):
                flag = True
                
            print(flag)
            
        except ValueError:
            print("Values must be of integer type!")
            
    print("\nChecking Account Balance: $" + str(float(r.hget(account_id, "CheckingBalance"))))
    print("Savings Account Balance: $" + str(float(r.hget(account_id, "SavingsBalance"))))
    print_menu()
    input_choice(account_id)
