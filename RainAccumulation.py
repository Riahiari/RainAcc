#This simulation works by creating a 3D environment filled with raindroplets. These raindroplets are then
#given a constant velocity and move through the environment by v*dt every timestep. An object is also placed
#in this environment with dimensions l,w,h which are parallel to x,y,z respectively. The object is then given a
#velocity vObject = <ovx,ovy>.  When the raindroplets are within the boundaries of this object they are placed 
#below the frame such that they only count once toward the accumilation of the rain on the object. The frame 
#Must have a sufficiently high height for the simulation since the density of raindrops cannot be changed and the
#droplets are placed uniformly throughout the environment. 

#The object follows a straight path from some coordinate (ox1,oy1) to (ox2,oy2) at some velocity <ovx,ovy>. The 
#timeframe of the simulation is calculated based on the distance and velocity of the path. This makes it easier 
#to compare the rain accumilated over the same path with two different speeds or geometries. 
 

#The  dimensions of the frame in which the simulation occurs. This is also the boundary in which the
#rain droplets are placed.
frame_height = 40
frame_length = 150
frame_width = 10
frame_size = frame_length*frame_height*frame_width

#Velocity of the rain droplets
vx = 2
vy = 0
vz = -2

#Object Position and Velocity
ox = 10 #initial x
oy = 0 #initial y
ovx = 2 #x component of object velocity
ovy = 0 #y component of object velocity

#Object initial and final position, as well as timeframe of simulation based on the former variables.
ox1 = float(ox) #initial x
oy1 = float(oy) #initial y
ox2 = 70.0 #final x
oy2 = 10.0 #final y

timeframe = (ox2-ox1)/ovx #timeframe of simulation calculated based on path and velocity

#Object dimensions
ol = 2 #changes face C
ow = 7 #changed both A and C
oh = 7 #changes face A

#Rain mass counter and droplet mass
drop_mass = 1 #Mass per droplet
rain_mass = 0 #Total mass of rain that has made contact with the object

#Simulation timestep calculation.
dt = 0.05*ol/ovx
#The reason it's calculated like this is to avoid errors where the object moves too much in one timestep, causing the
#collision between rain and object to not occur where it should. This makes it so that in each timestep, the object
#moves 5% of it's length so that in the majority of simulations the non-collision problem is avoided.

#Each raindrop is of the class "Raindrop" and so each drop has a coordinate in the simulation
class Raindrop:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


#Rain generation
Rains = [] #This is an array of all the raindroplets in the simulation. In this for-loop the raindroplets are created
            #and they are appended to the array. They are placed uniformly throughout the frame.

#This for-loop involves the placement of the rain droplets
for k in range(frame_height):
    for i in range(frame_length):
        for j in range(frame_width):
            Rains.append(Raindrop(i,j,k)) #Raindroplets are placed at each coordinate of the simulation


            #NOTCE how the rains array is a one dimensional array despite the rain being in 3 dimensions. Using indexing
            #techniques this is not a problem. 
            #The coordinate [k][i][j] corresponds to [k*frame_length*frame_width+i*frame_width+j]
        

#Prints the location of every rain droplet. Used for debugging.
def printLoc():
    for k in range(frame_height):
        for i in range(frame_length):
            for j in range(frame_width):
                print(vars([k*frame_length*frame_width+i*frame_width+j]))

#This was used to debug problems with the index
def printshawn ():
    for k in range(frame_height):
        for i in range(frame_length):
            for j in range(frame_width):
                print(k*frame_length*frame_width+i*frame_width+j)


#This checks if the rain is within the boundaries of the object
def rainCheck(q):
    if (Rains[q].x > ox and Rains[q].x < (ox+ol)) and (Rains[q].y > oy and Rains[q].y < (oy+ow)) and (Rains[q].z > 0 and Rains[q].z < oh):
        return True
    else:
        return False

#Since the object is placed on top of rain particles, the initial rain particles that are inside the object are removed
#and don't count toward the rain accumilation counter. This for loop does that.
def initCheck():
    for k in range(frame_height):
        for i in range(frame_length):
            for j in range(frame_width):
              if rainCheck(k*frame_length*frame_width+i*frame_width+j) == True:
                Rains[k*frame_length*frame_width+i*frame_width+j].z = -1


#Rain movement function for a single timestep
def timeStep():
    global ox
    global oy
    global ovx
    global ovy
    global rain_mass
    global ox1
    global oy1
    global ox2
    global oy2

    #Moving the object one timestep
    ox += ovx*dt 
    oy += ovy*dt

    #This for loop involves moving each raindroplet one timestep and checking if it is in the object
    for k in range(frame_height):
        for i in range(frame_length):
            for j in range(frame_width):
            #Moving the rain one timestep
                Rains[k*frame_length*frame_width+i*frame_width+j].x += vx*dt
                Rains[k*frame_length*frame_width+i*frame_width+j].y += vy*dt
                Rains[k*frame_length*frame_width+i*frame_width+j].z += vz*dt
                #Checking if there is rain in the object
                if rainCheck(k*frame_length*frame_width+i*frame_width+j) == True:
                    Rains[k*frame_length*frame_width+i*frame_width+j].z = -1
                    rain_mass += drop_mass


#Calculates rain and object movement over time
def moveRain(t):
    for i in range(int(t/dt)):
        timeStep()




initCheck()
print("Timeframe: "+str(timeframe))
moveRain(timeframe)
print("C: "+str(ow*ol)+" | A: "+str(ow*oh))
print("vx: "+str(vx)+" | ovx: "+str(ovx))
print("Mass of Rain: "+str(rain_mass))
print("complete")