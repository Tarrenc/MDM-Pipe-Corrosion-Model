from GeometryPy import PipeClass #import the pipe class (Tarren Clark)
from DepthPy import DepthClass #import the depth class (Ivan Barranco Gomez)
from DiffusionPy import CorrosionProb #import the probability class (Luis Liang and Bin Wang)
import numpy as np #import numpy for mathematical operations
import matplotlib.pyplot as plt #import matplotlib for graphical operations


#%% Parameters
#time variables
time=3650 #Period of time in question

#geometry variables
radius=10 #Radius
points=50  #nPoints
area= np.pi*radius**2 #cross sectional area
thickness=10 #wall thickness


#material variables
rho=8.96 #material density

#walk variables
p=0 #bias
q=0.4 #diffusion coefficient
#misc variables
switch=False #probability (True) or random walk (Fals)


#%%Functions
def Init(time, radius, points, thickness,rho, p, q): #Initialise the programme
    Pipe=PipeClass(radius, points,thickness, p, q) #create instance of the pipe class
    Depth=DepthClass(thickness,radius ,rho) #create an instance of the depth class
    Prob=CorrosionProb(time) #create an instance of the probability class
    
    return Pipe,Depth,Prob #return the instances

def Run(time,radius,points,thickness, p, q, rho): #Run the programme
    Instances = Init(time,radius,points,thickness,rho, p, q) #retrieve the instances
    Ncorrosions=[] #list to store the discrete corrosion events
    if switch==True: #if using probabilities
        print('############### Retrieving Pipe Corrosion Probabilities ###############')
        Probabilities=Instances[2].CorroProb() #retrieve probabilities
        print('############### Pipe Corrosion Probabilities Retrieved ###############')
        print('############### Calculating Number of Corrosive Events ###############')
        for i in range(points):
            Ncorrosions.append(Instances[0].Statistical(Probabilities,time)) #ca
    else: #if using random walk
        print('############### Calculating Corrosions Through Random Walks ###############')
        for i in range(points):
            Ncorrosions.append(Instances[0].RWalk(p,q,time))
    print('############### Number of Corrosive Events Found ###############')
    print('############### Calculating Magnitude of Corrosion ###############')
    
    
    global depths
    depths=Instances[1].LossWeightEq(np.array(Ncorrosions)/365)
    
    DeformedPipe,test,test1=Instances[0].Movement(depths)
    print('############### Magnitude of Corrosion Found ###############')
    PostProc(DeformedPipe, radius, thickness,Instances,depths)
    return DeformedPipe,test,test1
    

def PostProc(FinalPipe,radius,thickness,Instances,Depths): #Create various graphs etc
    global PointsOutter
    Angle,Points,PointsOutter=Instances[0].Circle()
    fig, ax = plt.subplots()
    ax.grid()
    ax.axis('equal')
    ax.plot(Points[:,0],Points[:,1],'r',label='Undeformed Inner Surface',alpha=0.5)
    ax.plot(PointsOutter[:,0],PointsOutter[:,1],'g',label='Outter Surface',markersize=3)
    ax.plot(FinalPipe[:,0],FinalPipe[:,1],'--bo',label='Deformed Surface',markersize=3)
    ax.legend()
    ax.set(xlabel='x', ylabel='y')
    ax.legend(loc='lower left',prop={'size': 7})
    print('Average corrosion depth: ', np.mean(np.array(Depths)))

    



#%% Run Programme
x,y,z  = Run(time,radius,points,thickness, p , q,rho)

