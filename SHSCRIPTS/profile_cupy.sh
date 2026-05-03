#!/bin/bash

#BSUB -J profile_cupy
#BSUB -o OUTPUTS/profile_cupy%J.out
#BSUB -e OUTPUTS/profile_cupy%J.err

#BSUB -q c02613
#BSUB -n 4
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=512MB]"
#BSUB -gpu "num=1:mode=exclusive_process"

#BSUB -W 00:30

source SHSCRIPTS/init_02613.sh

nsys profile -o OUTPUTS/cupy_profile python PYSCRIPTS/cupy_gpu.py 100
nsys stats OUTPUTS/cupy_profile.nsys_rep