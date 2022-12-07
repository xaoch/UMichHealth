# Instructions

## Extract Poses

sbatch PostureExtraction.s /scratch/xao1/UMichHealth/KEMK18/KEMK18_1.mp4 /scratch/xao1/UMichHealth/KEMK18/KEMK18_1_OP.avi /scratch/xao1/UMichHealth/KEMK18/postures_1/
sbatch PostureExtraction.s /scratch/xao1/UMichHealth/KEMK18/KEMK18_2.mp4 /scratch/xao1/UMichHealth/KEMK18/KEMK18_2_OP.avi /scratch/xao1/UMichHealth/KEMK18/postures_2/
sbatch PostureExtraction.s /scratch/xao1/UMichHealth/HCAJ18/HCAJ18_1.mp4 /scratch/xao1/UMichHealth/HCAJ18/HCAJ18_1_OP.avi /scratch/xao1/UMichHealth/HCAJ18/postures_1/
sbatch PostureExtraction.s /scratch/xao1/UMichHealth/HCAJ18/HCAJ18_2.mp4 /scratch/xao1/UMichHealth/HCAJ18/HCAJ18_2_OP.avi /scratch/xao1/UMichHealth/HCAJ18/postures_2/

## Installing Whisper
SINGULARITY_IMAGE=/scratch/work/public/singularity/ubuntu-20.04.1.sif
OVERLAY_FILE=/scratch/work/public/examples/greene-getting-started/overlay-15GB-500K-pytorch.ext3
singularity exec --nv --overlay $OVERLAY_FILE $SINGULARITY_IMAGE /bin/bash

source /ext3/miniconda3/bin/activate
conda create --prefix /scratch/xao1/whisper
pip install git+https://github.com/openai/whisper.git 

## Transcript
sbatch WhisperTranscript.s /scratch/xao1/UMichHealth/KEMK18/KEMK18_1.mp4 /scratch/xao1/UMichHealth/KEMK18/transcript_1/
sbatch WhisperTranscript.s /scratch/xao1/UMichHealth/KEMK18/KEMK18_2.mp4 /scratch/xao1/UMichHealth/KEMK18/transcript_2/
sbatch WhisperTranscript.s /scratch/xao1/UMichHealth/HCAJ18/HCAJ18_1.mp4 /scratch/xao1/UMichHealth/HCAJ18/transcript_1/
sbatch WhisperTranscript.s /scratch/xao1/UMichHealth/HCAJ18/HCAJ18_1.mp4 /scratch/xao1/UMichHealth/HCAJ18/transcript_2/

## extract Audio

sbatch extractAudio.s /scratch/xao1/UMichHealth/KEMK18/KEMK18_1.mp4
sbatch extractAudio.s /scratch/xao1/UMichHealth/KEMK18/KEMK18_2.mp4
sbatch extractAudio.s /scratch/xao1/UMichHealth/HCAJ18/HCAJ18_1.mp4
sbatch extractAudio.s /scratch/xao1/UMichHealth/HCAJ18/HCAJ18_1.mp4


## Transcript Nemo
sbatch NemoTranscript.s /scratch/xao1/UMichHealth/KEMK18/KEMK18_1.wav /scratch/xao1/UMichHealth/KEMK18/KEMK_18_1 4
sbatch NemoTranscript.s /scratch/xao1/UMichHealth/KEMK18/KEMK18_2.wav /scratch/xao1/UMichHealth/KEMK18/KEMK_18_2 4
sbatch NemoTranscript.s /scratch/xao1/UMichHealth/HCAJ18/HCAJ18_1.wav /scratch/xao1/UMichHealth/HCAJ18/HCAJ_18_1 4
sbatch NemoTranscript.s /scratch/xao1/UMichHealth/HCAJ18/HCAJ18_2.wav /scratch/xao1/UMichHealth/HCAJ18/HCAJ_18_2 4