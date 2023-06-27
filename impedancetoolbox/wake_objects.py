# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 11:59:12 2023

@author: teresia
"""

import numpy as np
from scipy.integrate import quad_vec
from . import constants

class Wake(object):
       
    # --- Constructor ---
   
    def __init__(self,time,wake,factor):        
        self._time = time; # Time
        
        if (wake != None):
            self._wakeZ = wake[:,0]; # Longitudinal wake
            self._wakeDx = wake[:,1]; # Horizontal dipole wake
            self._wakeDy = wake[:,2]; # Vertical dipole wake
            self._wakeQx = wake[:,3]; # Horizontal quadrupole wake
            self._wakeQy = wake[:,4]; # Vertical quadrupole wake
        else:
            self._wakeZ = np.zeros(len(time))
            self._wakeDx = np.zeros(len(time))
            self._wakeDy = np.zeros(len(time))
            self._wakeQx = np.zeros(len(time))
            self._wakeQy = np.zeros(len(time))
            
        if (factor != None):
            self._factorZ = factor[:,0];
            self._factorX = factor[:,1];
            self._factorY = factor[:,2];
        else:
            self._factorZ = 1
            self._factorX = 1
            self._factorY = 1
                        
    # ---  Properties ---
    
    @property
    def time(self):
        return self._time
    
    @property
    def wakeZ(self):
        return self._wakeZ
    
    @wakeZ.setter
    def wakeZ(self,value):
        self._wakeZ = value
    
    @property
    def wakeDx(self):
        return self._wakeDx       

    @property
    def wakeDy(self):
        return self._wakeDy
    
    @property
    def wakeQx(self):
        return self._wakeQx
    
    @property
    def wakeQy(self):
        return self._wakeQy
    
    @property
    def factorZ(self):
        return self._factorZ    
    
    @property
    def factorX(self):
        return self._factorX      
    
    @property
    def factorY(self):
        return self._factorY
    
    # --- Methods ---
    
    def add(self,new_wake):
        
        # TODO add check of same time
        
        self._wakeZ = np.add(self._wakeZ,new_wake.wakeZ)
        
    def save_AT_file(self,filename):
        
        s = self._time.reshape((-1,1))*constants.SPEED_OF_LIGHT
        
        wake_matrix = np.concatenate((s,self._wakeZ.reshape((-1,1)),self._wakeDx.reshape((-1,1)),self._wakeDx.reshape((-1,1)),self._wakeQx.reshape((-1,1)),self._wakeQy.reshape((-1,1))),axis=1)
        
        np.savetxt(filename,wake_matrix,header = "s [m] Long. wake [V/C] Hor. dipole wake [V/m/C] Ver. dipole wake [V/m/C] Hor. quadrupole wake [V/m^2/C] Ver. dipole wake [V/m^2/C]")
           
class ResistiveWallWakeFunction(Wake):
    
    speed_of_light = constants.SPEED_OF_LIGHT;
    impedance_free_space = constants.IMPEDANCE_FREE_SPACE
    
    # --- Constructor ---
    def __init__(self,time,rho,beff,length):
        self._time = time
        self._rho = rho
        self._beff = beff
        self._length = length
        
        #s = self.speed_of_light*time
        
        self._wakeZ = self.longitudinal_RW_wake(time,rho,beff,length)
        # TODO benchmark transverse
        self._wakeDx = self.transverse_RW_wake(time,rho,beff,length)
        self._wakeDy = self.transverse_RW_wake(time,rho,beff,length)
        
    # --- Properties ---    
    
    @property
    def time(self):
        return self._time
    
    @property
    def rho(self):
        return self._rho
    
    @property
    def beff(self):
        return self._beff    
        
    @property
    def length(self):
        return self._length
    
    # --- Analytic wakefield functions ---
    
    def longitudinal_RW_wake(self,time,rho,beff,length):
        # Based on equation 22 in Skripka et al. 'Simultaneous computation of intrabunch and interbunch collective beam motions in storage rings'
        # The equation gives the wake function per length unit
        
        s0 = (2*beff**2*rho/self.impedance_free_space)**(1./3)
        tau0 = s0/self.speed_of_light
        
        wake = np.zeros(len(time))
        
        # Find index of time >= 0
        index = np.where(time >= 0)
        
        tau = time[index]
        
        f = lambda x : x**2*np.exp(-x**2*tau/tau0)/(x**6+8);
        
        y, err = quad_vec(f,0,np.inf)
        
        wake[index] = 4*self.impedance_free_space*self.speed_of_light/(np.pi*beff**2)*(np.exp(-tau/tau0)/3 * np.cos(np.sqrt(3)*tau/tau0) - np.sqrt(2)/np.pi * y)*length
             
        return wake
    
    def transverse_RW_wake(self,time,rho,beff,length):
    # Based on equation 25 in Skripka et al. 'Simultaneous computation of intrabunch and interbunch collective beam motions in storage rings'
    # Multiplied with s0 since missing in formula
    # The equation gives the wake function per length unit

        s0 = (2*beff**2*rho/self.impedance_free_space)**(1/3);
        tau0 = s0/self.speed_of_light;
        
        wake = np.zeros(len(time))
        
        # Find index of time >= 0
        index = np.where(time >= 0)
        
        tau = time[index]
        
        f = lambda x : -np.exp(-x**2*tau/tau0)/(x**6+8);
        
        y, err = quad_vec(f,0,np.inf)
        
        # Negative sign on wake necessary to get detuning in tracking in AT
        wake[index] = -s0*8*self.impedance_free_space*self.speed_of_light/(np.pi*beff**4)*(1/12 * (-np.exp(-tau/tau0)*np.cos(np.sqrt(3)*tau/tau0) + np.sqrt(3)*np.exp(-tau/tau0)*np.sin(np.sqrt(3)*tau/tau0)) - np.sqrt(2)/np.pi*y)*length
        
        return wake
    
        
# class WakeFromIW2D(Wakefield):
    
#     # --- Constructor ---
#     def __init__(self,time,filepath,length):
#         self._time = time
#         self._fileZ = filepath[0]
#         self._fileDX = filepath[1]
#         self._fileDY = filepath[2]
#         self._fileQX = filepath[3]
#         self._fileQY = filepath[4]
         
#         s = self.speed_of_light*time
        
#         # Read longitudinal wake
#         self._wakeZ = self.read_IW2D_wake(self._fileZ)
#         self._wakeDX = self.read_IW2D_wake(self._fileDX)
#         self._wakeDY = self.read_IW2D_wake(self._fileDY)
#         self._wakeQX = self.read_IW2D_wake(self._fileQX)
#         self._wakeQY = self.read_IW2D_wake(self._fileQY)       
        
#         # Make the wake equally spaced
        
#         # Resample wake
        
#         # Multiply wake with length
        
#     def read_IW2D_wake(filepath):
        
#         if filepath is not None:
            
#             # Read in the IW2D data
#             data = np.loadtxt(filepath,skiprows=1)
        
#             return data
            
            
            
            
            
        

    
#     function struct = import_IW2D_wake(file,sampling_points,betas,convolution_bunch_length)
# %% Process impedanceWake2D input

#     %% Read in data
    
#     % Read file
#     fileID = fopen(file);
#     data = textscan(fileID,'%f %f %s %s','CommentStyle','#');
#     fclose(fileID);        
        
#     % Split file for planes
#     index = find(data{1} == 0);
#     data_lon = cellfun(@(v)v (index),data,'UniformOutput',false);

#     index = find(data{1} == 1);
#     data_hor = cellfun(@(v)v (index),data,'UniformOutput',false);

#     index = find(data{1} == 2);       
#     data_ver = cellfun(@(v)v (index),data,'UniformOutput',false);    
    
#     %% If convolution, even number of points required for numerical convolution to work correctly

#     if convolution_bunch_length ~= 0
#         initial_sampling_points = sampling_points;  
#         sampling_points = linspace(min(sampling_points),max(sampling_points),length(sampling_points)+1)';    
#     end

#     %% Create output wakes

#     WakeZ = zeros(length(sampling_points),1);
#     WakeDX = zeros(length(sampling_points),1);
#     WakeDY = zeros(length(sampling_points),1); 
    
#     %% Longitudinal wake
#     fprintf('Reading IW2D wake files\n'); 
       
#     fprintf('Reading longitudinal files\n');        
#     for i = 1:size(data_lon{1},1)
                
#         RW_length = data_lon{2}(i);
#         filename = char(data_lon{3}(i));
        
#         if ~isempty(filename)
            
#             lon_wake = importdata(filename);
#             lon_wake = lon_wake.data;
            
#             % Make the wake equally spaced
#             lon_wake = make_equally_spaced(lon_wake); 

#             % Resample wake
#             wake = interp1(lon_wake(:,1),lon_wake(:,2),sampling_points,'linear',0);

#             % Multiply wake with length
#             wake = wake.*RW_length;         

#             WakeZ = WakeZ + wake;
#         end
                             
#     end
#     fprintf('Finished reading longitudinal files. Read %d lines.\n\n',i);
        
#     %% Horizontal wake

#     if ~isempty(betas)                
#         % Calculate average horizontal beta over element lengths       
#         element_length = data_hor{2};
#         element_s = [0; cumsum(element_length)]';         
#         average_betax = zeros(1,length(element_s)-1);         
#         for i = 1:length(element_s)-1                   
#             average_betax(i) = integrate(betas.betax,element_s(i+1),element_s(i))./element_length(i);            
#         end
#     else
#         average_betax = 1;
#     end            
      
#     fprintf('Reading horizontal files\n');    
#     for i = 1:size(data_hor{1},1)
        
#         RW_length = data_hor{2}(i);
#         filename = char(data_hor{3}(i));
        
#         if ~isempty(filename)
            
#             hor_wake = importdata(filename);
#             hor_wake = hor_wake.data;

#             % Make the wake equally spaced
#             hor_wake = make_equally_spaced(hor_wake); 

#             % Resample wake
#             wake = interp1(hor_wake(:,1),hor_wake(:,2),sampling_points,'linear',0);  

#             % Multiply wake with length and change sign to to fit with AT
#             % conventions
#             wake = -wake.*RW_length;

#             WakeDX = WakeDX + wake.*average_betax(i);
#         end
                            
#     end
#     fprintf('Finished reading horizontal files. Read %d lines.\n\n',i);
               
#     %% Vertical wake
    
#     if ~isempty(betas)                
#         % Calculate average vertical beta over element lengths       
#         element_length = data_ver{2};
#         element_s = [0; cumsum(element_length)]';         
#         average_betay = zeros(1,length(element_s)-1);         
#         for i = 1:length(element_s)-1                   
#             average_betay(i) = integrate(betas.betay,element_s(i+1),element_s(i))./element_length(i);            
#         end
#     else
#         average_betay = 1;
#     end
    
#     fprintf('Reading vertical files\n');

#     for i = 1:size(data_ver{1},1)
        
#         RW_length = data_ver{2}(i);
#         filename = char(data_ver{3}(i));
        
#         if ~isempty(filename)
            
#             ver_wake = importdata(filename);
#             ver_wake = ver_wake.data;

#             % Make the wake equally spaced
#             ver_wake = make_equally_spaced(ver_wake); 

#             % Resample wake
#             wake = interp1(ver_wake(:,1),ver_wake(:,2),sampling_points,'linear',0);  

#             % Multiply wake with length and change sign to to fit with AT
#             % conventions
#             wake = -wake.*RW_length;

#             WakeDY = WakeDY + wake.*average_betay(i);
#         end
        
#     end
#     fprintf('Finished reading vertical files. Read %d lines.\n\n',i);
    
#     %% Convolute wake

#     if convolution_bunch_length ~= 0

#         conv_lon_wake = convolute(sampling_points,WakeZ,convolution_bunch_length);
#         conv_hor_wake = convolute(sampling_points,WakeDX,convolution_bunch_length);     
#         conv_ver_wake = convolute(sampling_points,WakeDY,convolution_bunch_length); 

#         % Changing sampling points back to initial points
#         WakeZ = interp1(sampling_points,conv_lon_wake,initial_sampling_points);
#         WakeDX = interp1(sampling_points,conv_hor_wake,initial_sampling_points);
#         WakeDY = interp1(sampling_points,conv_ver_wake,initial_sampling_points);

#         sampling_points = initial_sampling_points;

#     end

#     %% Create output struct

#     struct.WakeT = sampling_points;
#     struct.WakeZ = WakeZ;
#     struct.WakeDX = WakeDX;
#     struct.WakeDY = WakeDY;     
#     struct.WakeQX = zeros(length(sampling_points),1); 
#     struct.WakeQY = zeros(length(sampling_points),1);
#     struct.average_betax = average_betax;
#     struct.average_betay = average_betay;      

# end

# %%%%%%%%%%%%%%%%% Format IW2D input %%%%%%%%%%%%%%%%%%%%%%


# function new_wake = make_equally_spaced(wake)

# s = wake(:,1);
# values = wake(:,2);

# % Find index closes to zero
# [value, index] = min(abs(s));

# % Find values of index next to zero
# low_index = index - 1;
# high_index = index + 1;

# low_value = values(low_index);
# high_value = values(high_index);

# mean_value = (low_value+high_value)./2;

# % Replace these three points with a single point at zero
# new_values = values;
# new_values(index) = mean_value;

# new_s = s;
# new_s(index) = 0;

# new_values(low_index) = [];
# new_values(index) = [];

# new_s(low_index) = [];
# new_s(index) = [];

# new_wake = cat(2,new_s,new_values);

# end
    
    