#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 16:09:16 2022

@author: ivanbarrancogomez
"""
import numpy as np
import matplotlib.pyplot as plt


t = 14 #Wall thickness (mm)

#Corrosion Rate method with change in volume
Cr1 = lambda dt_total,T1,T2: (dt_total)/(T2-T1)

#Corrosion Rate method with moles of CO2
Cr2 = lambda MC02: 3.8263 * MC02 + 0.2796

#Corrosion Rate method with change in weight
Cr3 = lambda W,rho,r,Yr: (87.6* W /(rho*(np.pi * r**2)*Yr))

#Depth of Corrosion
dt = lambda t,Cr,T: (0.20*t) + Cr * T

#Define dt1 and dt2 from Pipe Corrosion Data
dt1= 1
dt2 = 1

#Loss of Weight from Data
W = np.array([1.67e3, 5.85e3, 7.5e3, 9.19e3, 13.08e3, 13.22e3])
#Time from the recording in years of weight loss measurement
T = np.array([1, 3.6, 5.5, 7.7, 9.6, 11.6])
n = np.size(T)
#Y = Year of interest
Y = 8

def LossWeightEq(W,T,n,Y,rho,A,Yr,t):
    """
    LossWeightEq caluclates the depth of corrosion using the corrosion rate 
    model of loss of weight of pipe

    Parameters
    ----------
    W : np.array
        Array containing the loss of weight information for the pipe
    T : np.array
        Time of inspection in years of pipe weight loss
    n : Float value
        Number of values in the np.array of T
    Y : Float value
        Year of interest
    rho : Float value
        Density of pipe material
    A : Float value
        Cross sectional area of pipe
    Yr : Float value
        Time of inspection in hours
    t : Float value
        Thickness of the pipe


    Returns
    -------
    d_corrosion : Float value
        Change in depth of the pipe

    """
    W_mean = np.mean(W)
    T_mean = np.mean(T)

    Sxy = np.sum(W*T)-n*W_mean*T_mean
    Sxx = np.sum(T*T)-n*T_mean*T_mean

    b1 = Sxy/Sxx
    b0 = W_mean-b1*T_mean

    y_pred = b1 * T + b0
    W_pred = b1 * Y + b0
    
# =============================================================================
#     m,c = np.polyfit(T,W,1)
#     eq = W * m +c
# =============================================================================

    plt.scatter(T,W, color = 'red')
    plt.plot(T,y_pred, color = 'green')
    
    print()
    CR3 = Cr3(W_pred,rho,A,Yr)
    d_corrosion = dt(t,CR3,Y)
    return d_corrosion

print(LossWeightEq(W,T,n,Y,8.96,3.81,70080,1))



def CorrosionMole(MC02,t,Y):
    """
    

    Parameters
    ----------
    MC02 : Float type
        Moles of CO2 present in the water of the pipe
    t : Float type
        Tickness of the pipe
    Y : Float type
        Year of inspection

    Returns
    -------
    d_corrosion : Float value
        Depth of corrosion of pipe

    """
    CR2 = (Cr2(MC02)*9.7811)+0.2203
    d_corrosion = dt(t,CR2,Y)
    return d_corrosion

    
print(CorrosionMole(0.2,1,1))


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
    
    