'''
Code for analyzing laser scan data
Written by Jacob Vietorisz 4/26/2023
for Stein Biological Physics Lab

This script produces plots of the scan data in various representations.
'''
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_raw3D(Vx, Vy, power):
    '''
    Produces 3D scatter plot of raw scan data.

    :params:
    Vx: 1D np.array. X voltages applied to steering mirror
    Vy: 1D np.array. Y voltages applied to steering mirror
    power: 1D np.array. Power measured on sensor for each voltage pair
    
    :returns:
    none
    '''
    fig = plt.figure()
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)

    # Plot the raw data
    scatter = ax.scatter(Vx, Vy, power, c=power, marker='o', s=3)

    # cbar_ax = fig.add_axes([0.95, 0.15, 0.03, 0.7])
    # fig.colorbar(scatter, cax=cbar_ax, cmap=cm.viridis, label='power (mW)')

    ax.set_zlim3d(2.5,6.5)
    ax.set_xlabel('Applied x Voltage (V)')
    ax.set_ylabel('Applied Y Voltage (V)')
    ax.set_zlabel('Measured Power (mW)')
    # ax.set_title('Raw Scan Data')

    # plt.savefig('raw_scan2.svg', format='svg', dpi=1200)
    plt.show()
    return

def plot_fit_model3D(fit, xgrid, ygrid):
    '''
    Produces 3D surface plot of the scan model.

    :params:
    fit: 2D np.array. The fitted model
    xgrid: 2D np.array. The X dimension of grid over which to plot the fit
    ygrid: 2D np.array. The Y dimension of grid over which to plot the fit
    
    :returns:
    none
    '''
    fig = plt.figure()
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)

    surface_fit = ax.plot_surface(xgrid, ygrid, fit, cmap='viridis', alpha=0.9)

    ax.set_zlim3d(2.5,6.5)
    ax.set_xlabel('Applied x Voltage (V)')
    ax.set_ylabel('Applied Y Voltage (V)')
    ax.set_zlabel('Measured Power (mW)')

    # plt.savefig('model2.svg', format='svg', dpi=1200)
    plt.show()
    return

def plot_tip_location(fit, xs, ys, tip_x, tip_x_inVolts, tip_y, tip_y_inVolts, 
                      Vx_min, Vx_max, Vy_min, Vy_max):
    '''
    Plots 2D representation of the scan model, 
    as well as the threshold points and tip location.

    :params:
    fit: 2D np.array. Fitted model of scan data. The predicted measured power
    tip_x_inVolts: float. X voltage to align beam with tip
    tip_y_inVolts: float. Y voltage to align beam with tip
    xs: 1D np.array. Indices of the x voltages with pixels satisfying threshold
    ys: 1D np.array. Indices of the y voltages with pixels satisfying threshold
    Vx_min: float. minimum X voltage set for scan
    Vx_max: float. maximum X voltage set for scan
    Vy_min: float. minimum X voltage set for scan
    Vy_max: float. maximum X voltage set for scan

    :returns:
    none
    '''

    num_xticks = (Vx_max-Vx_min)/5 +1
    num_yticks = (Vy_max-Vy_min)/5 +1
    xticks = np.linspace(0, fit.shape[1], num_xticks)
    yticks = np.linspace(0, fit.shape[0], num_yticks)
    
    xlabels = np.arange(Vx_min, Vx_max+1, num_xticks)
    ylabels = np.arange(Vy_min, Vy_max+1, num_yticks)
    plt.xticks(xticks, xlabels)
    plt.yticks(yticks, ylabels)
    
    plt.xlabel('Applied X voltage (V)', fontsize=10)
    plt.ylabel('Applied Y voltage (V)', fontsize=10)
    # plt.title('Przedicted Tip Coordinates')

    plt.scatter(xs, ys, s=0.2, color='red')
    plt.scatter(tip_x, tip_y, s=40, color='limegreen', marker='o', 
                label=f'Tip at ({tip_x_inVolts},{tip_y_inVolts})')
    plt.imshow(fit, cmap='binary')
    plt.legend()

    # plt.savefig('tipLocation2.svg', format='svg', dpi=1200)
    plt.show()
    return 