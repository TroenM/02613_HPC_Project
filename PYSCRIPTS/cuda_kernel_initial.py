from os.path import join
import sys

import numpy as np
from numba import cuda
from plotting import plot_temperature_distribution
from time import perf_counter

def load_data(load_dir, bid):
    SIZE = 512
    u = np.zeros((SIZE + 2, SIZE + 2))
    u[1:-1, 1:-1] = np.load(join(load_dir, f"{bid}_domain.npy"))
    interior_mask = np.load(join(load_dir, f"{bid}_interior.npy"))
    return u, interior_mask

@cuda.jit
def noif_jacobi_kernel(u, u_new, interior_mask):
    i, j = cuda.grid(2)

    # Using is_interior as (0 or 1) to avoid branching and avoids boundary checks
    is_interior = interior_mask[i-1, j-1]
    u_new[i,j] = 0.25 * (u[i, (j-is_interior)] + 
                      u[i, (j+is_interior)] + 
                      u[(i-is_interior), j] + 
                      u[(i+is_interior), j])


def run_jacobi(u, u_new, interior_mask, max_iter, atol):
    tpb = (8, 8)  # threads per block
    bpg_x = (u.shape[0] + tpb[0] - 1) // tpb[0]
    bpg_y = (u.shape[1] + tpb[1] - 1) // tpb[1]
    bpg = (bpg_x, bpg_y)

    u_d = cuda.to_device(u)
    u_new_d = cuda.to_device(u_new)
    interior_mask_d = cuda.to_device(interior_mask)

    # Run the kernel
    for i in range(max_iter):
        noif_jacobi_kernel[bpg, tpb](u_d, u_new_d, interior_mask_d)
        cuda.synchronize()  # Ensure kernel has finished before checking for convergence
        u_new_d, u_d = u_d, u_new_d  # Swap references for next iteration

    return u_d.copy_to_host(u)  # Copy final result back to host

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

    all_u = np.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = run_jacobi(u0, np.empty_like(u0), interior_mask, MAX_ITER, ABS_TOL)
        all_u[i] = u
    print(f"Total execution time: {perf_counter() - t_start:.2f} seconds")

# Print summary statistics in CSV format
    # stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    # print('building_id, ' + ', '.join(stat_keys))  # CSV header
    # for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
    #     stats = summary_stats(u, interior_mask)
    #     print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))