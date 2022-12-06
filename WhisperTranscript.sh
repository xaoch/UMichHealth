#!/bin/bash

VIDFILE=$1
DIR=$2

source /ext3/miniconda3/bin/activate

conda activate /scratch/xao1/whisper

mkdir $DIR

whisper --language English --model large --output_dir $DIR $VIDFILE