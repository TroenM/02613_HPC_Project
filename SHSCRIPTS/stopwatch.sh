#bin/bash.sh

#BSUB -J stoptime
#BSUB -o ./OUTPUTS/FULLGPUV100/stoptime.out
#BSUB -e ./OUTPUTS/FULLGPUV100/stoptime.err

#BSUB -q hpc
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=64MB]"
#BSUB -w full_jobs

#BSUB -W 00:05

echo "ARRAY_END_TIME: $(date)"