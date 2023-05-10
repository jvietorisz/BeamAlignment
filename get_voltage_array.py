# Code for creating raster scan voltage array
  
# Import necessary libraries
import numpy as np


def get_voltage_array(Vx_min, Vx_max, Vy_min, Vy_max, Vx_step, Vy_step):
    
    Nx = int((Vx_max-Vx_min)/Vx_step)  # number of discrete x voltages
    Ny = int((Vy_max-Vy_min)/Vy_step)  # number of discrete y voltages per column

    Vx = np.full((Nx+1)*(Ny+1), Vx_min)
    Vy = np.full((Nx+1)*(Ny+1), Vy_min)

    # Define sorters
    y_template = np.array([i for i in range(Ny+1)], dtype='uint8')
    for i in range(0, Ny+1):
        y_template = np.append(y_template, Ny-i)
    

    for i in range((Nx+1)*(Ny+1)):
        Vx[i] = Vx[i]+Vx_step*np.floor(i/(Ny+1))
        Vy[i] = Vy[i]+Vy_step*(y_template[int(i%len(y_template))])
    
    
    voltage_array = np.array([Vx, Vy])
    return voltage_array

voltage_array = get_voltage_array(Vx_min=0, Vx_max=20, Vy_min=0, Vy_max=20, Vx_step=2, Vy_step=2)
print(voltage_array)