'''
Get Raster Scan Voltage Array.
Created 02/24/2023 by Jacob Sage Vietorisz for Stein Biological Physics Lab, Brown University
Edited 02/27/2023 by Jacob Sage Vietorisz for Stein Biological Physics Lab, Brown University
'''

  
# Import necessary libraries
import numpy as np


def get_voltage_array(Vx_min, Vx_max, Vy_min, Vy_max, Vx_step, Vy_step):
    
    '''
    Code for creating raster scan voltage array. Written to be used in LabView 2020 with Python 3.6

    :params:
    :Vx_min: Float value. Lowest applied voltage to the X channel of the Thorlabs PPC102 piezo-actuated mirror controller.
    :Vx_max: Float value. Highest applied voltage to the X channel of the Thorlabs PPC102 piezo-actuated mirror controller.
    :Vy_min: Float value. Lowest applied voltage to the Y channel of the Thorlabs PPC102 piezo-actuated mirror controller.
    :Vy_max: Float value. Highest applied voltage to the Y channel of the Thorlabs PPC102 piezo-actuated mirror controller.
    :Vx_step: Float value. Amount to increment the applied X voltage between scan columns.
    :Vy_step: Float value. Amount to increment the applied Y voltage within each scan column.

    :returns:
    :voltage_array: (2 x n) Numpy array. Contains arrays of the X voltages -- voltage_array[0, :] -- 
                    and Y voltages -- voltage_array[1, :] -- to apply to the mirror controller. The dimension n depends on input params. 
    '''
    
    # Calculate number of discrete voltages in each channel
    Nx = int((Vx_max-Vx_min)/Vx_step)  # number of scan columns
    Ny = int((Vy_max-Vy_min)/Vy_step)  # number of discrete y voltages per column

    # Initialize arrays with minimum (starting) values
    Vx = np.full((Nx+1)*(Ny+1), Vx_min)
    Vy = np.full((Nx+1)*(Ny+1), Vy_min)

    # Define indexing template for Y channel
    y_template = np.array([i for i in range(Ny+1)], dtype='uint8')
    for i in range(0, Ny+1):
        y_template = np.append(y_template, Ny-i)
    
    # Iteratively define each voltage array
    for i in range((Nx+1)*(Ny+1)):
        Vx[i] = Vx[i]+Vx_step*np.floor(i/(Ny+1))
        Vy[i] = Vy[i]+Vy_step*(y_template[int(i%len(y_template))])
    
    
    voltage_array = np.array([Vx, Vy])
        
    return voltage_array
