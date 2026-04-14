#!/bin/bash

#BSUB -J jacobi_lprof.py
#BSUB -o OUTPUTS/jacobi_lprof%J.out
#BSUB -e OUTPUTS/jacobi_lprof%J.err

#BSUB -q hpc
#BSUB -n 1
#BSUB -W 00:10
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=5GB]"
#BSUB -R "select[model==XeonGold6226R]"

# Notifications
##BSUB -u <mail>
##BSUB -B
##BSUB -N

source SHSCRIPTS/init_02613.sh
kernprof -l -o OUTPUTS/jacobi_orignal.lprof PYSCRIPTS/jacobi_profilling.py 15
python -m line_profiler -rmt OUTPUTS/jacobi_orignal.lprof
