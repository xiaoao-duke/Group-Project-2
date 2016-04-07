
from pylab import*
import random as rd
import time

Fish_number = []
Shark_number = []
Total = []
Time = 1000
global size
size = 100 # grid size
n0_fish = 2000 # initial number of fish
n0_sharks = 200 # initial number of sharks
breed_age_fish = 15
breed_age_shark = 25
starve_time = 20
t = 0
Fish = -1*np.ones((size+1, size+1), dtype=np.int)
Shark = -1*np.ones((size+1, size+1), dtype=np.int)
Fishmove = -1*np.ones((size+1, size+1), dtype=np.int)
Sharkmove = -1*np.ones((size+1, size+1), dtype=np.int)
Sharkstarve = np.zeros((size+1, size+1), dtype=np.int)

# initial condition for Fish
k = 0
while k < int(n0_fish):
    i = int(size*rd.random())-1
    j = int(size*rd.random())-1
    if Fish[i,j] == -1:
        age = int((breed_age_fish-1)*rd.random()) # assign fish random age
        Fish[i,j] = age
        k += 1
# initial condition for Shark
k = 0
while k < int(n0_sharks):
    i = int(size*rd.random())-1
    j = int(size*rd.random())-1
    if Shark[i,j] == -1 and Fish[i,j] == -1:
        age = int((breed_age_shark-1)*rd.random()) # assign shark random age
        Shark[i,j] = age
        Sharkstarve[i,j] = 0 
        k += 1


def boundary(point):
    (a, b) = point
    if point[0] < 0:
        a = point[0]+size+1
    if point[1] < 0:
        b = point[1]+size+1
    if point[0] >= size:
        a = point[0]-size-1
    if point[1] >= size:
        b = point[1]-size-1
    return (a,b)

def savfigs(t, Fish, Shark):
    myfig = figure(t)
    for i in range(size):
        for j in range(size):
            if Shark[i,j]!=-1:
                plt.plot(i,j,'.r')
            if Fish[i,j]!=-1:
                plt.plot(i,j,'.b')
    plt.xlabel("time = "+str(t))
    plt.title("Prey-Predator Model, Blue--Fish, Red--Shark")
    plt.savefig(str(t)+".jpg")
    #plt.show()
    #plt.clf()


def savphase(t, Fish_number, Shark_number):
    myfig = figure(t)
    plt.plot(Fish_number, Shark_number, '.-m')
    plt.title("Prey-Predator Phase Portrait--time = "+str(t))
    plt.ylim(ymin=0,ymax=1500)
    plt.xlim(xmin=0,xmax=8000)
    plt.xlabel("Fish")
    plt.ylabel("Shark")
    plt.savefig(str(10*t)+".jpg")

#Fish swim and breed
def Fish_swim_breed(fish0,Shark,breed_age):
    fishmove = -1*ones([size+1,size+1])
    fish = fish0
    # main part
    for i in range(size):
        for j in range(size):
            if fish[i,j] != -1 and fishmove[i,j] == -1: # if there is a fish in (i,j)
	        choice = np.zeros(4)
                if (fish[boundary([i-1,j])] == -1)&(Shark[boundary([i-1,j])] == -1):
                    choice[0] = 1 # record index if left position is vacant and will be vacant later
                if (fish[boundary([i+1,j])] == -1)&(Shark[boundary([i+1,j])] == -1):
                    choice[1] = 2 # record index if right position is vacant
                if (fish[boundary([i,j+1])] == -1)&(Shark[boundary([i,j+1])] == -1):
                    choice[2] = 3 # record index if up position is vacant
                if (fish[boundary([i,j-1])] == -1)&(Shark[boundary([i,j-1])] == -1):
                    choice[3] = 4 # record index if down position is vacant
         
                Choice = filter(None, choice) # only vacant positions are reserved
                temp = [(i-1,j), (i+1,j), (i,j+1), (i,j-1)] # temperary storage for index
                if np.size(Choice) > 0:
                    index = int(np.random.choice(Choice))-1 # choose one vacant position randomly
                    if fish[i,j] < breed_age:
                        fish[boundary(temp[index])] = fish[i,j]+1  # a chosen position is replaced by fish (i,j) and age is increased
                        fishmove[boundary(temp[index])] = 1
                        fish[i,j] = -1
                    else:  # if fish reach breed age
                        fish[boundary(temp[index])] = 0
                        fish[i,j] = 0
                        fishmove[boundary(temp[index])] = 1
                else:
                    fish[i,j] = fish[i,j]+1 # if no place to go then stay there and age
                    fishmove[i,j] = 1
    return fish

