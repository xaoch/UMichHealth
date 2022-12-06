#!/bin/bash

VIDFILE=$1
DIR=$2
SPEAKERS=$3

source /ext3/miniconda3/bin/activate

conda activate /scratch/xao1/nemo

mkdir $DIR

python /home/xao1/Code/UMichHealth/NemoTranscript.py -i $VIDFILE -o $DIR -s $SPEAKERS