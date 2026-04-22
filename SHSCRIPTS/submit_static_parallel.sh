#!/bin/bash

#BSUB -J static_parallel[2-10]
#BSUB -o OUTPUTS/STATIC_PARALLEL/static_parallel_%I.out
#BSUB -e OUTPUTS/STATIC_PARALLEL/static_parallel_%I.err

#BSUB -q hpc
#BSUB -n 10
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -R "select[model==XeonGold6226R]"
#BSUB -W 00:30

source SHSCRIPTS/init_02613.sh
python PYSCRIPTS/static_parallel.py 100 $LSB_JOBINDEX >> OUTPUTS/TIMING/static_times.csv