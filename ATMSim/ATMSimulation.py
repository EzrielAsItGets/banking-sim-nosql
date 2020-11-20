# -*- coding: utf-8 -*-
"""
Name: Ezriel Ciriaco
      Zachary Dulac
"""

import math
import redis
r = redis.Redis(host = "redis-18248.c15.us-east-1-2.ec2.cloud.redislabs.com", port = "18248", password = "P4eSETx01bA5elBJEDWkfvUmngXhZrbY")

# Creates account if account_id does not exist.
def createAccount(account_id, ssn, name, pin, check, save):
    if idValidate(account_id) == False:
        d = {"SSN":ssn, "Name":name, "PIN":pin, "CheckingBalance":check, "SavingsBalance":save}
        r.hset(name = account_id, mapping = d)

# Creates account if account_id does not exist.
def deleteAccount(account_id):
    if idValidate(account_id) == True:
        r.delete(account_id)
        
# Validates account_id by requesting its value from the server.
def idValidate(account_id):
    vals = r.hgetall(account_id)
    
    if vals == {}:
        return False
    else:
        return True
    
# Validates the input PIN for the given account ID.
def pinValidate(account_id, inPIN):
    pin = int(r.hget(account_id, "PIN"))
    
    if inPIN == pin:
        return True
    else:
        return False
    
# Retrieve the balances for the key specified by account_id
def getBalances(account_id):
    return float(r.hget(account_id, "CheckingBalance")), float(r.hget(account_id, "SavingsBalance"))

# Retrieve the name for the key specified by account_id
def getName(account_id):
    return str(r.hget(account_id, "Name"), 'utf-8')

# A helper function to truncate values past the hundredths place
def trunc(total):
    total *= 100
    total = math.trunc(total)
    total /= 100

    return total

# Deposit total into the account specified by typ at key account_id
def deposit(account_id, typ, total):
    global r
    
    # Prevent sub-cent amounts from being deposited
    total = trunc(total)

    if typ == 'C':
        newBal = float(r.hget(account_id, "CheckingBalance")) + total
        r.hset(account_id, "CheckingBalance", newBal)
    elif typ == 'S':
        newBal = float(r.hget(account_id, "SavingsBalance")) + total
        r.hset(account_id, "SavingsBalance", newBal)
    
# Withdraw total from the account specified by typ at key account_id
def withdraw(account_id, typ, total):
    global r
    
    # Prevent sub-cent amounts from being withdrawn
    total = trunc(total)

    if typ == 'C':
        if float(r.hget(account_id, "CheckingBalance")) >= total:
            newBal = float(r.hget(account_id, "CheckingBalance")) - total
            r.hset(account_id, "CheckingBalance", newBal)
            return True
        else:
            return False
    elif typ == 'S':
        if float(r.hget(account_id, "SavingsBalance")) >= total:
            newBal = float(r.hget(account_id, "SavingsBalance")) - total
            r.hset(account_id, "SavingsBalance", newBal)
            return True
        else:
            return False

# Transfer total from the account specified by typ at key account_id into the user's other account
def transfer(account_id, typ, total):
    global r
    
    # Prevent sub-cent amounts from being transferred
    total = trunc(total)

    if typ == 'C':
        if float(r.hget(account_id, "CheckingBalance")) >= total:
            newBal = float(r.hget(account_id, "CheckingBalance")) - total
            r.hset(account_id, "CheckingBalance", newBal)
            newBal = float(r.hget(account_id, "SavingsBalance")) + total
            r.hset(account_id, "SavingsBalance", newBal)
            return True
        else:
            return False
        
    elif typ == 'S':
        if float(r.hget(account_id, "SavingsBalance")) >= total:
            newBal = float(r.hget(account_id, "SavingsBalance")) - total
            r.hset(account_id, "SavingsBalance", newBal)
            newBal = float(r.hget(account_id, "CheckingBalance")) + total
            r.hset(account_id, "CheckingBalance", newBal)
            return True
        else:
            return False
