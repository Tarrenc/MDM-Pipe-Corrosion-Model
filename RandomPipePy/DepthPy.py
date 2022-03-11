#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 16:09:16 2022

@author: ivanbarrancogomez
"""
import numpy as np
import matplotlib.pyplot as plt

class DepthClass:
    
    def __init__(self,t,r,rho): 
        self.t = t #Wall thickness (mm)
        self.W = np.array([1.67e3, 5.85e3, 7.5e3, 9.19e3, 13.08e3, 13.22e3])
        self.T = np.array([1, 3.6, 5.5, 7.7, 9.6, 11.6])
        self.n = np.size(self.T)
        self.r = r
        self.rho=rho
        
        
    def LossWeightEq(self,Y):
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
            Time of inspection in hours change T into hours
        t : Float value
            Thickness of the pipe
    
    
        Returns
        -------
        d_corrosion : Float value
            Change in depth of the pipe
    
        """
        
        W_mean = np.mean(self.W)
        T_mean = np.mean(self.T)
    
        Sxy = np.sum(self.W*self.T)-self.n*W_mean*T_mean
        Sxx = np.sum(self.T*self.T)-self.n*T_mean*T_mean
    
        b1 = Sxy/Sxx
        b0 = W_mean-b1*T_mean
    
        y_pred = b1 * self.T + b0
        
        W_pred = b1 * Y + b0
        
        plt.scatter(self.T,self.W, color = 'red')
        plt.plot(self.T,y_pred, color = 'green')
        
        Cr = DepthClass.CorrosionRate(self,W_pred,Y*8760)

        d_corrosion = (0.20*self.t) + Cr * Y
        return d_corrosion

    def CorrosionRate(self,W_pred,Time): #time of inspection
        Cr = (87.6*W_pred)/(self.rho*(self.r**2*np.pi)*Time)
        return Cr
    





        
        