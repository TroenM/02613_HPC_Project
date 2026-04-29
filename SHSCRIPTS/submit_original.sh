#!/bin/bash

#BSUB -J simulate_orig_100
#BSUB -o OUTPUTS/simulate_orig_100%J.out
#BSUB -e OUTPUTS/simulate_orig_100%J.err

#BSUB -q hpc
#BSUB -n 1
#BSUB -W 00:40
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=5GB]"
#BSUB -R "select[model==XeonGold6226R]"

# Notifications
##BSUB -u <mail>
#BSUB -B
#BSUB -N

source SHSCRIPTS/init_02613.sh
python -u PYSCRIPTS/simulate_original.py 100