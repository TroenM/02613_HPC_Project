#!/bin/bash

#BSUB -J time_cupy
#BSUB -o OUTPUTS/time_cupy%J.out
#BSUB -e OUTPUTS/time_cupy%J.err

#BSUB -q c02613
#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -gpu "num=1:mode=exclusive_process"

#BSUB -W 00:30

source SHSCRIPTS/init_02613.sh

time python PYSCRIPTS/cupy_gpu.py 15