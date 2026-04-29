import numpy as np
import sys
from os.path import join
import matplotlib.pyplot as plt

def speed_up_plot(filename):
    data = np.genfromtxt(filename, delimiter=',')

    if data.ndim == 1:
        data = data.reshape(1, -1)

    data = data[~np.isnan(data).any(axis=1)]

    T1 = 2017.04
    processes = data[:, 0]
    times = T1 / data[:, 1]

    # order = np.argsort(processes)
    # processes = processes[order]
    # times = times[order]

    plt.figure()
    plt.plot(processes, times, marker='o')
    plt.xlabel('Number of processes')
    plt.ylabel('Time [seconds]')
    plt.title('Time to process 100 floorplans vs. number of processes')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    return plt.gcf()

if __name__ == "__main__":
    filename = sys.argv[1]
    fig = speed_up_plot(filename)
    fig.savefig(join("PLOTS/" + "speedups", f'static_speedup_plot.png'))
    plt.close(fig)
    