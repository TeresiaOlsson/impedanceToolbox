# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 13:21:26 2023

@author: teresia
"""
import numpy as np
from .constants import SPEED_OF_LIGHT
#from scipy.special import binom

def generate_time_points(wake_range,n_points):
    
    # TODO: check so input is integer
    
    # Convert n_points to int
    n_points = int(n_points)
    
    
    def is_odd(number):
        return number % 2 != 0
    
    # Check if the number of points is an odd number otherwise increase with +1    
    if(~is_odd(n_points)):
       n_points += 1
       print('Number of sampling points is adjusted {0} to have odd number of points to include zero in range\n'.format(n_points))
       
    return np.linspace(-wake_range,wake_range,n_points)/SPEED_OF_LIGHT


# TODO: add sampling for Elegant'

# def bunch_profile(time,bunch_length):
    
#     bunch_duration = bunch_length/SPEED_OF_LIGHT
    
#     bunch_profile = 1/(np.sqrt(2*np.pi)*bunch_duration)*np.exp(-time**2/(2*bunch_duration**2))
    
#     return bunch_profile
    
# def convolute(time,wake,bunch_length):
    
#     profile = bunch_profile(time,bunch_length)
#     delta = time[1]-time[0]
    
#     return delta*np.convolve(wake, profile,"same")   
        
    
def convolute(time,wake,bunch_length):
    
    s = time*SPEED_OF_LIGHT
    
    bunch_profile = 1/(np.sqrt(2*np.pi)*bunch_length)*np.exp(-s**2/(2*bunch_length**2))
    
    delta = s[1]-s[0];
    
    return delta*np.convolve(wake, bunch_profile,"same")    
    

# def convolute_moments(wake_moments,bunch_moments,nOrders):
    
#     momentsZ = np.zeros(nOrders+1)
#     momentsDx = np.zeros(nOrders+1)
#     momentsDy = np.zeros(nOrders+1)
    
#     for j in range(nOrders+1):     
        
#         n = j
#         print("j :" + str(j))
        
#         for i in range(n+1):
#             print("i: " + str(i))
#             momentsZ[j] += binom(n,i)*wake_moments[0][i]*bunch_moments[n-i]
#             print(binom(n,i)*wake_moments[0][i]*bunch_moments[n-i])
            
#     return (momentsZ,momentsDx,momentsDy)
        
        
        
# def raw_moment(x, counts, order):
              
#     return np.sum(x**order*counts) / np.sum(counts)


# def calculate_bunch_moments(time,bunch_length,nOrders):
    
#     profile = bunch_profile(time,bunch_length)
    
#     moments = np.zeros(nOrders+1)
    
#     for i in range(nOrders+1): 
#         moments[i] = raw_moment(time,profile,i)
        
#     return moments
     



    

    
    

    
    
    
