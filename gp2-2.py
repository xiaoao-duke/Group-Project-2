from pylab import*
import random as rd
import time

Fish_number = []
Shark_number = []
dt = 0.1
Time = 10
movie = True
wait_time = 1.0
global size
size = 40 # grid size
breed_age_fish = 1.5
breed_age_shark = 2.5
starve_time = 2
t = 0
Fish = -1*np.ones((size+1, size+1), dtype=np.int)
Shark = -1*np.ones((size+1, size+1), dtype=np.int)
Fishmove = -1*np.ones((size+1, size+1), dtype=np.int)
Sharkmove = -1*np.ones((size+1, size+1), dtype=np.int)
Sharkstarve = np.zeros((size+1, size+1), dtype=np.int)

# initial condition for Fish
k = 0
while k < int(0.3*size**2):
    i = int(size*rd.random())-1
    j = int(size*rd.random())-1
    if Fish[i,j] == -1:
        Fish[i,j] = 0
        k += 1
# initial condition for Shark
k = 0
while k < int(0.04*size**2):
    i = int(size*rd.random())-1
    j = int(size*rd.random())-1
    if Shark[i,j] == -1 and Fish[i,j] == -1:
        Shark[i,j] = 0
        k += 1

def boundary(point):
    (a, b) = point
    if point[0] < 0:
        a = point[0]+1+size
    if point[1] < 0:
        b = point[1]+1+size
    if point[0] > size+1:
        a = point[0]-1-size
    if point[1] > size+1:
        b = point[1]-1-size
    return (a,b)

def savfigs(t, Fish, Shark):
    myfig = figure(t)
    for i in range(size):
        for j in range(size):
            if Shark[i,j]!=-1:
                plt.plot(i,j,'.r')
            if Fish[i,j]!=-1:
                plt.plot(i,j,'.b')
    plt.title("time = "+str(t))
    plt.xlabel("Blue--Fish, Red--Shark")
    plt.ylabel("Prey-Predator")
    #plt.savefig(str(t)+".jpg")
    plt.show()
    plt.clf()

#Fish swim and breed
def Fish_swim_breed(i,j,fish0,shark,breed_age):
    fishmove = -1*ones([size+1,size+1])
    fish = fish0
    # main part
    if fish[i,j] != -1: # if there is a fish in (i,j)
        choice = np.zeros(4)
        if (fish[i-1,j] == -1)&(fishmove[i-1,j] == -1)&(shark[i,j+1] == -1):
            choice[0] = 1 # record index if left position is vacant and will be vacant later
        if (fish[i+1,j] == -1)&(fishmove[i-1,j] == -1)&(shark[i,j+1] == -1):
            choice[1] = 2 # record index if right position is vacant
        if (fish[i,j+1] == -1)&(fishmove[i-1,j] == -1)&(shark[i,j+1] == -1):
            choice[2] = 3 # record index if up position is vacant
        if (fish[i,j-1] == -1)&(fishmove[i-1,j] == -1)&(shark[i,j+1] == -1):
            choice[3] = 4 # record index if down position is vacant
        Choice = filter(None, choice) # only vacant positions are reserved
        temp = [(i-1,j), (i+1,j), (i,j+1), (i,j-1)] # temperary storage for index
        if np.size(Choice) > 0:
            index = int(np.random.choice(Choice))-1 # choose one vacant position randomly
            if fish[i,j] < breed_age:
                fish[boundary(temp[index])] = fish[i,j]+1  # a chosen position is replaced by fish (i,j) and age is increased
                fish[i,j] = -1
            else:  # if fish reach breed age
                fish[boundary(temp[index])] = 0
                fish[i,j] = 0
        else:
            fish[i,j] = fish[i,j]+1 # if no place to go then stay there and age
    return fish

