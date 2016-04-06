from pylab import*
import random as rd
import time

Fish_number = []
Shark_number = []
dt = 0.1
Time = 10
movie = False
wait_time = 2.0
global size
size = 40 # grid size
breed_age_Fish = 10
breed_age_Shark = 4
starve_time = 3
t = 0
Fish = -1*np.ones((size+1, size+1), dtype=np.int)
Shark = -1*np.ones((size+1, size+1), dtype=np.int)
Fishmove = -1*np.ones((size+1, size+1), dtype=np.int)
Sharkmove = -1*np.ones((size+1, size+1), dtype=np.int)
Sharkstarve = np.zeros((size+1, size+1), dtype=np.int)

# initial condition for Fish
k = 0
while k < int(0.3*size**2):
#while k < int(1000):
    i = int(size*rd.random())-1
    j = int(size*rd.random())-1
    if Fish[i,j] == -1:
        Fish[i,j] = 0
        Fishmove[i,j] = 0
        k += 1
# initial condition for Shark
k = 0
while k < int(0.05*size**2):
#while k < int(1):
    i = int(size*rd.random())-1
    j = int(size*rd.random())-1
    if Shark[i,j] == -1 and Fish[i,j] == -1:
        Shark[i,j] = 0
        Sharkmove[i,j] = 0
        k += 1

def boundary(point):
    (a, b) = point
    if point[0] < 0:
        a = point[0]+size
    elif point[0] >= size:
        a = point[0]-size
    if point[1] < 0:
        b = point[1]+size
    elif point[1] >= size:
        b = point[1]-size
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
def Fish_swim_breed(i,j,Fish,Fishmove,Shark,Sharkmove,Sharkstarve):

    if Fish[i,j] != -1: # if there is a Fish in (i,j)

        choice = np.zeros(4)
        if (Fishmove[boundary([i-1,j])] == -1)&(Shark[boundary([i-1,j])] == -1):
            choice[0] = 1 # record index if left position is vacant and will be vacant later
        if (Fishmove[boundary([i+1,j])] == -1)&(Shark[boundary([i+1,j])] == -1):
            choice[1] = 2 # record index if right position is vacant
        if (Fishmove[boundary([i,j+1])] == -1)&(Shark[boundary([i,j+1])] == -1):
            choice[2] = 3 # record index if up position is vacant
        if (Fishmove[boundary([i,j-1])] == -1)&(Shark[boundary([i,j-1])] == -1):
            choice[3] = 4 # record index if down position is vacant

        Choice = filter(None, choice) # only vacant positions are reserved
        temp = [(i-1,j), (i+1,j), (i,j+1), (i,j-1)] # temperary storage for index


        if np.size(Choice) > 0:
            index = int(np.random.choice(Choice))-1 # choose one vacant position randomly

            if Fish[i,j] < breed_age_Fish:
                Fishmove[boundary(temp[index])] = Fish[i,j]+1  # a chosen position is replaced by Fish (i,j) and age is increased
                Fishmove[i,j] = -1

            else:  # if Fish reach breed age
                #print 'Breeding...'
                Fishmove[boundary(temp[index])] = 0
                Fishmove[i,j] = 0

        else:
            Fishmove[i,j] = Fish[i,j]+1 # if no place to go then stay there and age


