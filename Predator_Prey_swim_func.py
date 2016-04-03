from pylab import*


Fish_number = []
Shark_number = []
size = 100 # grid size
breed_age_fish = 15
breed_age_shark=50
starve_time=10

Fish = -1*np.ones((size+1, size+1), dtype=np.int)
Shark = -1*np.ones((size+1, size+1), dtype=np.int)
Fishmove = -1*np.ones((size+1, size+1), dtype=np.int)
Sharkmove = -1*np.ones((size+1, size+1), dtype=np.int)
Sharkstarve = np.zeros((size+1, size+1), dtype=np.int)

# initial condition for Fish
for j in range(100):
    for i in range(49):
        Fish[j,2*i+mod(j,2)]=0
# initial condition for Shark
for j in range(25):
    for i in range(24):
        Shark[4*j,4*i+mod(j,4)]=0

def Fish_swim_breed(yu,breed_age):
    fishmove=-1*ones([size+2,size+2])
    fish=-1*ones([size+2,size+2])
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
                if (fish[i-1,j] == -1)&(fishmove[i-1,j]==0):
                    choice[0] = 1 # record index if left position is vacant and will be vacant later
                if (fish[i+1,j] == -1)&(fishmove[i+1,j]==0): 
                    choice[1] = 2 # record index if right position is vacant
                if (fish[i, j+1] == -1)&(fishmove[i,j-1]==0):
                    choice[2] = 3 # record index if up position is vacant
                if (fish[i, j-1] == -1)&(fishmove[i,j+1]==0):
                    choice[3] = 4 # record index if down position is vacant
                Choice = filter(None, choice) # only vacant positions are reserved
                temp = [(i-1,j), (i+1,j), (i,j+1), (i,j-1)] # temperary storage for index
                if np.size(Choice)>0:
                    index = np.random.choice(Choice)-1 # choose one vacant position randomly
                    if fish[i,j]<breed_age:
                        fishmove[temp[index]]=fish[i,j]+1  # a chosen position is replaced by fish (i,j) and age is increased
                    else:  # if fish reach breed age
                        fishmove[temp[index]]=0
                        fishmove[i,j]=0
                else:
                    fishmove[i,j]=fish[i,j]+1 # if no place to go then stay there and age
    fishmove[1,1:size+1]=fishmove[1,1:size+1]+fishmove[size+1,1:size+1] # top boundary include from bottom to top(periodic boundary)
    fishmove[size,1:size+1]=fishmove[size,1:size+1]+fishmove[0,1:size+1]
    fishmove[1:size+1,1]=fishmove[1:size+1,1]+fishmove[1:size+1,size+1]
    fishmove[1:size+1,size]=fishmove[1:size+1,size]+fishmove[1:size+1,0]
    return fishmove[1:size+1,1:size+1]
    
# shark hunt and breed
def Shark_hunt_breed(shayu,shayustarve,fish,stave_time,breed_age)
    sharkmove=-1*ones([size+2,size+2])
    sharkstarve=zeros([size+2,size+2]) # record shark starving time
    shark=-1*ones([size+2,size+2])
    shark[1:size+1,1:size+2]=shayu   
    shark[0,1:size+1]=shayu[size-1]  # match top with bottom to achieve periodic boundary
    shark[size+1,1:size+1]=shayu[0]
    shark[1:size+1,0]=shayu[:,size-1]
    shark[1:size+1,size+1]=shayu[:,0]
# main part(exclude boundaries)
    for i in range(1,size+1)
        for j in range(1,size+1)
            if shark[i,j] != -1: # if there is a shark in (i,j)
                planA = np.zeros(4) # record choices with fish and no shark at a spot
                planB=np.zeros(4) # record choices without fish but no shark
                if (shark[i-1,j]==-1)&(sharkmove[i-1,j]==-1):
                    if fish[i-1,j]!=1:
                        planA[0]=1
                    else:
                        planB[0]=1
                if (shark[i+1,j]==-1)&(sharkmove[i+1,j]==-1): 
                    if fish[i+1,j]!=-1:
                        planA[1]=1
                    else:
                        planB[1]=1
                if (shark[i,j-1]==-1)&(sharkmove[i,j-1]==-1):
                    if fish[i,j-1]!=-1
                        planA[2]=1
                    else:
                        planB[2]=1
                if (shark[i,j+1]==-1)&(sharkmove[i,j+1]==-1):
                    if fish[i,j+1]!=-1
                        planA[3]=1
                    else:
                        planB[3]=1
                PlanA = filter(None,planA) # only fish and no shark coming spot are reserved
                PlanB=filter(None,planB) # no fish around spot without shark are reserved
                temp = [(i-1,j), (i+1,j), (i,j-1), (i,j+1)] # temperary storage for index
                if np.size(planA)>0:
                    index = np.random.choice(planA)-1 # choose one position randomly
                    if shark[i,j]<breed_age:
                        sharkmove[temp[index]] =shark[i,j]+1  # a chosen position is replaced by fish (i,j) and age is increased
                        sharkstarve[temp[index]]=0
                    else:  # if shark reach breed age
                        sharkhmove[temp[index]]=shark[i,j]+1
                        sharkmove[i,j]=0
                        sharkstarve[temp[index]]=0
                        sharkstarve[i,j]=0
                elif np.size(planB)>0:
                    index=np.random.choice(planB)-1
                    if shayustarve[index]+1<starve_time:
                        if shark[i,j]<breed_age:
                            sharkmove[temp[index]]=shark[i,j]+1
                            sharkstarve[temp[index]]=shayustarve[i,j]+1
                        else:
                            sharkmove[temp[index]]=0
                            sharkmove[i,j]=0
                            sharkstarve[temp[index]]=shayustarve[i,j]+1
                            sharkstarve[i,j]=shayustarve[i,j]+1
                else: # shark is surrounded by shark, shark do not move
                    if shayustarve[i,j]+1<starve_time:
                        sharkmove[i,j]=shark[i,j]+1
                        sharkstarve[i,j]=shayustarve[i,j]+1
# match boundaries
    sharkmove[1,1:size+1]=sharkmove[1,1:size+1]+sharkmove[size+1,1:size+1]
    sharkmove[size,1:size+1]=sharkmove[size,1:size+1]+sharkmove[0,1:size+1]
    sharkmove[1:size+1,1]=sharkmove[1:size+1,1]+sharkmove[1:size+1,size+1]
    sharkmove[1:size+1,size]=sharkmove[1:size+1,size]+sharkmove[1:size+1,0]
    sharkstarve[1,1:size+1]=sharkstarve[1,1:size+1]+sharkstarve[size+1,1:size+1]
    sharkstarve[size,1:size+1]=sharkstarve[size,1:size+1]+sharkstarve[0,1:size+1]
    sharkstarve[1:size+1,1]=sharkstarve[1:size+1,1]+sharkstarve[1:size+1,size+1]
    sharkstarve[1:size+1,size]=sharkstarve[1:size+1,size]+sharkstarve[1:size+1,0]
    return (sharkmove[1:size+1,1:size+1],sharkstarve[1:size+1,1:size+1])

# when shark encounter a fish, erase the fish
def fisheaten(fish,shark)
    for i in range(100):
        for j in range(100):
            if shark[i,j]!=-1:
                fish[i,j]=-1
    return fish

# order for one time step: 1.fish swim and breed 2. shark hunt breed 3. shark eat fish
Fish=Fish_swim_breed(Fish,breed_age_fish)
Shark,SharkStarve=Shark_hunt_breed(Shark,SharkStarve,Fish,starve_time,breed_age_shark)
                


            
            
            
            
            
            
            
            
            
            
