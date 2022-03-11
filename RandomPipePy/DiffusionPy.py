import numpy as np
from sympy import integrate,solve,symbols 
import random


#%%
class CorrosionProb:
    
    def __init__(self,totaltime):
        self.t_mu=13.24
        self.t_sigma=0.899
        
        self.h_mu=72.2
        self.h_sigma=2.355                   #the condition of simulation   
        
        self.totaltime=totaltime
    
    def get_temprature(self):                 ##simulate climate and get the current temperature
        x=np.random.normal(loc = self.t_mu , scale= self.t_sigma,size = 100) 
        n=int(random.random()*100)
        return x[n]                             
    
    def get_humidity(self):                     ####simulate climate and get the current humidity
        x=np.random.normal(loc =self.h_mu , scale= self.h_sigma,size = 100) 
        n=int(random.random()*100)
        return x[n]
    
    # rho is a content
    def k_tcl(t0,T,be):                                    ##compute the k_tcl according to the equation
        # be = 4758                   #regression coeﬃcient
        # t0 = 20                     # reference temperature
        term = be*(1/(t0+273)-1/(T+273))
        k = np.exp(term)
        return k
    
    
    def k_hcl(rhc,rho):                                ##compute the k_hcl according to the equation
        kh=(1+(1-rhc)**4/(1-rho)**4)**(-1)
        return kh
    
    
    def m(FA,SG):        #  return the proportion of ﬂy ash and slag in the mixture
    # FA = 0.7
    # SG = 1.2
        return 0.2 + 0.4*(FA/50 +SG/70)
    
    
    # Dt:diffusion coeficient
    # No matter what format the basic time is (Y M D), it needs to be coverted into the day
    # d28 is a content
    
    def dt(t,d28,m):
        dt=d28*(28/t)**m
        return dt
    
    def pipe_pro(T,H):            #return the st and a value that need in the next
        m_1 = CorrosionProb.m(0.7,1.2)              #current m
        dt_1 =CorrosionProb.dt(T,70000*7.8,m_1)          #current dt
        k_tcl1 = CorrosionProb.k_tcl(1,T,4758)        #current k_tcl
        k_hcl1 = CorrosionProb.k_hcl(H,0.75)           #current k_hcl
        fun = k_tcl1*k_hcl1*dt_1         
        t = symbols('t')
        st = integrate(fun, (t, 1, t))    # get the value of s(t) with intergate
        c0 = 0.28
        cs = 18
        c_last = 0.69
        return (c_last - c0)/(cs-c0),st
    
    
    def val(value):                       #compute the result and if it get the value oof erf(x)
        a =0
        define = np.array(np.linspace(0,10,100))
        list =[0]
        for j in define:
            if np.sum(list)<value:
                list.append(np.exp(-j**2)*(10/100))
            else:
                a = j
                break
        return a
    
    
    def time(self):           #after the compute, get the value of the time that pipe undergo
        T = CorrosionProb.get_temprature(self)
        H = CorrosionProb.get_humidity(self)
        value_com, st = CorrosionProb.pipe_pro(T,H)
        value = 1-0.4
        a = CorrosionProb.val(value)
        final = (0.35**2)/4/a/a
        t = symbols('t')
        aa  = solve([final - st],[t])
        return aa
    
    
    def get_pro(self,cc):
        pro = np.zeros(9)
        probovertime=[]
        for i in cc:
            if i<=100.0:
                pro[0] += 1
            if 100.0<i<=150.0:
                pro[1] += 1
            if 150.0<i<=200.0:
                pro[2] += 1
            if 200.0<i<=250.0:
                pro[3] += 1
            if 250.0<i<=300.0:
                pro[4] += 1
            if 300.0<i<=350.0:
                pro[5] += 1
            if 350.0<i<=400.0:
                pro[6] += 1
            if 400.0<i<=450.0:
                pro[7] += 1
            else:
                pro[8] += 1
                
        for i in range(self.totaltime):
            #print(i)
            if i<=100.0:
                probovertime.append(pro[0])
            elif 100.0<i<=150.0:
                probovertime.append(pro[1])
            elif 150.0<i<=200.0:
                probovertime.append(pro[2])
            elif 200.0<i<=250.0:
                probovertime.append(pro[3])
            elif 250.0<i<=300.0:
                probovertime.append(pro[4])
            elif 300.0<i<=350.0:
                probovertime.append(pro[5])
            elif 350.0<i<=400.0:
                probovertime.append(pro[6])
            elif 400.0<i<=450.0:
                probovertime.append(pro[7])
            else:
                probovertime.append(pro[8])
                
        return np.array(probovertime)/self.totaltime
    
    
    def CorroProb(self):
        global cc,pro
        time_set =[]               ##draw the conclusion and graph
        for i in range(self.totaltime):
            time_set.append(self.time())
        cc =[]
        for z in time_set:
            cc.append(list(z.values())[0])
        cc = np.array(cc, dtype=float)
        ProbOverTime = CorrosionProb.get_pro(self,cc)
        return ProbOverTime #probability of corrosion over pipes lifetime
    