# Shark hunt and breed
def Shark_hunt_breed(i,j,Fish,Fishmove,Shark,Sharkmove,Sharkstarve):

    # main part(exclude boundaries)
    if Shark[i,j] != -1: # if there is a Shark in (i,j)
        planA = np.zeros(4) # record choices with Fish and no Shark at a spot
        planB = np.zeros(4) # record choices without Fish but no Shark
        if (Sharkmove[boundary([i-1,j])] == -1):
            if Fish[boundary([i-1,j])] != -1:
                planA[0] = 1
            else:
                planB[0] = 1
        if (Sharkmove[boundary([i+1,j])] == -1):
            if Fish[boundary([i+1,j])] != -1:
                planA[1] = 2
            else:
                planB[1] = 2
        if (Sharkmove[boundary([i,j-1])] == -1):
            if Fish[boundary([i,j-1])] != -1:
                planA[2] = 3
            else:
                planB[2] = 3
        if (Sharkmove[boundary([i,j+1])] == -1):
            if Fish[boundary([i,j+1])] != -1:
                planA[3] = 4
            else:
                planB[3] = 4

        PlanA = filter(None,planA) # only Fish and no Shark coming spot are reserved
        PlanB = filter(None,planB) # no Fish around spot without Shark are reserved
        temp = [(i-1,j), (i+1,j), (i,j-1), (i,j+1)] # temperary storage for index
        if np.size(PlanA) > 0:
            index = int(np.random.choice(planA)-1) # choose one position randomly
            Fish[boundary(temp[index])] = -1
            if Shark[i,j] < breed_age_Shark:
                Sharkmove[boundary(temp[index])] = Shark[i,j]+1  # a chosen position is replaced by Shark (i,j) and age is increased
                Sharkmove[i,j] = -1
                Sharkstarve[boundary(temp[index])] = 0
                Sharkstarve[i,j] = 0
		#### remove Fish?
            else:  # if Shark reach breed age
                Sharkmove[boundary(temp[index])] = 0
                Sharkmove[i,j] = 0
                Sharkstarve[boundary(temp[index])] = 0
                Sharkstarve[i,j] = 0
        elif np.size(planB) > 0:
            index = int(np.random.choice(planB)-1)
            if Sharkstarve[i,j]+1 < starve_time:
                if Shark[i,j] < breed_age_Shark:
                    Sharkmove[boundary(temp[index])] = Shark[i,j]+1
                    Sharkmove[i,j] = -1
                    Sharkstarve[boundary(temp[index])]= Sharkstarve[i,j]+1
                    Sharkstarve[i,j] = 0

                else:
                    Sharkmove[boundary(temp[index])] = 0
                    Sharkmove[i,j] = 0
                    Sharkstarve[boundary(temp[index])] = Sharkstarve[i,j]+1
                    Sharkstarve[i,j] = 0
            else :
                Sharkmove[i,j] = -1
        else: # Shark is surrounded by Shark, Shark do not move
            if Sharkstarve[i,j]+1 < starve_time:
                Sharkmove[i,j] = Shark[i,j]+1
                Sharkstarve[i,j] = Sharkstarve[i,j]+1
            else :
                Sharkmove[i,j] = -1


# function for plotting
def plot_ocean(Fish_num,Shark_num):
    for i in range(size):
        for j in range(size):
            if Shark[i,j]!=-1:
                plt.plot(i,j,'or')
            if Fish[i,j]!=-1:
                plt.plot(i,j,'ob')
    plt.title("time = "+str(t)+'\tSharks: ' + str(Shark_num)+'\tFish: ' + str(Fish_num))
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

# order for one time step: 1.Fish swim and breed 2. Shark hunt breed 3. Shark eat Fish

while t < Time:

    # move fish
    for i in range(size):
        for j in range(size):
            if Fish[i,j] != -1:
                #print 'Fish_before'+str([t,i,j])+'=' + str(Fish[i,j])
                Fish_swim_breed(i,j,Fish,Fishmove,Shark,Sharkmove,Sharkstarve)
                #print 'NewFish_after' + str(bb) + ' ' + str(Fish[bb])
    Fish[:] = Fishmove

    # move sharks
    for i in range(size):
        for j in range(size):
            Shark_hunt_breed(i,j,Fish,Fishmove,Shark,Sharkmove,Sharkstarve)
    Shark[:] = Sharkmove

    t=t+dt

    # count number of Fish and number of Shark
    Fish_num=0
    for i in range(size):
        for j in range(size):
            if Fish[i,j] != -1:
	        Fish_num += 1
    Fish_number.append(Fish_num)
    Shark_num=0
    for i in range(size):
        for j in range(size):
            if Shark[i,j] != -1 :
	        Shark_num += 1
    Shark_number.append(Shark_num)
    print "Completed: "+str(100*t/Time)+"%"

    if movie:
        plt.clf()
        plot_ocean(Fish_num,Shark_num) # update the plot

figure
plt.plot(Fish_number, '-b', label = "Fish")
plt.plot(Shark_number, '-r', label = "Shark")
plt.legend()
plt.title("Prey-Predator Model")
plt.ylabel("Population")
plt.xlabel("time")
plt.savefig("population.jpg")
plt.show()
