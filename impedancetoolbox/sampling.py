# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 13:21:26 2023

@author: teresia
"""
import numpy as np
from .constants import SPEED_OF_LIGHT

def generate_time_points(wake_range,n_points):
    
    # TODO: check so input is integer
    
    # Convert n_points to int
    n_points = int(n_points)
    
    
    def is_odd(number):
        return number % 2 != 0
    
    # Check if the number of points is an odd number otherwise increase with +1
    # TODO: add why is needed
    
    if(~is_odd(n_points)):
       n_points += 1
       print('Number of sampling points is adjusted {0} to have odd number of points\n'.format(n_points))
       
    return np.linspace(-wake_range,wake_range,n_points)/SPEED_OF_LIGHT

# TODO: add sampling for Elegant'

# def bunch_profile(time,bunch_length):
    
#     bunch_duration = bunch_length/SPEED_OF_LIGHT
    
#     bunch_profile = 1/(np.sqrt(2*np.pi)*bunch_duration)*np.exp(-time**2/(2*bunch_duration**2))
    
#     return bunch_profile

    
def convolute(time,wake,bunch_length):
    
    s = time*SPEED_OF_LIGHT
    
    bunch_profile = 1/(np.sqrt(2*np.pi)*bunch_length)*np.exp(-s**2/(2*bunch_length**2))
    
    delta = s[1]-s[0];
    
    return delta*np.convolve(wake, bunch_profile,"same")


# def raw_moment(x, counts, order):
              
#     return np.sum(x**order*counts) / np.sum(counts)
  


    

    
    

    
    
    
