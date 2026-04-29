#!/bin/bash

#BSUB -J dynamic_parallel[1-10]
#BSUB -o OUTPUTS/DYNAMIC_PARALLEL/dynamic_parallel_%I.out
#BSUB -e OUTPUTS/DYNAMIC_PARALLEL/dynamic_parallel_%I.err

#BSUB -q hpc
#BSUB -n 10
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -W 00:30

source SHSCRIPTS/init_02613.sh
python PYSCRIPTS/dynamic_parallel.py 100 $LSB_JOBINDEX >> OUTPUTS/TIMING/dynamic_times.csv