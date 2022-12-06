#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:rtx8000:1
#SBATCH --time=0:20:00
#SBATCH --mem=16GB
#SBATCH --job-name=NemoTranscript
#SBATCH --mail-type=END
#SBATCH --mail-user=xavier.ochoa@nyu.edu
#SBATCH --output=slurm_NemoTranscript%j.out


OUTDIR=$2
VIDEOFILE=$1
SPEAKERS=$3
# singularity run --nv --overlay /scratch/work/public/singularity/openpose1.7.0-cuda11.1.1-cudnn8-devel-ubuntu20.04-dep.sqf:ro /scratch/work/public/singularity/cuda11.1.1-cudnn8-devel-ubuntu20.04.sif /home/xao1/Code/CollaborationAnalysis/extractPoses.sh $VIDEOFILE $OUTFILE $OUTJSON

SINGULARITY_IMAGE=/scratch/work/public/singularity/ubuntu-20.04.1.sif
OVERLAY_FILE=/scratch/work/public/examples/greene-getting-started/overlay-15GB-500K-pytorch.ext3
singularity exec --nv --overlay $OVERLAY_FILE $SINGULARITY_IMAGE /bin/bash /home/xao1/Code/UMichHealth/NemoTranscript.sh $VIDEOFILE $OUTDIR $SPEAKERS