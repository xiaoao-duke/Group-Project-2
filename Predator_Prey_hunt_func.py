import numpy as np
import matplotlib.pyplot as plt


Fish_number = []
Shark_number = []
size = 5 # grid size
breed_age = 15 # breeding age
starving_age = 5
Fish = -1*np.ones((size, size), dtype=np.int)
Shark = -1*np.ones((size, size), dtype=np.int)
Fishmove = np.ones((size, size), dtype=np.int)
Sharkmove = np.ones((size, size), dtype=np.int)
Sharkstarve = -1*np.ones((size, size), dtype=np.int)

Fish[2,2] = 3 # a fish is put at [2,2]
Fish[2,1] = 3 # another fish is put at [2,1]
Fish[4,2] = 3
Fish[3,3] = 3
Shark[3,2] = 14 # a shark is put at [2,2]
Shark[3,1] = 10 # another shark is put at [2,1]

print Fish
print Shark

def Shark_hunt_breed(i,j):
    if Shark[i,j] != -1: # if there is a shark in (i,j)
        choice = np.zeros(4)
        if Fish[i-1,j] != -1:
            choice[0] = 1 # record index if left position is a fish
        if Fish[i+1,j] != -1: 
            choice[1] = 2 # record index if right position is a fish
        if Fish[i, j+1] != -1:
            choice[2] = 3 # record index if up position is a fish
        if Fish[i, j-1] != -1:
            choice[3] = 4 # record index if down position is a fish
        Choice = filter(None, choice) # only positions with fish are reserved
        temp = [Fish[i-1,j], Fish[i+1,j], Fish[i,j+1], Fish[i,j-1]] # temperary storage for fish
        if np.size(Choice)>0: # if there is at least one fish
            index = np.random.choice(Choice)-1 # choose one fish position randomly
            if index == 0:
                shark_index = i-1,j
            if index == 1:
                shark_index = i+1,j
            if index == 2:
                shark_index = i,j+1
            if index == 3:
                shark_index = i,j-1               
            temp[int(index)] = -1 # a chosen fish is eaten by shark
            Shark[shark_index] = Shark[i,j]+1 # move shark to new position increase shark age
            Sharkstarve[shark_index] = 0
            if Shark[shark_index] > breed_age:
                Shark[i,j] = 0
                Shark[shark_index] = 0
            else:
                Shark[i,j] = -1 # original position is now vacant
                Sharkstarve[shark_index] = Sharkstarve[i,j]+1
                Sharkstarve[i,j] = -1
            Fish[i-1,j] = temp[0] # Yes, this is not efficient......
            Fish[i+1,j] = temp[1]
            Fish[i,j+1] = temp[2]
            Fish[i,j-1] = temp[3]
###########################################################################################

Shark_hunt_breed(3,2)
print Fish
print Shark