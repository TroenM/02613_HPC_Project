#bin/bash.sh

#BSUB -J cuda_kernel
#BSUB -o ./OUTPUTS/cuda_kernel_initial%J.out
#BSUB -e ./OUTPUTS/cuda_kernel_initial%J.err

#BSUB -q c02613
##BSUB -q gpua100
#BSUB -n 8
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -gpu "num=1:mode=exclusive_process"

#BSUB -W 00:10

source ../init_02613.sh

# python -u PYSCRIPTS/cuda_kernel_initial.py 100 >> OUTPUTS/full_stats.csv
python -u PYSCRIPTS/cuda_kernel_initial.py 100