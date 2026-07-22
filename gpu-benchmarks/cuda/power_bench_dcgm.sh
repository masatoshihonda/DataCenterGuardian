#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=short
#SBATCH --time=00:15:00
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --job-name=power_dcgm
#SBATCH --reservation=202607

module purge
module load CUDA

echo "=== GPU info ==="
nvidia-smi --query-gpu=name,power.limit --format=csv

dcgmi profile --pause

echo "MARKER: compute-bound (sustained_gemm) start $(date +%s.%N)"
dcgmi dmon -e 155,203,204,100 -d 200 -c 40 > dcgm_compute.log &
DCGM_PID=$!
sleep 1
./sustained_gemm 4096 2000
wait $DCGM_PID
echo "MARKER: compute-bound end $(date +%s.%N)"

sleep 2

echo "MARKER: memory-bound (laplace3d) start $(date +%s.%N)"
dcgmi dmon -e 155,203,204,100 -d 200 -c 40 > dcgm_memory.log &
DCGM_PID=$!
sleep 1
../prac3/laplace3d
wait $DCGM_PID
echo "MARKER: memory-bound end $(date +%s.%N)"

dcgmi profile --resume

echo "=== DCGM log: compute-bound (sustained_gemm) ==="
cat dcgm_compute.log

echo "=== DCGM log: memory-bound (laplace3d) ==="
cat dcgm_memory.log
