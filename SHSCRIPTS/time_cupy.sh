#!/bin/bash

#BSUB -J time_cupy
#BSUB -o OUTPUTS/time_cupy%J.out
#BSUB -e OUTPUTS/time_cupy%J.err

#BSUB -q c02613
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -gpu "num=1:mode=exclusive_process"

#BSUB -W 00:30

source SHSCRIPTS/init_02613.sh

echo "Original search/replace cupy script:"
python PYSCRIPTS/cupy_gpu.py 100

echo "Using cp.where to mask:"
python PYSCRIPTS/cupy_gpu_copy.py 100