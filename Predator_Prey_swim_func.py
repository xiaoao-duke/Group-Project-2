from pylab import*


Fish_number = []
Shark_number = []
size = 100 # grid size
breed_age = 15

Fish = -1*np.ones((size, size), dtype=np.int)
Shark = -1*np.ones((size, size), dtype=np.int)
Fishmove = np.ones((size, size), dtype=np.int)
Sharkmove = np.ones((size, size), dtype=np.int)
Sharkstarve = np.ones((size, size), dtype=np.int)
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
# boundary condition
Fish[0]=[round(15*sin(2*pi/size*i)*sin(t/10)) for i in range(100)]
Fish[99]=[round(15*sin(2*pi/size*i)*sin(t/10)) for i in range(100)]
Fish[:,0]=[round(15*sin(2*pi/size*i)*sin(t/10)) for i in range(100)]
Fish[:,99]=[round(15*sin(2*pi/size*i)*sin(t/10)) for i in range(100)]

def Fish_swim_breed(*fish,breed_age):
    fishmove=zeros([size,size])
    if fish(i,j) != -1: # if there is a fish in (i,j)
        choice = np.zeros(4)
        if fish(i-1,j) == -1:
            choice[0] = 1 # record index if left position is vacant
        if fish(i+1,j) == -1: 
            choice[1] = 2 # record index if right position is vacant
        if fish(i, j+1) == -1:
            choice[2] = 3 # record index if up position is vacant
        if fish(i, j-1) == -1:
            choice[3] = 4 # record index if down position is vacant
        Choice = filter(None, choice) # only vacant positions are reserved
        temp = [(i-1,j), (i+1,j), (i,j+1), (i,j-1)] # temperary storage for index
        if np.size(Choice)>0:
            index = np.random.choice(Choice)-1 # choose one vacant position randomly
            if fish[i,j]<breed_age:
                fishmove[temp[index]] = fishmove[temp[index]]+fish(i,j)+1  # a chosen position is replaced by fish (i,j) and age is increased
                fishmove[i,j]=fishmove[i,j]-fish[i,j]-1 # action of erasing current fish
            else:  # if fish reach breed age
                fishmove[temp[index]]=1
                fishmove[i,j]=-fish[i,j]
        else:
            fishmove[i,j]=fishmove[i,j]+1 # if no place to go then stay there and age
    return fishmove
def Shark_hunt_breed








Fishmove=Fish_swim_breed
Fish=Fish+Fishmove
print Fish     
            
            
            
            
            
            
            
            
            
            
            
