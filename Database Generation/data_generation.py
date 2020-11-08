# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 19:33:46 2020

@author: Ezriel Ciriaco <eciriaco@fordham.edu> & Zachary Dulac <zdulac@fordham.edu>
"""

import redis
import random
import math

r = redis.Redis(host = "redis-18248.c15.us-east-1-2.ec2.cloud.redislabs.com", port = "18248", password = "P4eSETx01bA5elBJEDWkfvUmngXhZrbY")

def line_appender(file_path, target):
	file = open(file_path,'r')
	splitfile = file.read().splitlines()
	for line in splitfile:
		target.append(line)

def name_selector(target_list):
	selected = target_list[random.randrange(len(target_list))]
	return selected
        
def name_builder(first_name_list_path, last_name_list_path):
	first_name_list = []
	last_name_list = []

	line_appender(first_name_list_path, first_name_list)
	line_appender(last_name_list_path, last_name_list)

	first_name_selected = name_selector(first_name_list)
	last_name_selected = name_selector(last_name_list)

	name = first_name_selected+" "+last_name_selected
	return name

for i in range(0, 100):
    ssn = random.randint(3121, 5672)
    name = name_builder('first_names_list.txt', 'last_names_list.txt')
    pin = random.randint(1000, 9999)
    
    cb = random.uniform(0, 200000)
    cb *= 100
    cb = math.trunc(cb)
    cb /= 100
    
    sb = random.uniform(0, 1200000)
    sb *= 100
    sb = math.trunc(sb)
    sb /= 100

    d = {"SSN":ssn, "Name":name, "PIN":pin, "CheckingBalance":cb, "SavingsBalance":sb}

    r.hset(name = i, mapping = d)
