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
def single_jacobi_kernel(u, u_new, delta_array, interior_mask):
    # Offset indices to skip the 1-pixel boundary
    i, j = cuda.grid(2)
    
    # Only compute relevant points
    if interior_mask[i, j]:
        # Jacobi Stencil (Assuming no interior points are also boundary points)
        u_new[i, j] = 0.25 * (u[i, j-1] + u[i, j+1] + u[i-1, j] + u[i+1, j])
        # delta_array[i, j] = abs(u[i, j] - u_new[i, j])
    else:
        u_new[i, j] = u[i, j]
        # delta_array[i, j] = 0.0

    # Avoid cpu side flipping references
    u[i, j] = u_new[i, j]  # Update u for the next iteration, but this won't affect the current kernel execution

@cuda.jit
def noif_jacobi_kernel(u, u_new, delta_array, interior_mask):
    # Offset indices to skip the 1-pixel boundary
    i, j = cuda.grid(2)

    # 
    is_interior = interior_mask[i, j]
    u_prime = 0.25 * (u[i, (j-1*is_interior)] + 
                      u[i, (j+1*is_interior)] + 
                      u[(i-1*is_interior), j] + 
                      u[(i+1*is_interior), j]) 
    
    # Use the mask to select between the computed value and the original value without branching
    u_new[i,j] = interior_mask[i, j]*u_prime + (1 - interior_mask[i, j])*u[i, j]
    # delta_array[i, j] = abs(u[i, j] - u_new[i, j])


def run_jacobi(u, u_new, delta_array, interior_mask, max_iter, atol):
    tpb = (16, 16)  # threads per block
    bpg_x = (u.shape[0] + tpb[0] - 1) // tpb[0]
    bpg_y = (u.shape[1] + tpb[1] - 1) // tpb[1]
    bpg = (bpg_x, bpg_y)

    u_d = cuda.to_device(u)
    u_new_d = cuda.to_device(u_new)
    delta_array_d = cuda.to_device(delta_array)
    interior_mask_d = cuda.to_device(interior_mask)

    # Run the kernel
    for i in range(max_iter):
        noif_jacobi_kernel[bpg, tpb](u_d, u_new_d, delta_array_d, interior_mask_d)
        # single_jacobi_kernel[bpg, tpb](u_d, u_new_d, delta_array_d, interior_mask_d)
        cuda.synchronize()  # Ensure kernel has finished before checking for convergence

        # if (i + 1) % 100 == 0:  # Check for convergence every 100 iterations
        #     delta_array = delta_array_d.copy_to_host()
        #     max_delta = delta_array.max()
        #     if max_delta < atol:
        #         break

    return u_d.copy_to_host(u)  # Copy final result back to host

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
    MAX_ITER = 10_000
    ABS_TOL = 1e-4

    all_u = np.empty_like(all_u0)
    for i, (u0, interior_mask) in enumerate(zip(all_u0, all_interior_mask)):
        u = run_jacobi(u0, np.empty_like(u0), np.empty_like(u0), interior_mask, MAX_ITER, ABS_TOL)
        all_u[i] = u

    print(f"Total execution time: {perf_counter() - t_start:.2f} seconds")

# Print summary statistics in CSV format
    # stat_keys = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
    # print('building_id, ' + ', '.join(stat_keys))  # CSV header
    # for bid, u, interior_mask in zip(building_ids, all_u, all_interior_mask):
    #     stats = summary_stats(u, interior_mask)
    #     print(f"{bid},", ", ".join(str(stats[k]) for k in stat_keys))