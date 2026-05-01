#bin/bash.sh

#BSUB -J full
#BSUB -o ./OUTPUTS/FULLGPUV100/full.out
#BSUB -e ./OUTPUTS/FULLGPUV100/full.err

#BSUB -q hpc
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"

#BSUB -W 00:10

echo "ARRAY_START_TIME: $(date)"
bsub < SHSCRIPTS/submit_full_jobs.sh
bsub < SHSCRIPTS/stopwatch.sh