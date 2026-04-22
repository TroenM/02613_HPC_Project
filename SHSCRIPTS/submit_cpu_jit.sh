#!/bin/bash

#BSUB -J jit.py
#BSUB -o OUTPUTS/jit_simulate%J.out
#BSUB -e OUTPUTS/jit_simulate%J.err
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
time python PYSCRIPTS/cpu_jit.py 15