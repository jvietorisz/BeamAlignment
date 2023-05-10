'''
Code for analyzing laser scan data
Written by Jacob Vietorisz 4/26/2023
for Stein Biological Physics Lab

This script contains functions to analyze the output of the raster 
scanning procedure to identify the optimal voltages to apply to the 
steering mirror to align the laser beam with the nanotip.
'''

# Import necessary packages
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import scipy as sc
from skimage import feature


def load_data(path):
    '''
    Loads and unpacks a scan file.

    :params:
    path: string. Path to the csv file containing the scan data

    :returns:
    indices: 1D np.array. Unifying indices for all measured quantities
    Vx_out: 1D np.array.  channel voltages applied to steering mirror during scan, in order 
    Vy_out: 1D np.array. Y channel voltages applied to steering mirror during scan, in order 
    time: 1D np.array. Time (ms) measured at each applied voltage pair and measured power
    power_mW: 1D np.array. Power (mW) measured by sensor for each pair of applied steering voltages
    X_pos: 1D np.array. X positions measured by sensor for each pair of applied steering voltages
    Y_pos:  1D np.array. Y positions measured by sensor for each pair of applied steering voltages
    
    '''
    scan = np.loadtxt(path, dtype = float, skiprows = 22)

    # Extract data from scan file
    indices = scan[:, 0]
    Vx_out = scan[:, 1]
    Vy_out = scan[:, 2]
    time = scan[:, 3]-scan[0, 3] #Calculate time in experiment.
    power_mW = scan[:, 4]*(10**3) # Convert from W to mW
    X_pos = scan[:, 5]*10**(-3) # Convert to easier (arbitrary) units
    Y_pos = scan[:, 6]*10**(-3)

    return indices, Vx_out, Vy_out, time, power_mW, X_pos, Y_pos

def model(data, alpha, a, beta, b, delta, d, const):
    '''
    Function to which to fit scan data.

    :params:
    data: tuple of 1D np.arrays. X and Y channel voltages
    alpha, a, beta, b, delta, d, const: parameters fit during optimization

    :returns:
    fit: 2D np.array. High resolutionn modeled power values
    '''
    # amplitude and sd vary linearly with distance from tip
    X = data[0]
    Y = data[1]
    Amp = alpha*X+a
    sigma = beta*X+b
    D = delta*X+d 
    
    # make piecewise
    Amp[Amp<0]=0
    fit = const - np.abs(Amp*np.exp(-(Y-d)**2/(2*sigma**2)))
    return fit


def fit_scan_data(model, Vx_out, Vy_out, power, Vx_min, Vx_max, Vy_min, Vy_max):
    '''
    Optimizes parameters to fit the scan data to the model by 
    non-linear least squares regression.

    :params:
    model: function. function defining the model to which to fit data
    Vx: 1D np.array. X voltages applied to the steering mirror
    Vy: 1D np.array. X voltages applied to the steering mirror
    
    :returns:
    params: 1D np.array. Optimized fit parameters
    residuals: 2D np.array. Matrix of residuals
    fit: 2D np.array. Fitted model of scan data
    '''

    # Create grid for plotting fit
    n = 10*int(np.sqrt(len(Vx_out)))
    xg = np.linspace(Vx_min, Vx_max+1, n)
    yg = np.linspace(Vy_min, Vy_max+1, n)
    xgrid, ygrid = np.meshgrid(xg, yg)

    # Linear fitting
    params, residuals = sc.optimize.curve_fit(model, [Vx_out, Vy_out], power, 
                                             maxfev=100000, p0=[0.1, 2.0, 0.1, 2.25, 0.0, 8, 5.8])
    fit = model([xgrid, ygrid], *params)
    return params, residuals, fit, xgrid, ygrid

def find_alignment_voltages(fit, Vx_min, Vx_max, Vy_min, Vy_max, params):
    '''
    Finds the optimal voltages to align laser beam with nanotip.

    :params:
    fit: 2D np.array. Fitted model of scan data. The predicted measured power
    Vx_min: float. minimum X voltage set for scan
    Vx_mad: float. maximum X voltage set for scan
    Vy_min: float. minimum X voltage set for scan
    Vy_max: float. maximum X voltage set for scan

    :returns:
    tip_x: int. index within fit of the X voltage to align beam with tip
    tip_x_inVolts: float. X voltage to align beam with tip
    tip_y: int. index within fit of the Y voltage to align beam with tip
    tip_y_inVolts: float. Y voltage to align beam with tip
    xs: 1D np.array. Indices of the x voltages with pixels satisfying threshold
    ys: 1D np.array. Indices of the y voltages with pixels satisfying threshold
    '''

    H = 0.05 # Threshold signal
    const = params[6] # Baseline signal

    keypoints_grid = np.zeros(fit.shape)
    bottom = const - H*const
    top = const - (H-0.01)*const

    for i_j, el in np.ndenumerate(fit):
        if el >= bottom and el <= top:
            keypoints_grid[i_j] = 1
    
    local_max_cords = feature.peak_local_max(keypoints_grid, min_distance=1)
    xs = local_max_cords[:, 1]
    ys = local_max_cords[:, 0]

    # Average the positions of the 5 leftmost points
    sorted_indices = np.argsort(xs)
    leftmost_indices = sorted_indices[0:5]
    xleftmost_values = np.array([xs[el] for el in leftmost_indices])
    yleftmost_values = np.array([ys[el] for el in leftmost_indices])
    tip_x = np.mean(xleftmost_values)
    tip_y = np.mean(yleftmost_values)

    
    
    # Convert from fit mesh space to voltages
    tip_x_inVolts = Vx_min + tip_x*((Vx_max-Vx_min)/fit.shape[1])
    tip_x_inVolts = np.round(tip_x_inVolts, 2)

    tip_y_inVolts = Vy_min + tip_y*((Vy_max-Vy_min)/fit.shape[0])
    tip_y_inVolts = np.round(tip_y_inVolts, 2)

    return fit, xs, ys, tip_x, tip_x_inVolts, tip_y, tip_y_inVolts