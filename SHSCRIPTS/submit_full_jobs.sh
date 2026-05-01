#bin/bash.sh

#BSUB -J full_jobs[1-2]
#BSUB -o ./OUTPUTS/FULLGPUV100/full_jobs%I.out
#BSUB -e ./OUTPUTS/FULLGPUV100/full_jobs%I.err

#BSUB -q gpuv100
#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=3GB]"
#BSUB -gpu "num=1:mode=exclusive_process"

#BSUB -W 01:00

source ../init_02613.sh

time python -u PYSCRIPTS/cuda_kernel.py 2286 $LSB_JOBINDEX >> OUTPUTS/full_stats.csv