# -*- coding: utf-8 -*-
"""
Name: Ezriel Ciriaco
      Zachary Dulac
"""

import redis
r = redis.Redis(host = "redis-18248.c15.us-east-1-2.ec2.cloud.redislabs.com", port = "18248", password = "P4eSETx01bA5elBJEDWkfvUmngXhZrbY")
    
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
    
def getBalances(account_id):
    return float(r.hget(account_id, "CheckingBalance")), float(r.hget(account_id, "SavingsBalance"))

def getName(account_id):
    return str(r.hget(account_id, "Name"), 'utf-8')

def deposit(account_id, typ, total):
    global r
            
    if typ == 'C':
        newBal = float(r.hget(account_id, "CheckingBalance")) + total
        r.hset(account_id, "CheckingBalance", newBal)
    elif typ == 'S':
        newBal = float(r.hget(account_id, "SavingsBalance")) + total
        r.hset(account_id, "SavingsBalance", newBal)
    

def withdraw(account_id, typ, total):
    global r
            
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

def transfer(account_id, typ, total):
    global r
    
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
