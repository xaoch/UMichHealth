#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:rtx8000:1
#SBATCH --time=8:00:00
#SBATCH --mem=4GB
#SBATCH --job-name=poseExtraction
#SBATCH --mail-type=END
#SBATCH --mail-user=xavier.ochoa@nyu.edu
#SBATCH --output=slurm_postureExtraction%j.out


OUTFILE=$2
OUTJSON=$3
VIDEOFILE=$1
# singularity run --nv --overlay /scratch/work/public/singularity/openpose1.7.0-cuda11.1.1-cudnn8-devel-ubuntu20.04-dep.sqf:ro /scratch/work/public/singularity/cuda11.1.1-cudnn8-devel-ubuntu20.04.sif /home/xao1/Code/CollaborationAnalysis/extractPoses.sh $VIDEOFILE $OUTFILE $OUTJSON

singularity exec --nv \
      --overlay /scratch/work/public/singularity/openpose1.7.0-cuda11.1.1-cudnn8-devel-ubuntu20.04-dep.sqf:ro \
	    /scratch/work/public/singularity/cuda11.1.1-cudnn8-devel-ubuntu20.04.sif \
	    /bin/bash /home/xao1/Code/UMichHealth/PostureExtraction.sh $VIDEOFILE $OUTFILE $OUTJSON

cd $OUTJSON
cd ..
tar -zcvf postures.tar.gz postures
rm -rf postures