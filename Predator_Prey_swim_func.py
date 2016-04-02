from pylab import*


Fish_number = []
Shark_number = []
size = 100 # grid size
breed_age = 15

Fish = -1*np.ones((size+1, size+1), dtype=np.int)
Shark = -1*np.ones((size+1, size+1), dtype=np.int)
Fishmove = np.ones((size+1, size+1), dtype=np.int)
Sharkmove = np.ones((size+1, size+1), dtype=np.int)
Sharkstarve = np.ones((size+1, size+1), dtype=np.int)
Fish[5,5] = 13
print Fish
# initial condition for Fish
for j in range(100):
    for i in range(49):
        Fish[j,2*i+mod(j,2)]=0
# initial condition for Shark
for j in range(25):
    for i in range(24):
        Shark[4*j,4*i+mod(j,4)]=0

def Fish_swim_breed(yu,breed_age):
    fishmove=zeros([size+2,size+2])
    occupied=zeros([size+2,size+2])
    fish=zeros([size+2,size+2])
    fish[1:size+1,1:size+2]=yu   
    fish[0,1:size+1]=yu[size-1]  # match top with bottom to achieve periodic boundary
    fish[size+1,1:size+2]=yu[0]
    fish[1:size+1,0]=yu[:,size-1]
    fish[1:size+1,size+1]=yu[:,0]
    # main part(exclude boundaries)
    for i in range(1,size+1)
        for j in range(1,size+1)
            if fish[i,j] != -1: # if there is a fish in (i,j)
                choice = np.zeros(4)
                if (fish[i-1,j] == -1)&(occupied[i-1,j]==0):
                    choice[0] = 1 # record index if left position is vacant and will be vacant later
                if (fish[i+1,j] == -1)&(occupied[i+1,j]==0): 
                    choice[1] = 2 # record index if right position is vacant
                if (fish[i, j+1] == -1)&(occupied[i,j-1]==0):
                    choice[2] = 3 # record index if up position is vacant
                if (fish[i, j-1] == -1)&(occupied[i,j+1]==0):
                    choice[3] = 4 # record index if down position is vacant
                Choice = filter(None, choice) # only vacant positions are reserved
                temp = [(i-1,j), (i+1,j), (i,j+1), (i,j-1)] # temperary storage for index
                if np.size(Choice)>0:
                    index = np.random.choice(Choice)-1 # choose one vacant position randomly
                    if fish[i,j]<breed_age:
                        fishmove[temp[index]] = fishmove[temp[index]]+fish(i,j)+1  # a chosen position is replaced by fish (i,j) and age is increased
                        fishmove[i,j]=fishmove[i,j]-fish[i,j]-1 # action of erasing current fish
                        occupied[temp[index]]=1
                    else:  # if fish reach breed age
                        fishmove[temp[index]]=1
                        fishmove[i,j]=-fish[i,j]
                        occupied[temp[index]]=1
                else:
                    fishmove[i,j]=fishmove[i,j]+1 # if no place to go then stay there and age
    fishmove[1,1:size+1]=fishmove[1,1:size+1]+fishmove[size+1,1:size+1] # top boundary include from bottom to top(periodic boundary)
    fishmove[size,1:size+1]=fishmove[size,1:size+1]+fishmove[0,1:size+1]
    fishmove[1:size+1,1]=fishmove[1:size+1,1]+fishmove[1:size+1,size+1]
    fishmove[1:size+1,size]=fishmove[1:size+1,size]+fishmove[1:size+1,0]
    return fishmove[1:size+1,1:size+1]
def Shark_hunt_breed(shayu,shayustarve,fish,breed_age)
    sharkmove=zeros([size+2,size+2])
    occupied=zeros([size+2,size+2])
    sharkstarve=zeros([size+2,size+2]) # record shark starving time
    shark=zeros([size+2,size+2])
    shark[1:size+1,1:size+2]=shayu   
    shark[0,1:size+1]=shayu[size-1]  # match top with bottom to achieve periodic boundary
    shark[size+1,1:size+1]=shayu[0]
    shark[1:size+1,0]=shayu[:,size-1]
    shark[1:size+1,size+1]=shayu[:,0]
    sharkeat[1:size+1,1:size+1]=shayustarve
# main part(exclude boundaries)
    for i in range(1,size+1)
        for j in range(1,size+1)
            if shark[i,j] != -1: # if there is a shark in (i,j)
                choice = np.zeros(4)
            if (fish[i-1,j] != -1)&(occupied[i-1,j]==0):
                choice[0] = 1 # record index if there is a fish at (i-1,j) and no shark is coming
            if (fish[i+1,j] != -1)&(occupied[i+1,j]==0): 
                choice[1] = 2 
            if (fish[i, j+1] != -1)&(occupied[i,j-1]==0):
                choice[2] = 3
            if (fish[i, j-1] != -1)&(occupied[i,j+1]==0):
                choice[3] = 4
            Choice = filter(None, choice) # only fish and no shark coming spot are reserved
            temp = [(i-1,j), (i+1,j), (i,j+1), (i,j-1)] # temperary storage for index
            if np.size(Choice)>0:
                index = np.random.choice(Choice)-1 # choose one position randomly
                if fish[i,j]<breed_age:
                    fishmove[temp[index]] = fishmove[temp[index]]+fish(i,j)+1  # a chosen position is replaced by fish (i,j) and age is increased
                    fishmove[i,j]=fishmove[i,j]-fish[i,j]-1 # action of erasing current fish
                    occupied[temp[index]]=1
                else:  # if fish reach breed age
                    fishmove[temp[index]]=1
                    fishmove[i,j]=-fish[i,j]
                    occupied[temp[index]]=1
            else:
                fishmove[i,j]=fishmove[i,j]+1 # if no place to go then stay there and age
    fishmove[1,1:size+2]=fishmove[1,1:size+2]+fishmove[size+1,1:size+2] # top boundary include from bottom to top(periodic boundary)
    fishmove[size,1:size+2]=fishmove[size,1:size+2]+fishmove[0,1:size+2]
    fishmove[1:size+2,1]=fishmove[1:size+2,1]+fishmove[1:size+2,size+1]
    fishmove[1:size+2,size]=fishmove[1:size+2,size]+fishmove[1:size+2,0]
    return fishmove[1:size+2,1:size+2]







Fishmove=Fish_swim_breed
Fish=Fish+Fishmove
print Fish     
            
            
            
            
            
            
            
            
            
            
            
