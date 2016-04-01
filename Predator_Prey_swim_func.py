import numpy as np
import matplotlib.pyplot as plt



Fish_number = []
Shark_number = []
size = 10 # grid size
breed_age = 15

Fish = -1*np.ones((size, size), dtype=np.int)
Shark = -1*np.ones((size, size), dtype=np.int)
Fishmove = np.ones((size, size), dtype=np.int)
Sharkmove = np.ones((size, size), dtype=np.int)
Sharkstarve = np.ones((size, size), dtype=np.int)
Fish[5,5] = 13
print Fish

def Fish_swim_breed(i,j):
    if Fish(i,j) != -1: # if there is a fish in (i,j)
        choice = np.zeros(4)
        if Fish(i-1,j) == -1:
            choice[0] = 1 # record index if left position is vacant
        if Fish(i+1,j) == -1: 
            choice[1] = 2 # record index if right position is vacant
        if Fish(i, j+1) == -1:
            choice[2] = 3 # record index if up position is vacant
        if Fish(i, j-1) == -1:
            choice[3] = 4 # record index if down position is vacant
        Choice = filter(None, choice) # only vacant positions are reserved
        temp = [Fish(i-1,j), Fish(i+1,j), Fish(i,j+1), Fish(i,j-1)] # temperary storage
        if np.size(Choice)>0:
            index = np.random.choice(Choice)-1 # choose one vacant position randomly
            temp[index] = Fish(i,j)+1  # a chosen position is replaced by fish (i,j) and age is increased
            if temp[index] > breed_age:
                Fish(i,j) = 0
                temp[index] = 0
            else:
                Fish(i,j) = -1 # original position is now vacant
            Fish(i-1,j) = temp[0] # Yes, this is not efficient......
            Fish(i+1,j) = temp[1]
            Fish(i,j+1) = temp[2]
            Fish(i,j-1) = temp[3]

i = 5
j = 5
#Fish = Fish_swim_breed(i,j)        
print Fish     
            
            
            
            
            
            
            
            
            
            
            