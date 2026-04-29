from os.path import join
import sys

import numpy as np
import matplotlib.pyplot as plt

def plot_mask_and_temperature(u: np.ndarray, interior_mask: np.ndarray, bid: str, plot_subdir='raw_data/') -> None:
    """
    Creates a side-by-side plot of the interior mask and the temperature distribution for a given building ID (bid).
    The plot is saved to the specified subdirectory under "PLOTS/plot_subdir".
    """
    fig, ax = plt.subplots(1,2,figsize=(12, 5), dpi = 300)
    ax[0].imshow(interior_mask, cmap='hot', interpolation='nearest')
    ax[0].set_xlabel('X-axis')
    ax[0].set_ylabel('Y-axis')
    ax[0].set_title(f'Interior Mask for Building {bid}')

    ax[1].imshow(u, cmap='hot', interpolation='nearest')
    ax[1].set_xlabel('X-axis')
    ax[1].set_ylabel('Y-axis')
    ax[1].set_title(f'Temperature Distribution for Building {bid}')

    cbar = plt.colorbar(ax[1].imshow(u, cmap='hot', interpolation='nearest'), ax=ax[1])
    cbar.set_label('Temperature (°C)')

    plt.tight_layout()
    plt.savefig(join("PLOTS/" + plot_subdir, f'{bid}_temperature_distribution.png'))
    plt.close()
    

def plot_temperature_distribution(u, bid, plot_subdir='temperature_distributions/'):
    """
    Creates a plot of the temperature distribution for a given building ID (bid) and saves it to the specified subdirectory under "PLOTS/plot_subdir".
    """
    fig, ax = plt.subplots(figsize=(6, 5), dpi = 500)
    im = ax.imshow(u, cmap='hot', interpolation='nearest')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title(f'Temperature Distribution for Building {bid}')
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Temperature (°C)')
    plt.tight_layout()
    plt.savefig(join("PLOTS/" + plot_subdir, f'{bid}_temperature_distribution.png')) 
    plt.close()

if __name__ == '__main__':
    from simulate_original import load_data    
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'

    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()
    if len(sys.argv) < 2:
        N = 1
    else:
        N = int(sys.argv[1])
    building_ids = building_ids[:N]

    for bid in building_ids:
        u0, interior_mask = load_data(LOAD_DIR, bid)
        plot_temperature_distribution(u0, bid)
        plot_mask_and_temperature(u0, interior_mask, bid)