# shark hunt and breed
def Shark_hunt_breed(shark0, sharkstarve,fish,starve_time,breed_age):
    shark = shark0
    sharkmove = -1*ones([size+1,size+1])
    # main part(exclude boundaries)
    for i in range(size):
        for j in range(size):
            if shark[i,j] != -1 and sharkmove[i,j] == -1: # if there is a shark in (i,j)
                planA = np.zeros(4) # record choices with fish and no shark at a spot
                planB = np.zeros(4) # record choices without fish but no shark
                if (shark[boundary([i-1,j])] == -1):
                    if fish[boundary([i-1,j])] != -1:
                        planA[0] = 1
                    else:
                        planB[0] = 1
                if (shark[boundary([i+1,j])] == -1):
                    if fish[boundary([i+1,j])] != -1:
                        planA[1] = 2
                    else:
                        planB[1] = 2
                if (shark[boundary([i,j-1])] == -1):
                    if fish[boundary([i,j-1])] != -1:
                        planA[2] = 3
                    else:
                        planB[2] = 3
                if (shark[boundary([i,j+1])] == -1):
                    if fish[boundary([i,j+1])] != -1:
                        planA[3] = 4
                    else:
                        planB[3] = 4
                PlanA = filter(None,planA) # only fish and no shark coming spot are reserved
                PlanB = filter(None,planB) # no fish around spot without shark are reserved
                temp = [(i-1,j), (i+1,j), (i,j-1), (i,j+1)] # temperary storage for index
                if np.size(PlanA) > 0:
                    if sharkstarve[i,j] < starve_time :
                        index = int(np.random.choice(PlanA))-1 # choose one position randomly
                        fish[boundary(temp[index])] = -1
                        if shark[i,j] < breed_age:
                            shark[boundary(temp[index])] = shark[i,j]+1  # a chosen position is replaced by shark (i,j) and age is increased
                            shark[i,j] = -1
                            sharkmove[boundary(temp[index])] = 1
                            sharkstarve[boundary(temp[index])] = 0
                            #sharkstarve[i,j] = 0
                        else:  # if shark reach breed age
                            shark[boundary(temp[index])] = 0
                            shark[i,j] = 0
                            sharkmove[boundary(temp[index])] = 1
                            sharkstarve[boundary(temp[index])] = 0
                            sharkstarve[i,j] = 0
                    else : 
                        shark[i,j] = -1
                        #sharkstarve[i,j] = 0
    
                elif np.size(PlanB) > 0:
                    index = int(np.random.choice(PlanB))-1
                    if sharkstarve[i,j] < starve_time :
                        if shark[i,j] < breed_age:
                            shark[boundary(temp[index])] = shark[i,j]+1
                            shark[i,j] = -1
                            #sharkstarve[i,j] = 0
                            sharkmove[boundary(temp[index])] = 1
                            sharkstarve[boundary(temp[index])]= sharkstarve[i,j]+1
                        else:
                            shark[boundary(temp[index])] = 0
                            shark[i,j] = 0
                            sharkmove[boundary(temp[index])] = 1
                            sharkstarve[boundary(temp[index])] = sharkstarve[i,j]+1
                            sharkstarve[i,j] = 0
                    else :
                        shark[i,j] = -1
                        #sharkstarve[i,j] = 0
                else: # shark is surrounded by shark, shark do not move
                    if sharkstarve[i,j] < starve_time :
                        shark[i,j] = shark[i,j]+1
                        sharkmove[i,j] = 1
                        sharkstarve[i,j] = sharkstarve[i,j]+1
                    else :
                        shark[i,j] = -1
                        #sharkstarve[i,j] = 0
    return (fish, shark, sharkstarve)



# order for one time step: 1.fish swim and breed 2. shark hunt breed 3. shark eat fish

while t < Time:
    Fish = Fish_swim_breed(Fish, Shark, breed_age_fish)
    (Fish, Shark, Sharkstarve) = Shark_hunt_breed(Shark,Sharkstarve,Fish,starve_time,breed_age_shark)
    t=t+1

    # count number of fish and number of shark
    fish_num=0
    total = 0
    for i in range(size):
        for j in range(size):
            if Fish[i,j] != -1:
	        fish_num += 1
                total += 1
    Fish_number.append(fish_num)

    shark_num=0
    for i in range(size):
        for j in range(size):
            if Shark[i,j] != -1 :
	        shark_num += 1
                total += 1
    Shark_number.append(shark_num)
    Total.append(total)    
    savfigs(t, Fish, Shark)
    #savphase(t, Fish_number, Shark_number)
    print "Completed: "+str(100.0*t/Time)+"%"

figure()
plt.plot(Fish_number, '-b', label = "Fish")
plt.plot(Shark_number, '-r', label = "Shark")
#plt.plot(Total, '-g', label = "Total")
plt.legend()
plt.title("Prey-Predator Model")
plt.ylabel("Population")
plt.xlabel("time steps")
plt.savefig("pop4.jpg")
plt.savefig("pop4.pdf")
#plt.show()


