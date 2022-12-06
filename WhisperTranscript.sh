#!/bin/bash

VIDFILE=$1
DIR=$2

source /ext3/miniconda3/bin/activate

conda activate /scratch/xao1/asr/whisper

mkdir $DIR

whisper --language English --model large --ouput_dir $DIR $VIDFILE