# shark hunt and breed
def Shark_hunt_breed(i,j,shark0,sharkstarve,fish,starve_time,breed_age):
    sharkmove = -1*ones([size+1,size+1])
    shark = shark0
    # main part(exclude boundaries)
    if shark[i,j] != -1: # if there is a shark in (i,j)
        planA = np.zeros(4) # record choices with fish and no shark at a spot
        planB = np.zeros(4) # record choices without fish but no shark
        if (shark[i-1,j] == -1)&(sharkmove[i-1,j] == -1):
            if fish[i-1,j] != -1:
                planA[0] = 1
            else:
                planB[0] = 1
        if (shark[i+1,j] == -1)&(sharkmove[i+1,j] == -1):
            if fish[i+1,j] != -1:
                planA[1] = 2
            else:
                planB[1] = 2
        if (shark[i,j-1] == -1)&(sharkmove[i,j-1] == -1):
            if fish[i,j-1] != -1:
                planA[2] = 3
            else:
                planB[2] = 3
        if (shark[i,j+1] == -1)&(sharkmove[i,j+1] == -1):
            if fish[i,j+1] != -1:
                planA[3] = 4
            else:
                planB[3] = 4
        PlanA = filter(None,planA) # only fish and no shark coming spot are reserved
        PlanB = filter(None,planB) # no fish around spot without shark are reserved
        temp = [(i-1,j), (i+1,j), (i,j-1), (i,j+1)] # temperary storage for index
        if np.size(planA) > 0:
            index = int(np.random.choice(planA)-1) # choose one position randomly
            fish[boundary(temp[index])] = -1
            if shark[i,j] < breed_age:
                shark[boundary(temp[index])] = shark[i,j]+1  # a chosen position is replaced by shark (i,j) and age is increased
                shark[i,j] = -1
                sharkstarve[boundary(temp[index])] = 0
                sharkstarve[i,j] = 0
		#### remove fish?
            else:  # if shark reach breed age
                shark[boundary(temp[index])] = 0
                shark[i,j] = 0
                sharkstarve[boundary(temp[index])] = 0
                sharkstarve[i,j] = 0
        elif np.size(planB) > 0:
            index = int(np.random.choice(planB)-1)
            if sharkstarve[index]+1 < starve_time:
                if shark[i,j] < breed_age:
                    shark[boundary(temp[index])] = shark[i,j]+1
                    shark[i,j] = -1
                    sharkstarve[boundary(temp[index])]= sharkstarve[i,j]+1
                    sharkstarve[i,j] = 0
                else:
                    shark[boundary(temp[index])] = 0
                    shark[i,j] = 0
                    sharkstarve[boundary(temp[index])] = sharkstarve[i,j]+1
                    sharkstarve[i,j] = 0
            else :
                shark[i,j] = -1
        else: # shark is surrounded by shark, shark do not move
            if sharkstarve[i,j]+1 < starve_time:
                shark[i,j] = shark[i,j]+1
                sharkstarve[i,j] = sharkstarve[i,j]+1
            else :
                shark[i,j] = -1
    return (fish, shark,sharkstarve)

# when shark encounter a fish, erase the fish
def Fisheaten(fish,shark):
    for i in range(size):
        for j in range(size):
            if shark[i,j] != -1 and fish[i,j] != -1:
                fish[i,j] = -1
    return fish

# function for plotting
def plot_ocean(fish_num,shark_num):
    for i in range(size):
        for j in range(size):
            if Shark[i,j]!=-1:
                plt.plot(i,j,'or')
            if Fish[i,j]!=-1:
                plt.plot(i,j,'ob')
    plt.title("time = "+str(t)+'\tSharks: ' + str(shark_num)+'\tFish: ' + str(fish_num))
    plt.xlabel("Blue--Fish, Red--Shark")
    plt.show()
    plt.pause(wait_time)

# make initial plot
if movie:
    plt.ion()
    plt.figure()
    plt.title("time = "+str(t))
    plt.xlabel("Blue--Fish, Red--Shark")
    for i in range(size):
        for j in range(size):
            if Shark[i,j]!=-1:
                plt.plot(i,j,'or')
            if Fish[i,j]!=-1:
                plt.plot(i,j,'ob')
    plt.show()
    plt.pause(wait_time)

# order for one time step: 1.fish swim and breed 2. shark hunt breed 3. shark eat fish

while t < Time:
    plt.clf()

    for i in range(size):
        for j in range(size):
            Fish = Fish_swim_breed(i,j,Fish, Shark, breed_age_fish)
            (Fish, Shark, Sharkstarve) = Shark_hunt_breed(i,j,Shark,Sharkstarve,Fish,starve_time,breed_age_shark)
            #Fish = Fisheaten(Fish,Shark)
    t=t+dt

    # count number of fish and number of shark
    fish_num=0
    for i in range(size):
        for j in range(size):
            if Fish[i,j] != -1:
	        fish_num += 1
    Fish_number.append(fish_num)
    shark_num=0
    for i in range(size):
        for j in range(size):
            if Shark[i,j] != -1 :
	        shark_num += 1
    Shark_number.append(shark_num)
    print "Completed: "+str(100*t/Time)+"%"

    if movie: plot_ocean(fish_num,shark_num) # update the plot

figure
plt.plot(Fish_number, '-b', label = "Fish")
plt.plot(Shark_number, '-r', label = "Shark")
plt.legend()
plt.title("Prey-Predator Model")
plt.ylabel("Population")
plt.xlabel("time")
plt.savefig("population.jpg")
plt.show()
