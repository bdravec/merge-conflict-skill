#!/bin/bash
# Holds a 1x H100 allocation on gpu-invest so an interactive shell can attach
# via `srun --jobid=<id> --overlap --pty bash` -- survives submit-host reboots,
# tmux death, SSH drops, etc. (Unlike `srun --pty bash` which dies with the
# client and loses the queue position.)
#
# Usage:
#   sbatch scripts/slurm/hold_h100.sh
#   squeue -u $USER                                   # wait for ST=R
#   srun --jobid=<JOBID> --overlap --pty bash         # attach interactively
#   # ...do work in the attached shell...
#   scancel <JOBID>                                   # release when done
#
# Mem/CPU sized for vLLM serving Qwen3-32B in bf16 (~64 GB weights → host RAM
# during load, ~4 CPUs for tokenizer/scheduler threads). Adjust for other models.

#SBATCH --job-name=h100-hold
#SBATCH --partition=gpu-invest
#SBATCH --gres=gpu:h100:1
#SBATCH --time=02:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G
#SBATCH --output=slurm-%j.out

echo "==========================================="
echo "Allocation acquired"
echo "  host:   $(hostname)"
echo "  date:   $(date)"
echo "  jobid:  $SLURM_JOB_ID"
echo "  nodes:  $SLURM_NODELIST"
echo ""
echo "Attach with:"
echo "  srun --jobid=$SLURM_JOB_ID --overlap --pty bash"
echo ""
echo "Holding for --time=02:00:00. SLURM will SIGTERM at timeout."
echo "==========================================="

# Hold the allocation; SLURM sends SIGTERM at --time, exiting cleanly.
sleep infinity
