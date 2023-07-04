# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 08:31:30 2023

@author: teresia
"""

#import itertools
from .wake_objects import Wake, ResistiveWallWakeFunction
import numpy as np
from .utils import convolute
from .sources import Source

class ImpedanceLattice(object):
    
    # --- Constructor ---   
    def __init__(self,lattice_list):
        self._lattice = list(self._unnest_list(lattice_list))
        
    # --- Properties ---
    
    @property
    def lattice(self):
        return self._lattice
    
    # --- Methods ---
       
    # Unnest list
    
    def _unnest_list(self, input_list):
       
        # Check so input is list
        if(isinstance(input_list,list)):
            
            for item in input_list:
                if(isinstance(item,list)):
                    self.unnest_list(item)
                else:
                    print(item)
                    yield item
                             
        else:
            yield input_list
            
    """ Generate lumped resistive wall wake """
    def generate_resistive_wall_wake(self,source,time_points,beta_functions,convolution_bunch_length):
                
        if source == Source.ANALYTIC:
            
        # Necessary to use even number of sampling points for the convolution to work correctly 
            if (convolution_bunch_length > 0):
                initial_time_points = time_points
                time_points = np.linspace(np.min(time_points),np.max(time_points),len(time_points)+1)    
               
               
            # Generate analytic resistive-wall
        
            lumped_wake = Wake(time_points,None,None)
        
            for element in self._lattice:
                
                rho = element.material
                beff = element.RW_radius
                length = element.length
                          
                lumped_wake.add(ResistiveWallWakeFunction(time_points,rho,beff,length))
                
                # TODO: add transverse 
                
            if (convolution_bunch_length > 0):
                
                # Do convolution
                wakeZ_conv = convolute(time_points,lumped_wake.wakeZ,convolution_bunch_length)
                wakeDx_conv = convolute(time_points,lumped_wake.wakeDx,convolution_bunch_length)
                wakeDy_conv = convolute(time_points,lumped_wake.wakeDy,convolution_bunch_length)
                wakeQx_conv = convolute(time_points,lumped_wake.wakeQx,convolution_bunch_length)
                wakeQy_conv = convolute(time_points,lumped_wake.wakeQy,convolution_bunch_length)
    
                # TODO: Add transverse
    
                # Change the sampling points back and change the wake
                lumped_wake.time = initial_time_points
                lumped_wake.wakeZ = np.interp(initial_time_points,time_points,wakeZ_conv)
                lumped_wake.wakeDx = np.interp(initial_time_points,time_points,wakeDx_conv)
                lumped_wake.wakeDx = np.interp(initial_time_points,time_points,wakeDy_conv)
                lumped_wake.wakeQx = np.interp(initial_time_points,time_points,wakeQx_conv)
                lumped_wake.wakeQy = np.interp(initial_time_points,time_points,wakeQy_conv)
                            
            
        return lumped_wake
        
class ImpedanceElement(object):
    
    # --- Constructor ---
    def __init__(self,name,length):
        
        self._name = name;
        self._length = length;
        self._group = None
        self._material = None
        self._thickness = None;
        self._RW_radius = None
        #self._apertures = None;
        
        
    # --- Properties ---
    
    @property
    def name(self):
        return self._name
    
    @property
    def length(self):
        return self._length
    
    @property
    def group(self):
        return self._group
    
    @property
    def material(self):
        return self._material
    
    @property
    def thickness(self):
        return self._thickness
    
    @property
    def RW_radius(self):
        return self._RW_radius
    
    # @property
    # def apertures(self):
    #     return self._apertures
    
        
        # self._RW_wake_files = None;
        # self._RW_impedance_files = None;
        # self._geometic
        
class Drift(ImpedanceElement):
    
    # --- Constructor ---
    def __init__(self,name,length,material,thickness,RW_radius):

        self._name = name;
        self._length = length;
        self._material = material
        self._thickness = thickness
        self._RW_radius = RW_radius
    
# class Taper(ImpedanceElement):
    
#     # --- Constructor ---
#     def __init__(self,name,length):
#         self._name = name;
#         self._length = length;
#         self._material = None
#         self._thickness = None;
#         self._apertures = None;    
        
# class BPM(ImpedanceElement):
     
#      # --- Constructor ---
#      def __init__(self,name,length):
#          self._name = name;
#          self._length = length;
#          self._material = None
#          self._thickness = None;
#          self._apertures = None;
         
# class Flange(ImpedanceElement):
     
#      # --- Constructor ---
#      def __init__(self,name,length):
#          self._name = name;
#          self._length = length;
#          self._material = None
#          self._thickness = None;
#          self._apertures = None;
        
# class Valve(ImpedanceElement):
     
#      # --- Constructor ---
#      def __init__(self,name,length):
#          self._name = name;
#          self._length = length;
#          self._material = None
#          self._thickness = None;
#          self._apertures = None;
         
# class Stripline(ImpedanceElement):
     
#      # --- Constructor ---
#      def __init__(self,name,length):
#          self._name = name;
#          self._length = length;
#          self._material = None
#          self._thickness = None;
#          self._apertures = None;

# class Cavity(ImpedanceElement):
     
#      # --- Constructor ---
#      def __init__(self,name,length):
#          self._name = name;
#          self._length = length;
#          self._material = None
#          self._thickness = None;
#          self._apertures = None;

# class InsertionDevice(ImpedanceElement):
     
#      # --- Constructor ---
#      def __init__(self,name,length):
#          self._name = name;
#          self._length = length;
#          self._material = None
#          self._thickness = None;
#          self._apertures = None;            
         
         