#!/bin/bash
#SBATCH --mail-user=es4753@nyu.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=stylegan3_garfield_training
#SBATCH --open-mode=append
#SBATCH --output=/scratch/es4753/logs-project/%j_%x.out
#SBATCH --error=/scratch/es4753/logs-project/%j_%x.err
#SBATCH --export=ALL
#SBATCH --time=48:00:00
#SBATCH --gres=gpu:1
#SBATCH --mem=64G
#SBATCH -c 12

singularity exec --nv --overlay $SCRATCH/overlay-25GB-500K.ext3:rw /scratch/work/public/singularity/cuda10.1-cudnn7-devel-ubuntu18.04-20201207.sif /bin/bash -c "
source /ext3/env.sh
conda activate

python ../stylegan3/train.py --outdir=/scratch/es4753/training-runs --cfg=stylegan3-t \
  --data=/scratch/es4753/garfield_images.zip --gpus=8 --batch=32 --gamma=8.2 \
  --mirror=1
"