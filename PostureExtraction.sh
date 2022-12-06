#!/bin/bash

cd /home/xao1/Code/openpose

mkdir $3

build/examples/openpose/openpose.bin \
    --video $1 \
    --write_json $3 \
    --write_video $2 \
    --display 0

ffmpeg -y -i $2 "${2/%avi/mp4}"