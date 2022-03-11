# Python code for 1-D random walk.
#%%Libraries
import numpy as np 
#%% Class 


class PipeClass: 
    
    def __init__(self, Radius, nPoints, thickness, p, q):
        self.Radius=Radius
        self.nPoints=nPoints
        self.thickness=thickness
        self.p=p
        self.q=q
    
    def RWalk(self,p,q,iterations): #function to describe a potential random walk
        Walk=[] #store the walk 
        WalkCount=0
        for i in range(iterations):
            left=(q/2)*(1-p)
            right=(q/2)*(1+p)
            still=1-q
            possibilities=[still,left,right]
            Walks=[]
            for j in range(3):
                rando=np.random.uniform(0,max(possibilities))
                Walks.append(possibilities[j]-rando)
            
            maxo=max(Walks)
            index=Walks.index(maxo)
            if index==1:
                WalkCount+=1
            elif index==2:
                WalkCount+=1
            else:
                pass
            Walk.append(index)
        return WalkCount
    
    def Statistical(self, Probability, iterations):
        CorroCount=0
        for i in range(iterations):
            rando=np.random.uniform(0,1)
            if Probability[i]>=rando:
                CorroCount+=1
            else:
                pass
        return CorroCount
        
    
    def Circle(self): #draw a circle
        theta=np.linspace(0,2*np.pi,self.nPoints)
        x=self.Radius*np.cos(theta)
        y=self.Radius*np.sin(theta)
        x1=(self.Radius+self.thickness)*np.cos(theta)
        y1=(self.Radius+self.thickness)*np.sin(theta)
        points=list(zip(x,y))
        points1=list(zip(x1,y1))
        points=np.array([np.array(list(x)) for x in points])
        points1=np.array([np.array(list(x)) for x in points1])
        return theta,points,points1
    
    
    def Movement(self,LineChanges): #function to deform the PipeClass
        Theta,Points,PointsUnused = self.Circle()
        Circle=np.array(Points)
        X_mov=[]
        Y_mov=[]
        for i in range(len(LineChanges)):
            X_mov.append(abs(LineChanges[i]*np.cos(Theta[i])))
            Y_mov.append(abs(LineChanges[i]*np.sin(Theta[i])))
        DCircle=[]
        for i in range(len(LineChanges)):
            if Points[i][0]<=0 and Points[i][1]>=0:
                DCircle.append(Circle[i]+[-X_mov[i],Y_mov[i]])
            elif Points[i][0]>=0 and Points[i][1]>=0:
                DCircle.append(Circle[i]+[X_mov[i],Y_mov[i]])
            elif Points[i][0]>=0 and Points[i][1]<=0:
                DCircle.append(Circle[i]+[X_mov[i],-Y_mov[i]])
            else:
                DCircle.append(Circle[i]+[-X_mov[i],-Y_mov[i]])
            
        return np.array(DCircle),Theta,Points



