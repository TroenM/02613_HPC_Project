from os.path import join
import sys

import numpy as np
from plotting import plot_temperature_distribution
import multiprocessing as mp
from time import perf_counter


def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask


def jacobi(u, interior_mask, max_iter, atol=1e-6):
    u = np.copy(u)

    for i in range(max_iter):
        # Compute average of left, right, up and down neighbors, see eq. (1)
        u_new = 0.25 * (u[1:-1, :-2] + u[1:-1, 2:] + u[:-2, 1:-1] + u[2:, 1:-1])
        u_new_interior = u_new[interior_mask]
        delta = np.abs(u[1:-1, 1:-1][interior_mask] - u_new_interior).max()
        u[1:-1, 1:-1][interior_mask] = u_new_interior

        if delta < atol:
            break
    return u


def summary_stats(u, interior_mask):
    u_interior = u[1:-1, 1:-1][interior_mask]
    mean_temp = u_interior.mean()
    std_temp = u_interior.std()
    pct_above_18 = np.sum(u_interior > 18) / u_interior.size * 100
    pct_below_15 = np.sum(u_interior < 15) / u_interior.size * 100
    return {
        'mean_temp': mean_temp,
        'std_temp': std_temp,
        'pct_above_18': pct_above_18,
        'pct_below_15': pct_below_15,
    }

def jacobi_chunk(u0_chunk, interior_mask_chunk, max_iter, atol = 1e-6):
    """
    Helper method for chunked parallelization
    """
    u_chunk = np.empty_like(u0_chunk)
    for i, (u0, interior_mask) in enumerate(zip(u0_chunk, interior_mask_chunk)):
        u = jacobi(u0, interior_mask, max_iter, atol)
        u_chunk[i] = u

    return u_chunk


if __name__ == '__main__':
    t_start = perf_counter()
    # Load data
    LOAD_DIR = '/dtu/projects/02613_2025/data/modified_swiss_dwellings/'
    with open(join(LOAD_DIR, 'building_ids.txt'), 'r') as f:
        building_ids = f.read().splitlines()

    if len(sys.argv) < 2:
        N = 1
    else:
        N = int(sys.argv[1])
    building_ids = building_ids[:N]

    # Load floor plans
    all_u0 = np.empty((N, 514, 514))
    all_interior_mask = np.empty((N, 512, 512), dtype='bool')
    for i, bid in enumerate(building_ids):
        u0, interior_mask = load_data(LOAD_DIR, bid)
        all_u0[i] = u0
        all_interior_mask[i] = interior_mask

    # Run jacobi iterations for each floor plan
    MAX_ITER = 20_000
    ABS_TOL = 1e-4


    n_proc = int(sys.argv[2]) # Number of processes
    chunk_size = N//n_proc + ((N%n_proc) != 0) # Number of floors per process

    with mp.Pool(n_proc) as pool:
        tasks = []
        for b in range(0,N,chunk_size):
            u_slice = all_u0[b:b+chunk_size]
            interior_mask_slice = all_interior_mask[b:b+chunk_size]
            
            res = pool.apply_async(jacobi_chunk, (u_slice, interior_mask_slice, MAX_ITER, ABS_TOL, ))
            tasks.append(res)
        
        result = [t.get() for t in tasks]
    
    all_u = np.concatenate(result, axis = 0)
    print(f"{n_proc}, {perf_counter() - t_start}", flush=True, end = "\n")


# Print summary statistics in CSV format
    # stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    # print('building_id, ' + ', '.join(stat_keys))  # CSV header
    # for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
    #     stats = summary_stats(u, interior_mask)
    #     print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))