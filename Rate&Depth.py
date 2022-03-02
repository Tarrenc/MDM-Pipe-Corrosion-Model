#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 16:09:16 2022

@author: ivanbarrancogomez
"""
import numpy as np
import matplotlib.pyplot as plt



##Parameters##
t = 14 #Wall thickness (mm)

#Corrosion Rate
Cr1 = lambda dt_total,T1,T2: (dt_total)/(T2-T1)

Cr2 = lambda MC02: 3.8263 * MC02 + 0.2796

Cr3 = lambda W,rho,A,T: (87.6*(W * A))/(rho*A*T)

#Depth of Corrosion
dt = lambda t,Cr,T: (0.20*t) + Cr * T

#Define dt1 and dt2 from Pipe Corrosion Data
dt1= 1
dt2 = 1

#Loss of Weight/Area
W = np.array([427e-6, 1.28e-3, 1.65e-3, 1.71e-3, 3.08e-3, 2.89e-3])
T = np.array([1, 3.6, 5.5, 7.7, 9.6, 1.6])
n = np.size(T)
Y = 3

def LossWeightEq(W,T,n,Y,rho,A,Yr,t,T_year):
    W_mean = np.mean(W)
    T_mean = np.mean(T)

    Sxy = np.sum(W*T)-n*W_mean*T_mean
    Sxx = np.sum(T*T)-n*W_mean*T_mean

    b1 = Sxy/Sxx
    b0 = W_mean-b1*T_mean

    y_pred = b1 * T + b0
    W_pred = b1 * Y + b0

    plt.scatter(T,W, color = 'red')
    plt.plot(T,y_pred, color = 'green')
    
    CR3 = Cr3(W_pred,rho,A,Yr)
    d_corrosion = dt(t,CR3,T_year)
    return d_corrosion

print(LossWeightEq(W,T,n,Y,1000,0.5,200,14,1))



def CorrosionMole(MC02,t,T_year):
 CR2 = (Cr2(MC02)*9.7811)+0.2203
 d_corrosion = dt(t,CR2,T_year)
 return d_corrosion


# =============================================================================
# def CorrosionRate1(dt1,dt2):
#      
#      CR1 = []
#      
#      for dt1 in zip(dt1,dt2):
#          dt_total = dt2 - dt1
#      
#      for i in dt_total:
#          CR1 = Cr1(dt_total,2,1) 
#          CR1.append(CR1)
#      
#      CR1 = sum(CR1)/len(CR1)
#          
#      return CR1
# =============================================================================

# =============================================================================
# def depth_corrosion(t,CR,T):
#     
#     dt_ar = []
#     for i in range(T):
#         dt_ar = dt(t,CR,T)
#         dt_ar.append(dt_ar)
#         return dt_ar
#         
# =============================================================================
    
    