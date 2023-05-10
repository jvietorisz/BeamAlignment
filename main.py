'''
Code for analyzing laser scan data
Written by Jacob Vietorisz 4/26/2023
for Stein Biological Physics Lab

This script analyzes files output by the raster scanning procedure 
to identify the optimal voltages to apply to the steering mirror 
to align the laser beam with the nanotip.
'''
from scan_analysis import load_data, model, fit_scan_data, find_alignment_voltages
from visualizers import plot_raw3D, plot_fit_model3D, plot_tip_location


def main():
    '''
    Main script which analyzes scan data and produces relevant plots.

    :params:
    none

    :returns:
    tip_x_inVolts: float. The voltage to apply to the X channel of the steering mirror to align beam with nanotip
    tip_y_inVolts: float. The voltage to apply to the Y channel of the steering mirror to align beam with nanotip

    '''
    # Define scan parameters
    path = '/Users/jacobvietorisz/Documents/Stein Lab Research/Raster Scanning/230304/230304_HighResScan_X(-25,0)_Y(-5,20)_2(10)-1_1000.lvm'
    
    # Voltage extrema (in V)
    Vx_min = -25
    Vx_max = 10
    Vy_min = 0
    Vy_max = 30

    # Boolean to decide if plotting
    plotting = True

#########################################

    # Load and extract scan data 
    indices, Vx_out, Vy_out, time, power_mW, X_pos, Y_pos = load_data(path)

    # Optimize parameters to fit scan data
    params, residuals, fit, xgrid, ygrid = fit_scan_data(model, Vx_out, Vy_out, power_mW, 
                                           Vx_min, Vx_max, Vy_min, Vy_max)
    
    # Find alignment voltages
    fit, xs, ys, tip_x, tip_x_inVolts, tip_y, tip_y_inVolts = find_alignment_voltages(fit, Vx_min, Vx_max, Vy_min, Vy_max, params)

#########################################

    if plotting == True:
        plot_raw3D(Vx_out, Vy_out, power_mW)
        plot_fit_model3D(fit, xgrid, ygrid)
        plot_tip_location(fit, xs, ys, tip_x, tip_x_inVolts, tip_y, tip_y_inVolts, 
                          Vx_min, Vx_max, Vy_min, Vy_max)
        
    return tip_x_inVolts, tip_y_inVolts
        


if __name__ == "__main__":
    main()

